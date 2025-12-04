"""
Enhanced Lead Scoring Service

Advanced scoring with behavioral analysis, package boost, time decay.
Complements ML model with rule-based enhancements.
"""

from datetime import datetime, timezone
from typing import Dict

from src.models.chatbot import Lead


class EnhancedLeadScoringService:
    """Service for enhanced lead scoring with behavioral analysis"""

    # Scoring weights (0-100 scale)
    PACKAGE_WEIGHT = 0.15  # Premium package gets boost
    BEHAVIOR_WEIGHT = 0.20  # Sentiment, engagement velocity
    DATA_WEIGHT = 0.35  # Data completeness
    DECAY_WEIGHT = 0.30  # Time decay for old leads

    # Package scoring modifiers
    PACKAGE_SCORES = {
        "basic": 0,
        "standard": 5,
        "premium": 15,
        "express": 20,
    }

    # Behavior scoring modifiers
    SENTIMENT_SCORES = {
        "very_positive": 10,
        "positive": 5,
        "neutral": 0,
        "negative": -5,
        "very_negative": -10,
    }

    @classmethod
    def calculate_enhanced_score(
        cls,
        lead: Lead,
        base_score: int,
        context_memory: Dict,
        conversation_data: Dict = None,
    ) -> int:
        """
        Calculate enhanced lead score with all modifiers

        Args:
            lead: Lead object
            base_score: Base ML/rule-based score (0-100)
            context_memory: Context data
            conversation_data: Optional conversation data

        Returns:
            Enhanced score (0-100)
        """
        score = base_score

        # Apply package modifier
        package_modifier = cls._get_package_modifier(context_memory.get("package"))
        score += package_modifier

        # Apply behavioral modifier
        if conversation_data:
            behavior_modifier = cls._get_behavior_modifier(conversation_data)
            score += behavior_modifier

        # Apply time decay modifier
        time_modifier = cls._get_time_decay_modifier(lead.created_at)
        score += time_modifier

        # Apply verification bonus
        if lead.email_verified or lead.phone_verified:
            score += 15

        # Apply data completeness bonus
        completeness_bonus = cls._get_data_completeness_bonus(context_memory)
        score += completeness_bonus

        # Clamp score to 0-100
        return max(0, min(100, score))

    @staticmethod
    def _get_package_modifier(package: str) -> int:
        """
        Get score modifier based on package choice

        Higher tier packages = higher score (more likely to convert)
        """
        package_lower = (package or "basic").lower()

        return EnhancedLeadScoringService.PACKAGE_SCORES.get(package_lower, 0)

    @staticmethod
    def _get_behavior_modifier(conversation_data: Dict) -> int:
        """
        Get score modifier based on conversation behavior

        Factors:
        - Message sentiment
        - Response speed
        - Number of questions asked
        - Message quality (word count)
        """
        modifier = 0

        # Sentiment analysis
        sentiment = conversation_data.get("sentiment", "neutral")
        sentiment_scores = EnhancedLeadScoringService.SENTIMENT_SCORES
        modifier += sentiment_scores.get(sentiment, 0)

        # Response velocity (faster = more engaged)
        avg_response_time = conversation_data.get("avg_response_time", 0)
        if avg_response_time > 0:
            # Fast responses (< 30 seconds) = good engagement
            if avg_response_time < 30:
                modifier += 10
            elif avg_response_time < 60:
                modifier += 5

        # Question count (curiosity = interest)
        question_count = conversation_data.get("question_count", 0)
        if question_count >= 5:
            modifier += 10
        elif question_count >= 3:
            modifier += 5

        # Message quality (average word count)
        avg_word_count = conversation_data.get("avg_word_count", 0)
        if avg_word_count >= 20:  # Thoughtful messages
            modifier += 5

        return modifier

    @staticmethod
    def _get_time_decay_modifier(created_at) -> int:
        """
        Apply time decay modifier

        Fresh leads (< 24 hours) = higher score
        Old leads (> 7 days) = lower score
        """
        if not created_at:
            return 0

        age_days = (datetime.now(timezone.utc) - created_at).days

        if age_days <= 1:
            return 5  # Fresh lead boost
        elif age_days <= 3:
            return 0  # No penalty
        elif age_days <= 7:
            return -5  # Slight decay
        else:
            return -10  # Significant decay for old leads

    @staticmethod
    def _get_data_completeness_bonus(context_memory: Dict) -> int:
        """
        Bonus for data completeness

        Full data = higher score
        Minimal data = lower score
        """
        bonus = 0
        data_points = 0
        max_data_points = 6

        required_fields = [
            "name",
            "email",
            "phone",
            "city",
            "square_meters",
            "package",
        ]

        for field in required_fields:
            if context_memory.get(field):
                data_points += 1

        # 6/6 fields = +10 bonus
        # 5/6 fields = +5 bonus
        # 4/6 fields = 0 bonus
        # < 4 fields = -5 penalty

        if data_points == max_data_points:
            bonus = 10
        elif data_points == max_data_points - 1:
            bonus = 5
        elif data_points < max_data_points - 2:
            bonus = -5

        return bonus

    @staticmethod
    def get_score_explanation(
        lead: Lead,
        score: int,
        base_score: int,
    ) -> str:
        """
        Get human-readable explanation of score

        Helps sales team understand lead quality
        """
        if score >= 80:
            status = "🔴 CRITICAL - Contact immediately"
            reason = "Very high quality lead with strong buying signals"
        elif score >= 60:
            status = "🟠 HIGH - Priority contact"
            reason = "Good quality lead, likely to convert"
        elif score >= 40:
            status = "🟡 MEDIUM - Follow up"
            reason = "Moderate quality lead, worth pursuing"
        elif score >= 20:
            status = "🔵 LOW - Keep in database"
            reason = "Lower quality but potential interest"
        else:
            status = "⚪ VERY LOW - Monitor"
            reason = "Minimal signals, nurture in time"

        modifiers = []
        if lead.email_verified or lead.phone_verified:
            modifiers.append("✅ Verified contact")
        if lead.interested_package and lead.interested_package.lower() in ["premium", "express"]:
            modifiers.append("💎 Premium package choice")
        if lead.created_at and (datetime.now(timezone.utc) - lead.created_at).days <= 1:
            modifiers.append("⭐ Fresh lead")

        explanation = f"{status}\n{reason}"
        if modifiers:
            explanation += "\n" + " | ".join(modifiers)

        return explanation

    @staticmethod
    def get_recommended_action(score: int) -> str:
        """Get recommended action based on score"""
        if score >= 80:
            return "Call immediately"
        elif score >= 60:
            return "Schedule call/meeting"
        elif score >= 40:
            return "Send proposal"
        elif score >= 20:
            return "Follow up email"
        else:
            return "Add to nurture campaign"


# Singleton instance
enhanced_lead_scoring = EnhancedLeadScoringService()
