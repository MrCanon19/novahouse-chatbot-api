#!/usr/bin/env python3
"""
Test: Aplikacja startuje bez numpy/scikit-learn
"""

import os
import sys

# Symuluj brak numpy/scikit-learn
sys.modules["numpy"] = None
sys.modules["sklearn"] = None
sys.modules["sklearn.ensemble"] = None
sys.modules["sklearn.model_selection"] = None

print("🔍 Test: Import lead_scoring_ml bez numpy...")

try:
    # Dodaj src do path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    from src.services.lead_scoring_ml import NUMPY_AVAILABLE, lead_scorer_ml

    if NUMPY_AVAILABLE:
        print("❌ FAIL: NUMPY_AVAILABLE powinno być False")
        sys.exit(1)

    print("✅ PASS: NUMPY_AVAILABLE = False")
    print(f"✅ PASS: lead_scorer_ml zainicjalizowany: {lead_scorer_ml is not None}")

    # Test predict_score (powinien użyć fallback)
    context = {"email": "test@example.com", "phone": "+48123456789", "name": "Test User"}

    conversation = {
        "message_count": 5,
        "duration_minutes": 10,
        "messages": ["test"],
        "timestamps": [],
        "has_competitive_mention": False,
        "has_booking_intent": True,
    }

    score = lead_scorer_ml.predict_score(context, conversation)

    if 0 <= score <= 100:
        print(f"✅ PASS: predict_score zwrócił poprawny wynik: {score}/100")
    else:
        print(f"❌ FAIL: predict_score zwrócił niepoprawny wynik: {score}")
        sys.exit(1)

    print("\n🎉 Wszystkie testy przeszły! Aplikacja działa bez numpy/scikit-learn")
    sys.exit(0)

except ImportError as e:
    print(f"❌ FAIL: ImportError podczas importu: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ FAIL: Nieoczekiwany błąd: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
