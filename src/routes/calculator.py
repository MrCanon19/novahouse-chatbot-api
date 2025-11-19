"""
Price Calculator Route
======================
Instant price calculation for all packages based on square meters
"""

from flask import Blueprint, jsonify, request

calculator_routes = Blueprint("calculator", __name__, url_prefix="/api/calculator")


# Package prices per m²
PACKAGE_PRICES = {
    "express": 999,
    "express_plus": 1199,
    "comfort": 1499,
    "premium": 1999,
}


@calculator_routes.route("/calculate", methods=["POST"])
def calculate_price():
    """
    Calculate instant price for all packages

    Request JSON:
    {
        "square_meters": 60
    }

    Response:
    {
        "square_meters": 60,
        "calculations": {
            "express": {
                "price_per_sqm": 999,
                "total_price": 59940,
                "total_price_formatted": "59 940 zł"
            },
            ...
        }
    }
    """
    try:
        data = request.get_json()

        if not data or "square_meters" not in data:
            return jsonify({"error": "Missing square_meters parameter"}), 400

        square_meters = float(data["square_meters"])

        if square_meters <= 0:
            return jsonify({"error": "Square meters must be greater than 0"}), 400

        if square_meters > 1000:
            return (
                jsonify(
                    {
                        "error": "For projects over 1000m², please contact us directly for a custom quote"
                    }
                ),
                400,
            )

        # Calculate for all packages
        calculations = {}
        for package_key, price_per_sqm in PACKAGE_PRICES.items():
            total = square_meters * price_per_sqm
            calculations[package_key] = {
                "name": package_key.replace("_", " ").title(),
                "price_per_sqm": price_per_sqm,
                "total_price": int(total),
                "total_price_formatted": f"{int(total):,} zł".replace(",", " "),
            }

        return jsonify({"square_meters": square_meters, "calculations": calculations})

    except ValueError:
        return jsonify({"error": "Invalid square_meters value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@calculator_routes.route("/prices", methods=["GET"])
def get_prices():
    """Get current price list per m²"""
    return jsonify(
        {
            "prices_per_sqm": PACKAGE_PRICES,
            "packages": [
                {
                    "id": "express",
                    "name": "Express",
                    "price": 999,
                    "description": "Najbardziej ekonomiczna opcja, 150 produktów",
                },
                {
                    "id": "express_plus",
                    "name": "Express Plus",
                    "price": 1199,
                    "description": "Rozszerzony wybór, 300 produktów",
                },
                {
                    "id": "comfort",
                    "name": "Comfort",
                    "price": 1499,
                    "description": "Wyższy standard, 450 produktów Premium",
                },
                {
                    "id": "premium",
                    "name": "Premium",
                    "price": 1999,
                    "description": "Najwyższa jakość, pełna personalizacja",
                },
            ],
        }
    )
