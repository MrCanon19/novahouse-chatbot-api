"""
ML-Based Lead Scoring
Predictive model trained on historical conversation data
"""

import json
import logging
import os
import pickle
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.warning("numpy not available - ML scoring disabled, using rule-based fallback")


class LeadScoringML:
    """
    Machine Learning based lead scoring
    Predicts conversion probability based on conversation features
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path or "models/lead_scoring_model.pkl"
        self.feature_names = [
            "message_count",
            "conversation_duration_minutes",
            "has_email",
            "has_phone",
            "has_name",
            "has_package",
            "has_square_meters",
            "has_city",
            "response_speed_avg",
            "question_marks_count",
            "exclamation_marks_count",
            "word_count_avg",
            "competitive_mention",
            "booking_intent_detected",
        ]

        # Try to load existing model (only if numpy available)
        if NUMPY_AVAILABLE and os.path.exists(self.model_path):
            self.load_model()

    def extract_features(self, context_memory: Dict, conversation_data: Dict) -> List:
        """
        Extract features from conversation for ML prediction

        Args:
            context_memory: Context data (name, email, phone, etc.)
            conversation_data: {
                'message_count': int,
                'duration_minutes': float,
                'messages': List[str],
                'timestamps': List[datetime],
                'has_competitive_mention': bool,
                'has_booking_intent': bool
            }

        Returns:
            List of features (converted to numpy array internally if available)
        """
        features = []

        # Message count
        features.append(conversation_data.get("message_count", 0))

        # Conversation duration
        features.append(conversation_data.get("duration_minutes", 0))

        # Data completeness (binary features)
        features.append(1 if context_memory.get("email") else 0)
        features.append(1 if context_memory.get("phone") else 0)
        features.append(1 if context_memory.get("name") else 0)
        features.append(1 if context_memory.get("package") else 0)
        features.append(1 if context_memory.get("square_meters") else 0)
        features.append(1 if context_memory.get("city") else 0)

        # Response speed (average time between messages)
        timestamps = conversation_data.get("timestamps", [])
        if len(timestamps) > 1:
            diffs = [
                (timestamps[i + 1] - timestamps[i]).total_seconds()
                for i in range(len(timestamps) - 1)
            ]
            avg_response_time = sum(diffs) / len(diffs) if diffs else 0
        else:
            avg_response_time = 0
        features.append(avg_response_time)

        # Engagement signals
        messages = conversation_data.get("messages", [])
        all_text = " ".join(messages)
        features.append(all_text.count("?"))  # Question marks
        features.append(all_text.count("!"))  # Exclamation marks

        # Word count average
        if messages:
            word_counts = [len(msg.split()) for msg in messages]
            avg_word_count = sum(word_counts) / len(word_counts)
        else:
            avg_word_count = 0
        features.append(avg_word_count)

        # Intent signals
        features.append(1 if conversation_data.get("has_competitive_mention", False) else 0)
        features.append(1 if conversation_data.get("has_booking_intent", False) else 0)

        # Convert to numpy array only if available
        if NUMPY_AVAILABLE:
            return np.array(features).reshape(1, -1)
        else:
            return [features]  # Return as list of lists for compatibility

    def predict_score(self, context_memory: Dict, conversation_data: Dict) -> int:
        """
        Predict lead score using ML model

        Returns:
            Lead score (0-100)
        """
        if not NUMPY_AVAILABLE or self.model is None:
            # Fallback to rule-based scoring
            if not NUMPY_AVAILABLE:
                logger.warning("numpy not available, using rule-based fallback")
            else:
                logger.info("Model not loaded, using rule-based fallback")
            return self._fallback_rule_based_scoring(context_memory, conversation_data)

        try:
            # Extract features
            features = self.extract_features(context_memory, conversation_data)

            # Predict probability
            if hasattr(self.model, "predict_proba"):
                # Classification model (RandomForest, XGBoost)
                proba = self.model.predict_proba(features)[0][1]  # Probability of class 1
                score = int(proba * 100)
            else:
                # Regression model
                score = int(self.model.predict(features)[0])

            # Clip to valid range
            score = max(0, min(100, score))

            logger.info(f"Predicted score: {score}/100")
            return score

        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return self._fallback_rule_based_scoring(context_memory, conversation_data)

    def _fallback_rule_based_scoring(self, context_memory: Dict, conversation_data: Dict) -> int:
        """
        Rule-based scoring as fallback when ML model unavailable
        This is the original algorithm
        """
        score = 0

        # Data completeness (40 points)
        if context_memory.get("name"):
            score += 10
        if context_memory.get("email"):
            score += 15
        if context_memory.get("phone"):
            score += 15

        # Intent signals (30 points)
        if context_memory.get("package"):
            score += 15
        if context_memory.get("square_meters"):
            score += 10
        if context_memory.get("city"):
            score += 5

        # Engagement (30 points)
        message_count = conversation_data.get("message_count", 0)
        if message_count >= 5:
            score += 20
        elif message_count >= 3:
            score += 10

        duration = conversation_data.get("duration_minutes", 0)
        if duration >= 5:
            score += 10
        elif duration >= 2:
            score += 5

        return min(100, score)

    def train_model(self, training_data: List[Dict]):
        """
        Train ML model on historical data

        Args:
            training_data: List of dicts with:
                - context_memory
                - conversation_data
                - actual_converted (bool) - whether lead converted
        """
        if not NUMPY_AVAILABLE:
            logger.warning("numpy/scikit-learn not available, cannot train model")
            return False

        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split

            logger.info(f"Training on {len(training_data)} samples...")

            # Extract features and labels
            X = []
            y = []

            for sample in training_data:
                features = self.extract_features(
                    sample["context_memory"], sample["conversation_data"]
                )
                X.append(features[0])
                y.append(1 if sample.get("actual_converted", False) else 0)

            X = np.array(X)
            y = np.array(y)

            if len(X) < 10:
                logger.warning("Not enough data (<10 samples), skipping training")
                return False

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Train RandomForest
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
            )

            self.model.fit(X_train, y_train)

            # Evaluate
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)

            logger.info(f"Train accuracy: {train_score:.2%}")
            logger.info(f"Test accuracy: {test_score:.2%}")

            # Feature importance
            importances = self.model.feature_importances_
            for i, importance in enumerate(importances):
                if importance > 0.05:  # Show only important features
                    logger.info(f"{self.feature_names[i]}: {importance:.2%}")

            # Save model
            self.save_model()

            return True

        except ImportError:
            logger.error("scikit-learn not installed. Run: pip install scikit-learn")
            return False
        except Exception as e:
            logger.error(f"Training error: {e}", exc_info=True)
            return False

    def save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, "wb") as f:
                pickle.dump(self.model, f)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Model save failed: {e}", exc_info=True)

    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.warning(f"Model load failed: {e}")
            self.model = None

    def collect_training_data_from_db(self) -> List[Dict]:
        """
        Collect training data from database

        Returns:
            List of training samples
        """
        try:
            from src.models.chatbot import ChatConversation, ChatMessage, Lead

            training_data = []

            # Get all leads (these are conversions)
            leads = Lead.query.filter(Lead.data_confirmed.is_(True)).all()

            logger.info(f"Found {len(leads)} confirmed leads")

            for lead in leads:
                # Get conversation
                conversation = ChatConversation.query.filter_by(session_id=lead.session_id).first()

                if not conversation:
                    continue

                # Get messages
                messages = (
                    ChatMessage.query.filter_by(conversation_id=conversation.id)
                    .order_by(ChatMessage.timestamp.asc())
                    .all()
                )

                if len(messages) < 2:
                    continue

                # Extract context
                context_memory = json.loads(conversation.context_data or "{}")

                # Build conversation data
                user_messages = [msg.message for msg in messages if msg.sender == "user"]
                timestamps = [msg.timestamp for msg in messages]

                duration = (timestamps[-1] - timestamps[0]).total_seconds() / 60.0

                # Check competitive intel mentions
                from src.models.chatbot import CompetitiveIntel

                has_competitive = (
                    CompetitiveIntel.query.filter_by(session_id=lead.session_id).first() is not None
                )

                conversation_data = {
                    "message_count": len(messages),
                    "duration_minutes": duration,
                    "messages": user_messages,
                    "timestamps": timestamps,
                    "has_competitive_mention": has_competitive,
                    "has_booking_intent": any("zencal" in msg.message.lower() for msg in messages),
                }

                training_data.append(
                    {
                        "context_memory": context_memory,
                        "conversation_data": conversation_data,
                        "actual_converted": True,  # It's a confirmed lead
                    }
                )

            # Add negative examples (conversations without leads)
            conversations_without_leads = (
                ChatConversation.query.outerjoin(
                    Lead, Lead.session_id == ChatConversation.session_id
                )
                .filter(Lead.id.is_(None))
                .filter(ChatConversation.ended_at.isnot(None))
                .limit(len(training_data))  # Balance positive/negative examples
                .all()
            )

            for conv in conversations_without_leads:
                messages = ChatMessage.query.filter_by(conversation_id=conv.id).all()
                if messages:
                    context_memory = json.loads(conv.context_data or "{}")
                    user_messages = [msg.message for msg in messages if msg.sender == "user"]
                    timestamps = [msg.timestamp for msg in messages]
                    duration = (timestamps[-1] - timestamps[0]).total_seconds() / 60.0

                    conversation_data = {
                        "message_count": len(messages),
                        "duration_minutes": duration,
                        "messages": user_messages,
                        "timestamps": timestamps,
                        "has_competitive_mention": False,
                        "has_booking_intent": False,
                    }

                    training_data.append(
                        {
                            "context_memory": context_memory,
                            "conversation_data": conversation_data,
                            "actual_converted": False,  # No lead created
                        }
                    )

            logger.info(f"Collected {len(training_data)} training samples")
            return training_data

        except Exception as e:
            logger.error(f"Data collection error: {e}", exc_info=True)
            return []


# Global instance
lead_scorer_ml = LeadScoringML()
