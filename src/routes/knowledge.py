"""
NovaHouse Knowledge Base API Endpoints
Endpointy udostępniające bazę wiedzy o firmie
"""

from flask import Blueprint, jsonify

from src.knowledge.novahouse_info import (
    BLOG_ARTICLES,
    CLIENT_REVIEWS,
    COMPANY_STATS,
    COVERAGE_AREAS,
    FAQ,
    PACKAGES,
    PORTFOLIO,
    PROCESS_STEPS,
    PRODUCT_PARTNERS,
    TEAM_INFO,
    WHY_CHOOSE_US,
    get_client_reviews_summary,
    get_portfolio_list,
    get_process_overview,
)
from src.middleware.security import rate_limit

knowledge_bp = Blueprint("knowledge", __name__)


@knowledge_bp.route("/packages", methods=["GET"])
def get_packages():
    """Zwraca listę pakietów wykończeniowych"""
    try:
        packages_list = []
        for key, package in PACKAGES.items():
            packages_list.append(
                {
                    "id": key,
                    "name": package["name"],
                    "price_per_sqm": package["price_per_sqm"],
                    "standard": package["standard"],
                    "ideal_for": package["ideal_for"],
                }
            )

        return jsonify(packages_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/faq", methods=["GET"])
def get_faq():
    """Zwraca FAQ - najczęściej zadawane pytania"""
    try:
        return jsonify(FAQ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/portfolio", methods=["GET"])
@rate_limit(max_requests=100, window_seconds=60)  # 100 req/min
def get_portfolio():
    """Zwraca listę portfolio - realizacje NovaHouse"""
    try:
        portfolio_list = []
        for key, project in PORTFOLIO.items():
            portfolio_list.append(
                {
                    "id": key,
                    "title": project["title"],
                    "type": project["type"],
                    "location": project["location"],
                    "url": project["url"],
                }
            )

        return (
            jsonify(
                {
                    "success": True,
                    "count": len(portfolio_list),
                    "portfolio": portfolio_list,
                    "description": get_portfolio_list(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/process", methods=["GET"])
def get_process():
    """Zwraca szczegółowy proces realizacji (4 kroki)"""
    try:
        steps = []
        for key, step in PROCESS_STEPS.items():
            steps.append(
                {
                    "step": key,
                    "title": step["title"],
                    "description": step["description"],
                    "duration": step["duration"],
                    "deliverables": step["deliverables"],
                }
            )

        return (
            jsonify(
                {
                    "success": True,
                    "total_steps": len(steps),
                    "steps": steps,
                    "overview": get_process_overview(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/reviews", methods=["GET"])
def get_reviews():
    """Zwraca opinie klientów z Google"""
    try:
        return (
            jsonify(
                {
                    "success": True,
                    "count": len(CLIENT_REVIEWS),
                    "reviews": CLIENT_REVIEWS,
                    "summary": get_client_reviews_summary(),
                    "google_url": "https://maps.google.com/?cid=15887695859047735593",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/partners", methods=["GET"])
def get_partners():
    """Zwraca listę partnerów produktowych"""
    try:
        return (
            jsonify(
                {
                    "success": True,
                    "count": len(PRODUCT_PARTNERS),
                    "partners": PRODUCT_PARTNERS,
                    "description": (
                        f"Współpracujemy z {len(PRODUCT_PARTNERS)} renomowanymi "
                        f"producentami materiałów wykończeniowych i wyposażenia wnętrz."
                    ),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/why-us", methods=["GET"])
def get_why_us():
    """Zwraca USP - dlaczego NovaHouse"""
    try:
        usp_list = [{"key": key, "value": value} for key, value in WHY_CHOOSE_US.items()]

        return jsonify({"success": True, "count": len(usp_list), "usp": usp_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/team", methods=["GET"])
def get_team():
    """Zwraca informacje o zespole"""
    try:
        return jsonify({"success": True, "team": TEAM_INFO}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/stats", methods=["GET"])
def get_stats():
    """Zwraca statystyki firmy"""
    try:
        return jsonify({"success": True, "stats": COMPANY_STATS, "coverage": COVERAGE_AREAS}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/blog", methods=["GET"])
def get_blog():
    """Zwraca listę artykułów blogowych"""
    try:
        return (
            jsonify({"success": True, "count": len(BLOG_ARTICLES), "articles": BLOG_ARTICLES}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@knowledge_bp.route("/all", methods=["GET"])
def get_all_knowledge():
    """Zwraca całą bazę wiedzy - przegląd"""
    try:
        return (
            jsonify(
                {
                    "success": True,
                    "summary": {
                        "stats": COMPANY_STATS,
                        "coverage": COVERAGE_AREAS,
                        "portfolio_count": len(PORTFOLIO),
                        "reviews_count": len(CLIENT_REVIEWS),
                        "partners_count": len(PRODUCT_PARTNERS),
                        "blog_articles": len(BLOG_ARTICLES),
                        "usp_count": len(WHY_CHOOSE_US),
                        "process_steps": len(PROCESS_STEPS),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
