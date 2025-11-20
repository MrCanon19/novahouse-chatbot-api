"""
Real-time Sentiment Analysis Service
Integrates with message handler for emotion detection and auto-escalation
"""

from typing import Dict, Optional, Tuple

from src.services.analytics_service import AdvancedAnalytics


class SentimentService:
    """Real-time sentiment analysis for chatbot conversations"""

    # Sentiment thresholds
    NEGATIVE_THRESHOLD = -0.3  # Below this = frustrated/angry
    POSITIVE_THRESHOLD = 0.2  # Above this = happy/satisfied

    # Escalation rules
    MAX_NEGATIVE_STREAK = 2  # Escalate after 2 negative messages in a row
    CRITICAL_SCORE = -0.6  # Immediate escalation threshold

    def __init__(self):
        self.analytics = AdvancedAnalytics()
        self.session_sentiments = {}  # Track sentiment history per session

    def analyze_message_sentiment(self, message: str, session_id: str) -> Dict:
        """
        Analyze sentiment of user message in real-time

        Args:
            message: User's message text
            session_id: Session identifier

        Returns:
            dict with sentiment analysis and escalation recommendation
        """
        # Get sentiment from analytics service
        sentiment_data = self.analytics.analyze_sentiment(message)

        # Track sentiment history
        if session_id not in self.session_sentiments:
            self.session_sentiments[session_id] = []

        self.session_sentiments[session_id].append(
            {"sentiment": sentiment_data["sentiment"], "score": sentiment_data["score"]}
        )

        # Keep only last 5 messages
        if len(self.session_sentiments[session_id]) > 5:
            self.session_sentiments[session_id].pop(0)

        # Check if escalation needed
        should_escalate, escalation_reason = self._check_escalation(session_id, sentiment_data)

        # Adjust response tone
        response_tone = self._determine_response_tone(sentiment_data)

        return {
            "sentiment": sentiment_data["sentiment"],
            "score": sentiment_data["score"],
            "confidence": sentiment_data["confidence"],
            "should_escalate": should_escalate,
            "escalation_reason": escalation_reason,
            "response_tone": response_tone,
            "sentiment_trend": self._get_sentiment_trend(session_id),
        }

    def _check_escalation(
        self, session_id: str, current_sentiment: Dict
    ) -> Tuple[bool, Optional[str]]:
        """Check if human escalation is needed"""
        score = current_sentiment["score"]

        # Critical score - immediate escalation
        if score <= self.CRITICAL_SCORE:
            return True, "critical_frustration"

        # Check for negative streak
        history = self.session_sentiments.get(session_id, [])
        if len(history) >= self.MAX_NEGATIVE_STREAK:
            recent = history[-self.MAX_NEGATIVE_STREAK :]
            if all(s["score"] < self.NEGATIVE_THRESHOLD for s in recent):
                return True, "negative_streak"

        return False, None

    def _determine_response_tone(self, sentiment_data: Dict) -> str:
        """Determine appropriate bot response tone based on sentiment"""
        score = sentiment_data["score"]

        if score >= self.POSITIVE_THRESHOLD:
            return "enthusiastic"  # Match positive energy
        elif score <= self.NEGATIVE_THRESHOLD:
            return "empathetic"  # Be understanding and helpful
        else:
            return "neutral"  # Professional and informative

    def _get_sentiment_trend(self, session_id: str) -> str:
        """Get sentiment trend over conversation"""
        history = self.session_sentiments.get(session_id, [])

        if len(history) < 2:
            return "stable"

        recent_scores = [s["score"] for s in history[-3:]]

        # Calculate trend
        if len(recent_scores) >= 2:
            trend = recent_scores[-1] - recent_scores[0]
            if trend > 0.2:
                return "improving"
            elif trend < -0.2:
                return "declining"

        return "stable"

    def get_empathetic_response_prefix(self, sentiment: str, score: float) -> str:
        """Get empathetic response prefix based on sentiment"""
        if sentiment == "negative" and score < -0.4:
            return "Rozumiem Twoją frustrację. "
        elif sentiment == "negative":
            return "Przykro mi, że masz wątpliwości. "
        elif sentiment == "positive":
            return "Cieszę się, że mogę pomóc! "
        else:
            return ""

    def adjust_lead_score_by_sentiment(self, base_score: int, session_id: str) -> int:
        """Adjust lead score based on sentiment trend"""
        history = self.session_sentiments.get(session_id, [])

        if not history:
            return base_score

        # Calculate average sentiment
        avg_sentiment = sum(s["score"] for s in history) / len(history)

        # Adjust score
        if avg_sentiment >= 0.3:
            return min(base_score + 15, 100)  # Very positive = +15
        elif avg_sentiment >= 0.1:
            return min(base_score + 5, 100)  # Positive = +5
        elif avg_sentiment <= -0.3:
            return max(base_score - 15, 0)  # Negative = -15
        elif avg_sentiment <= -0.1:
            return max(base_score - 5, 0)  # Slightly negative = -5

        return base_score


# Global instance
sentiment_service = SentimentService()
