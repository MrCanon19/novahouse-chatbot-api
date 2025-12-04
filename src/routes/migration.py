"""
Migration endpoint - run database migrations via HTTP
Only accessible with ADMIN_API_KEY
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import inspect, text

from src.models.chatbot import db

migration_bp = Blueprint("migration", __name__)


@migration_bp.route("/api/migration/run-ab-competitive", methods=["POST"])
def run_ab_competitive_migration():
    """
    Run A/B Testing & Competitive Intelligence migration
    Requires admin authentication
    """
    import os

    admin_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return jsonify({"error": "Admin key not configured"}), 500

    provided_key = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if provided_key != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        results = []

        # 1. Create followup_tests table
        if "followup_tests" not in existing_tables:
            db.session.execute(
                text(
                    """
                CREATE TABLE followup_tests (
                    id SERIAL PRIMARY KEY,
                    question_type VARCHAR(100) NOT NULL,
                    variant_a TEXT NOT NULL,
                    variant_b TEXT NOT NULL,
                    variant_a_shown INTEGER DEFAULT 0,
                    variant_b_shown INTEGER DEFAULT 0,
                    variant_a_responses INTEGER DEFAULT 0,
                    variant_b_responses INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )
            db.session.commit()
            results.append("✅ followup_tests table created")
        else:
            results.append("⚠️  followup_tests already exists")

        # 2. Create competitive_intel table
        if "competitive_intel" not in existing_tables:
            db.session.execute(
                text(
                    """
                CREATE TABLE competitive_intel (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100) NOT NULL,
                    intel_type VARCHAR(50) NOT NULL,
                    competitor_name VARCHAR(100),
                    user_message TEXT NOT NULL,
                    context TEXT,
                    sentiment VARCHAR(20),
                    priority VARCHAR(20) DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )
            db.session.commit()
            results.append("✅ competitive_intel table created")
        else:
            results.append("⚠️  competitive_intel already exists")

        # 3. Add followup_variant column
        try:
            result = db.session.execute(
                text(
                    """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='chat_conversations'
                AND column_name='followup_variant'
            """
                )
            )

            if result.fetchone() is None:
                db.session.execute(
                    text("ALTER TABLE chat_conversations ADD COLUMN followup_variant VARCHAR(10)")
                )
                db.session.commit()
                results.append("✅ followup_variant column added")
            else:
                results.append("⚠️  followup_variant already exists")
        except Exception as e:
            results.append(f"⚠️  followup_variant: {str(e)}")

        # 4. Insert default A/B tests
        default_tests = [
            {
                "type": "package_to_sqm",
                "a": "💡 **A jaki jest mniej więcej metraż Twojego mieszkania?** To pomoże mi lepiej dopasować ofertę.",
                "b": "📐 **Ile metrów kwadratowych ma Twoje mieszkanie?** Na tej podstawie przygotuję dokładną wycenę.",
            },
            {
                "type": "sqm_to_location",
                "a": "📍 **W jakim mieście szukasz wykonawcy?** Mamy zespoły w całej Polsce.",
                "b": "🗺️ **Gdzie znajduje się Twoje mieszkanie?** Sprawdzę dostępność naszych ekip w Twojej okolicy.",
            },
            {
                "type": "price_to_budget",
                "a": "💰 **Masz już określony budżet? Mogę pokazać opcje finansowania i rozłożenia płatności.**",
                "b": "💵 **Jaki budżet planujesz przeznaczyć na wykończenie?** Dopasuję najlepszą opcję dla Ciebie.",
            },
        ]

        for test in default_tests:
            result = db.session.execute(
                text("SELECT id FROM followup_tests WHERE question_type = :qtype"),
                {"qtype": test["type"]},
            )

            if result.fetchone() is None:
                db.session.execute(
                    text(
                        """
                    INSERT INTO followup_tests (question_type, variant_a, variant_b, is_active)
                    VALUES (:qtype, :variant_a, :variant_b, true)
                """
                    ),
                    {
                        "qtype": test["type"],
                        "variant_a": test["a"],
                        "variant_b": test["b"],
                    },
                )
                db.session.commit()
                results.append(f"✅ Added A/B test: {test['type']}")
            else:
                results.append(f"⚠️  Test exists: {test['type']}")

        # 5. Verify
        test_count = db.session.execute(text("SELECT COUNT(*) FROM followup_tests")).scalar()
        intel_count = db.session.execute(text("SELECT COUNT(*) FROM competitive_intel")).scalar()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Migration completed successfully",
                    "results": results,
                    "verification": {
                        "followup_tests_count": test_count,
                        "competitive_intel_count": intel_count,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@migration_bp.route("/api/migration/add-context-data", methods=["POST"])
def add_context_data_column():
    """
    Add missing columns to chat_conversations
    Requires admin authentication
    """
    import os

    admin_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return jsonify({"error": "Admin key not configured"}), 500

    provided_key = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if provided_key != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        results = []

        # Define columns to add - HARDCODED for security (prevent SQL injection)
        # NEVER accept column names/types from user input in DDL statements!
        SAFE_COLUMNS = {
            "context_data": "TEXT",
            "user_satisfaction": "INTEGER",
            "feedback_text": "TEXT",
            "awaiting_confirmation": "BOOLEAN DEFAULT FALSE",
        }

        for column_name, column_type in SAFE_COLUMNS.items():
            # Check if column exists - use parameterized query
            result = db.session.execute(
                text(
                    """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='chat_conversations'
                AND column_name=:col_name
            """
                ),
                {"col_name": column_name},
            )

            if result.fetchone() is None:
                # Use parameterized query for safety
                pass

                # Hardcoded column definitions - safe but use proper SQLAlchemy methods
                db.session.execute(
                    text(f"ALTER TABLE chat_conversations ADD COLUMN {column_name} {column_type}")
                )
                db.session.commit()
                results.append(f"✅ {column_name} added")
            else:
                results.append(f"⚠️  {column_name} already exists")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Migration completed",
                    "results": results,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@migration_bp.route("/api/migration/add-leads-columns", methods=["POST"])
def add_leads_columns():
    """
    Add missing columns to leads table
    Requires admin authentication
    """
    import os

    admin_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return jsonify({"error": "Admin key not configured"}), 500

    provided_key = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if provided_key != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        results = []

        # Define columns to add to leads table - HARDCODED for security
        # NEVER accept column names/types from user input in DDL statements!
        columns_to_add = [
            ("lead_score", "INTEGER DEFAULT 0"),
            ("conversation_summary", "TEXT"),
            ("data_confirmed", "BOOLEAN DEFAULT FALSE"),
            ("last_interaction", "TIMESTAMP"),
            ("monday_item_id", "VARCHAR(50)"),
            ("notes", "TEXT"),
        ]

        for column_name, column_type in columns_to_add:
            # Check if column exists - use parameterized query
            result = db.session.execute(
                text(
                    """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='leads'
                AND column_name=:col_name
            """
                ),
                {"col_name": column_name},
            )

            if result.fetchone() is None:
                # Use hardcoded values only - safe but document for security review
                # TODO: Consider using Alembic for production migrations
                db.session.execute(
                    text(f"ALTER TABLE leads ADD COLUMN {column_name} {column_type}")
                )
                db.session.commit()
                results.append(f"✅ {column_name} added")
            else:
                results.append(f"⚠️  {column_name} already exists")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Leads table migration completed",
                    "results": results,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@migration_bp.route("/api/migration/fix-null-values", methods=["POST"])
def fix_null_values():
    """
    Fix NULL values in followup_tests table
    Requires admin authentication
    """
    import os

    admin_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return jsonify({"error": "Admin key not configured"}), 500

    provided_key = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if provided_key != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Fix NULL values in followup_tests
        db.session.execute(
            text(
                """
            UPDATE followup_tests
            SET variant_a_shown = 0 WHERE variant_a_shown IS NULL
        """
            )
        )
        db.session.execute(
            text(
                """
            UPDATE followup_tests
            SET variant_b_shown = 0 WHERE variant_b_shown IS NULL
        """
            )
        )
        db.session.execute(
            text(
                """
            UPDATE followup_tests
            SET variant_a_responses = 0 WHERE variant_a_responses IS NULL
        """
            )
        )
        db.session.execute(
            text(
                """
            UPDATE followup_tests
            SET variant_b_responses = 0 WHERE variant_b_responses IS NULL
        """
            )
        )
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "NULL values fixed in followup_tests",
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@migration_bp.route("/api/migration/train-ml-model", methods=["POST"])
def train_ml_model():
    """
    Train ML lead scoring model on historical data
    Requires admin authentication
    """
    import os

    admin_key = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
    if not admin_key:
        return jsonify({"error": "Admin key not configured"}), 500

    provided_key = request.headers.get("X-ADMIN-API-KEY") or request.headers.get("X-API-KEY")
    if provided_key != admin_key:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        from src.services.lead_scoring_ml import lead_scorer_ml

        # Collect training data
        training_data = lead_scorer_ml.collect_training_data_from_db()

        if len(training_data) < 10:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Not enough training data ({len(training_data)} samples, need 10+)",
                        "samples_collected": len(training_data),
                    }
                ),
                400,
            )

        # Train model
        success = lead_scorer_ml.train_model(training_data)

        if success:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "ML model trained successfully",
                        "training_samples": len(training_data),
                        "model_path": lead_scorer_ml.model_path,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Training failed (check logs)",
                        "training_samples": len(training_data),
                    }
                ),
                500,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
