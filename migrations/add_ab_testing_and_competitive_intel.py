"""
Migration: Add A/B Testing and Competitive Intelligence tables
Date: 2024-12-19
"""

from sqlalchemy import inspect

from src.models.chatbot import CompetitiveIntel, FollowUpTest, db


def run_migration():
    """Create new tables and add initial A/B tests"""
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()

    # Create FollowUpTest table
    if "followup_tests" not in existing_tables:
        print("[Migration] Creating followup_tests table...")
        FollowUpTest.__table__.create(db.engine)
        print("✅ followup_tests table created")
    else:
        print("⚠️  followup_tests table already exists")

    # Create CompetitiveIntel table
    if "competitive_intel" not in existing_tables:
        print("[Migration] Creating competitive_intel table...")
        CompetitiveIntel.__table__.create(db.engine)
        print("✅ competitive_intel table created")
    else:
        print("⚠️  competitive_intel table already exists")

    # Add followup_variant column to chat_conversations if missing
    try:
        from sqlalchemy import text

        with db.engine.connect() as conn:
            # Check if column exists
            result = conn.execute(
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
                print("[Migration] Adding followup_variant column to chat_conversations...")
                conn.execute(
                    text("ALTER TABLE chat_conversations ADD COLUMN followup_variant VARCHAR(10)")
                )
                conn.commit()
                print("✅ followup_variant column added")
            else:
                print("⚠️  followup_variant column already exists")
    except Exception as e:
        print(f"[Migration] Error adding column: {e}")

    # Add initial A/B tests
    print("\n[Migration] Adding default A/B tests...")

    default_tests = [
        {
            "question_type": "package_to_sqm",
            "variant_a": "💡 **A jaki jest mniej więcej metraż Twojego mieszkania?** To pomoże mi lepiej dopasować ofertę.",
            "variant_b": "📐 **Ile metrów kwadratowych ma Twoje mieszkanie?** Na tej podstawie przygotuję dokładną wycenę.",
        },
        {
            "question_type": "sqm_to_location",
            "variant_a": "📍 **W jakim mieście szukasz wykonawcy?** Mamy zespoły w całej Polsce.",
            "variant_b": "🗺️ **Gdzie znajduje się Twoje mieszkanie?** Sprawdzę dostępność naszych ekip w Twojej okolicy.",
        },
        {
            "question_type": "price_to_budget",
            "variant_a": "💰 **Masz już określony budżet? Mogę pokazać opcje finansowania i rozłożenia płatności.**",
            "variant_b": "💵 **Jaki budżet planujesz przeznaczyć na wykończenie?** Dopasuję najlepszą opcję dla Ciebie.",
        },
    ]

    for test_data in default_tests:
        existing = FollowUpTest.query.filter_by(question_type=test_data["question_type"]).first()

        if not existing:
            test = FollowUpTest(
                question_type=test_data["question_type"],
                variant_a=test_data["variant_a"],
                variant_b=test_data["variant_b"],
                is_active=True,
            )
            db.session.add(test)
            print(f"✅ Added A/B test: {test_data['question_type']}")
        else:
            print(f"⚠️  A/B test already exists: {test_data['question_type']}")

    db.session.commit()
    print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    from main import app

    with app.app_context():
        run_migration()
