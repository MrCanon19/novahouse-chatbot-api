#!/usr/bin/env python3
"""
Train ML Lead Scoring Model
Collects historical data and trains RandomForest classifier
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.lead_scoring_ml import lead_scorer_ml


def main():
    print("=" * 70)
    print("🤖 ML LEAD SCORING MODEL TRAINING")
    print("=" * 70)
    print()

    # Step 1: Collect training data from database
    print("📊 Step 1: Collecting training data from database...")
    training_data = lead_scorer_ml.collect_training_data_from_db()

    if len(training_data) == 0:
        print("❌ No training data found!")
        print("   Make sure you have confirmed leads in the database.")
        return

    print(f"✅ Collected {len(training_data)} training samples")
    print()

    # Step 2: Train model
    print("🎯 Step 2: Training RandomForest model...")
    success = lead_scorer_ml.train_model(training_data)

    if not success:
        print("❌ Training failed!")
        return

    print()
    print("=" * 70)
    print("✅ MODEL TRAINING COMPLETE")
    print("=" * 70)
    print()
    print("📁 Model saved to: models/lead_scoring_model.pkl")
    print()
    print("🚀 Next steps:")
    print("   1. Test the model: python3 scripts/test_lead_scoring.py")
    print("   2. Deploy to GAE: gcloud app deploy")
    print()


if __name__ == "__main__":
    main()
