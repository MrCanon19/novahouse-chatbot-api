#!/usr/bin/env python3
"""
Test ML Lead Scoring Model
Compare ML predictions with rule-based scoring
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timezone

from src.services.lead_scoring_ml import lead_scorer_ml


def test_ml_scoring():
    """Test ML scoring with sample data"""
    print("=" * 70)
    print("🧪 TESTING ML LEAD SCORING")
    print("=" * 70)
    print()

    # Test cases
    test_cases = [
        {
            "name": "High Quality Lead",
            "context_memory": {
                "name": "Jan Kowalski",
                "email": "jan@example.com",
                "phone": "+48123456789",
                "city": "Warszawa",
                "square_meters": 60,
                "package": "Express Plus",
            },
            "conversation_data": {
                "message_count": 8,
                "duration_minutes": 5.5,
                "messages": [
                    "Cześć, szukam wykończenia",
                    "Interesuje mnie Express Plus",
                    "60 metrów",
                    "Warszawa",
                    "jan@example.com",
                    "+48123456789",
                ],
                "timestamps": [datetime.now(timezone.utc) for _ in range(6)],
                "has_competitive_mention": False,
                "has_booking_intent": True,
            },
        },
        {
            "name": "Medium Quality Lead",
            "context_memory": {
                "name": "Anna Nowak",
                "email": "anna@example.com",
                "square_meters": 45,
            },
            "conversation_data": {
                "message_count": 4,
                "duration_minutes": 2.0,
                "messages": [
                    "Cześć",
                    "Jakie pakiety macie?",
                    "45m2",
                    "anna@example.com",
                ],
                "timestamps": [datetime.now(timezone.utc) for _ in range(4)],
                "has_competitive_mention": False,
                "has_booking_intent": False,
            },
        },
        {
            "name": "Low Quality Lead",
            "context_memory": {
                "name": "Test",
            },
            "conversation_data": {
                "message_count": 2,
                "duration_minutes": 0.5,
                "messages": ["Cześć", "Ok"],
                "timestamps": [datetime.now(timezone.utc) for _ in range(2)],
                "has_competitive_mention": False,
                "has_booking_intent": False,
            },
        },
        {
            "name": "Competitive Mention (High Priority)",
            "context_memory": {
                "name": "Piotr",
                "phone": "+48987654321",
                "package": "Premium",
                "city": "Kraków",
            },
            "conversation_data": {
                "message_count": 6,
                "duration_minutes": 4.0,
                "messages": [
                    "Cześć",
                    "Remonteo mi powiedział że jest taniej",
                    "Ale wolę NovaHouse",
                    "Premium",
                    "+48987654321",
                    "Kraków",
                ],
                "timestamps": [datetime.now(timezone.utc) for _ in range(6)],
                "has_competitive_mention": True,
                "has_booking_intent": False,
            },
        },
    ]

    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print("-" * 70)

        # Get ML prediction
        ml_score = lead_scorer_ml.predict_score(
            test_case["context_memory"], test_case["conversation_data"]
        )

        # Get rule-based score (fallback)
        rule_score = lead_scorer_ml._fallback_rule_based_scoring(
            test_case["context_memory"], test_case["conversation_data"]
        )

        print(f"   ML Score:         {ml_score}/100")
        print(f"   Rule-based Score: {rule_score}/100")
        print(f"   Difference:       {abs(ml_score - rule_score)} points")

        # Context summary
        context = test_case["context_memory"]
        print(f"   Context: {len(context)} fields")
        print(f"   Messages: {test_case['conversation_data']['message_count']}")
        print(f"   Duration: {test_case['conversation_data']['duration_minutes']:.1f} min")
        print()

    print("=" * 70)
    print("✅ TESTING COMPLETE")
    print("=" * 70)
    print()

    if lead_scorer_ml.model is None:
        print("⚠️  ML model not loaded. Train it first:")
        print("   python3 scripts/train_lead_scoring_model.py")
    else:
        print("✅ ML model is loaded and working!")
        print()
        print("🎯 Feature importance:")
        if hasattr(lead_scorer_ml.model, "feature_importances_"):
            importances = lead_scorer_ml.model.feature_importances_
            feature_importance = [
                (name, imp) for name, imp in zip(lead_scorer_ml.feature_names, importances)
            ]
            feature_importance.sort(key=lambda x: x[1], reverse=True)

            for name, importance in feature_importance[:5]:
                print(f"   {name}: {importance:.2%}")


if __name__ == "__main__":
    test_ml_scoring()
