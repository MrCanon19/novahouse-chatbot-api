"""
Advanced Analytics Service
===========================
Sentiment analysis, heatmaps, funnels, cohort analysis
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from src.models.chatbot import db
from src.models.analytics import ChatAnalytics
from src.models.chatbot import Lead
from collections import defaultdict
from typing import Dict, Any


class AdvancedAnalytics:
    """Advanced analytics service with ML capabilities"""

    @staticmethod
    def analyze_sentiment(message: str) -> Dict[str, Any]:
        """
        Simple sentiment analysis based on keywords
        For production, use Google Cloud Natural Language API or similar

        Returns:
            dict: {
                'sentiment': 'positive'|'negative'|'neutral',
                'score': float (-1.0 to 1.0),
                'confidence': float (0.0 to 1.0)
            }
        """
        # Positive keywords (Polish)
        positive_words = [
            "super",
            "świetnie",
            "doskonale",
            "fantastycznie",
            "rewelacja",
            "pięknie",
            "profesjonalnie",
            "polecam",
            "zadowolony",
            "zachwycony",
            "dziękuję",
            "dzięki",
            "wow",
            "idealnie",
            "perfekcyjnie",
            "tak",
            "dobry",
            "świetny",
            "excellent",
            "great",
            "good",
        ]

        # Negative keywords (Polish)
        negative_words = [
            "źle",
            "kiepsko",
            "nie",
            "słabo",
            "okropnie",
            "tragedia",
            "beznadziejnie",
            "rozczarowany",
            "niezadowolony",
            "problem",
            "błąd",
            "awaria",
            "pomyłka",
            "zły",
            "bad",
            "poor",
            "terrible",
        ]

        message_lower = message.lower()

        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)

        # Calculate score (-1.0 to 1.0)
        total_words = len(message_lower.split())
        if total_words == 0:
            return {"sentiment": "neutral", "score": 0.0, "confidence": 0.0}

        score = (positive_count - negative_count) / max(total_words, 1)
        score = max(-1.0, min(1.0, score))  # Clamp to [-1, 1]

        # Determine sentiment
        if score > 0.1:
            sentiment = "positive"
        elif score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Calculate confidence
        confidence = min(abs(score) * 2, 1.0)

        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "confidence": round(confidence, 3),
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
        }

    @staticmethod
    def get_activity_heatmap(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Generate activity heatmap by day of week and hour

        Returns:
            dict: {
                'heatmap': [[hour0_mon, hour0_tue, ...], [hour1_mon, ...]],
                'peak_hours': [(hour, count), ...],
                'peak_days': [(day, count), ...]
            }
        """
        # Query all interactions in date range
        interactions = (
            db.session.query(
                func.extract("dow", ChatAnalytics.timestamp).label("day_of_week"),
                func.extract("hour", ChatAnalytics.timestamp).label("hour"),
                func.count(ChatAnalytics.id).label("count"),
            )
            .filter(ChatAnalytics.timestamp >= start_date, ChatAnalytics.timestamp <= end_date)
            .group_by("day_of_week", "hour")
            .all()
        )

        # Initialize heatmap (24 hours x 7 days)
        heatmap = [[0 for _ in range(7)] for _ in range(24)]

        # Fill heatmap
        for day, hour, count in interactions:
            # PostgreSQL: Sunday=0, Monday=1, ..., Saturday=6
            # We want: Monday=0, ..., Sunday=6
            day_idx = (int(day) - 1) % 7
            hour_idx = int(hour)
            heatmap[hour_idx][day_idx] = count

        # Calculate peak hours (aggregate across all days)
        hour_totals = defaultdict(int)
        for interaction in interactions:
            hour_totals[int(interaction.hour)] += interaction.count

        peak_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)[:5]

        # Calculate peak days
        day_totals = defaultdict(int)
        day_names = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Ndz"]
        for interaction in interactions:
            day_idx = (int(interaction.day_of_week) - 1) % 7
            day_totals[day_names[day_idx]] += interaction.count

        peak_days = sorted(day_totals.items(), key=lambda x: x[1], reverse=True)

        return {
            "heatmap": heatmap,
            "peak_hours": [{"hour": h, "count": c} for h, c in peak_hours],
            "peak_days": [{"day": d, "count": c} for d, c in peak_days],
            "total_interactions": sum(c for _, _, c in interactions),
        }

    @staticmethod
    def get_conversion_funnel(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Analyze conversion funnel from first message to lead

        Stages:
        1. Initial Contact (first message)
        2. Engagement (3+ messages)
        3. Interest (asked about pricing/services)
        4. Intent (requested contact/booking)
        5. Conversion (submitted lead form)

        Returns:
            dict: {
                'stages': [
                    {'name': 'Initial Contact', 'count': 1000, 'percentage': 100},
                    {'name': 'Engagement', 'count': 450, 'percentage': 45},
                    ...
                ],
                'drop_off_rates': {...},
                'avg_time_between_stages': {...}
            }
        """
        # Stage 1: All unique sessions
        total_sessions = (
            db.session.query(func.count(func.distinct(ChatAnalytics.session_id)))
            .filter(ChatAnalytics.timestamp >= start_date, ChatAnalytics.timestamp <= end_date)
            .scalar()
            or 0
        )

        # Stage 2: Engaged users (3+ messages)
        engaged_users = (
            db.session.query(func.count(func.distinct(ChatAnalytics.session_id)))
            .filter(
                ChatAnalytics.timestamp >= start_date,
                ChatAnalytics.timestamp <= end_date,
                ChatAnalytics.message_count >= 3,
            )
            .scalar()
            or 0
        )

        # Stage 3: Showed interest (pricing/services intents)
        interested_users = (
            db.session.query(func.count(func.distinct(ChatAnalytics.session_id)))
            .filter(
                ChatAnalytics.timestamp >= start_date,
                ChatAnalytics.timestamp <= end_date,
                ChatAnalytics.intent_detected.in_(["pricing", "services", "portfolio"]),
            )
            .scalar()
            or 0
        )

        # Stage 4: Showed intent (contact/booking intents)
        intent_users = (
            db.session.query(func.count(func.distinct(ChatAnalytics.session_id)))
            .filter(
                ChatAnalytics.timestamp >= start_date,
                ChatAnalytics.timestamp <= end_date,
                ChatAnalytics.intent_detected.in_(["contact", "booking"]),
            )
            .scalar()
            or 0
        )

        # Stage 5: Converted (lead generated)
        converted_users = (
            db.session.query(func.count(func.distinct(Lead.id)))
            .filter(Lead.created_at >= start_date, Lead.created_at <= end_date)
            .scalar()
            or 0
        )

        # Calculate percentages and drop-off rates
        stages = [
            {"name": "Initial Contact", "count": total_sessions, "percentage": 100.0},
            {
                "name": "Engagement (3+ messages)",
                "count": engaged_users,
                "percentage": round(
                    (engaged_users / total_sessions * 100) if total_sessions > 0 else 0, 2
                ),
            },
            {
                "name": "Interest (pricing/services)",
                "count": interested_users,
                "percentage": round(
                    (interested_users / total_sessions * 100) if total_sessions > 0 else 0, 2
                ),
            },
            {
                "name": "Intent (contact/booking)",
                "count": intent_users,
                "percentage": round(
                    (intent_users / total_sessions * 100) if total_sessions > 0 else 0, 2
                ),
            },
            {
                "name": "Conversion (lead)",
                "count": converted_users,
                "percentage": round(
                    (converted_users / total_sessions * 100) if total_sessions > 0 else 0, 2
                ),
            },
        ]

        # Calculate drop-off rates between stages
        drop_off_rates = []
        for i in range(len(stages) - 1):
            current = stages[i]["count"]
            next_stage = stages[i + 1]["count"]
            if current > 0:
                drop_off = round(((current - next_stage) / current * 100), 2)
                drop_off_rates.append(
                    {
                        "from": stages[i]["name"],
                        "to": stages[i + 1]["name"],
                        "drop_off_percentage": drop_off,
                        "users_lost": current - next_stage,
                    }
                )

        return {
            "stages": stages,
            "drop_off_rates": drop_off_rates,
            "overall_conversion_rate": stages[-1]["percentage"],
            "total_sessions": total_sessions,
            "total_conversions": converted_users,
        }

    @staticmethod
    def get_cohort_analysis(
        cohort_period: str = "week", num_cohorts: int = 8  # 'day', 'week', 'month'
    ) -> Dict[str, Any]:
        """
        Cohort retention analysis
        Groups users by signup date and tracks their return rate

        Returns:
            dict: {
                'cohorts': [
                    {
                        'cohort_date': '2025-01-01',
                        'users': 100,
                        'retention': [100, 45, 32, 28, ...]  # % returning in each period
                    },
                    ...
                ]
            }
        """
        now = datetime.now(timezone.utc)

        # Determine period length
        if cohort_period == "day":
            period_delta = timedelta(days=1)
            date_trunc = "day"
        elif cohort_period == "week":
            period_delta = timedelta(weeks=1)
            date_trunc = "week"
        else:  # month
            period_delta = timedelta(days=30)
            date_trunc = "month"

        # Get first interaction date for each user (cohort assignment)
        cohort_query = (
            db.session.query(
                ChatAnalytics.user_id,
                func.date_trunc(date_trunc, func.min(ChatAnalytics.timestamp)).label("cohort_date"),
            )
            .filter(ChatAnalytics.timestamp >= now - (period_delta * num_cohorts))
            .group_by(ChatAnalytics.user_id)
            .subquery()
        )

        # Get all user interactions with their cohort date
        interactions = (
            db.session.query(
                cohort_query.c.user_id,
                cohort_query.c.cohort_date,
                func.date_trunc(date_trunc, ChatAnalytics.timestamp).label("interaction_date"),
            )
            .join(ChatAnalytics, ChatAnalytics.user_id == cohort_query.c.user_id)
            .all()
        )

        # Build cohort retention data
        cohort_data = defaultdict(lambda: {"users": set(), "retention_periods": defaultdict(set)})

        for user_id, cohort_date, interaction_date in interactions:
            cohort_key = cohort_date.strftime("%Y-%m-%d")
            cohort_data[cohort_key]["users"].add(user_id)

            # Calculate period number (0 = cohort period, 1 = next period, etc.)
            period_num = int(
                (interaction_date - cohort_date).total_seconds() / period_delta.total_seconds()
            )
            cohort_data[cohort_key]["retention_periods"][period_num].add(user_id)

        # Format results
        cohorts = []
        for cohort_date in sorted(cohort_data.keys(), reverse=True):
            data = cohort_data[cohort_date]
            total_users = len(data["users"])

            # Calculate retention percentages for each period
            retention = []
            max_period = max(data["retention_periods"].keys()) if data["retention_periods"] else 0

            for period in range(max_period + 1):
                returning_users = len(data["retention_periods"].get(period, set()))
                retention_pct = round(
                    (returning_users / total_users * 100) if total_users > 0 else 0, 2
                )
                retention.append(retention_pct)

            cohorts.append(
                {"cohort_date": cohort_date, "users": total_users, "retention": retention}
            )

        return {
            "cohorts": cohorts[:num_cohorts],
            "period": cohort_period,
            "num_periods": num_cohorts,
        }

    @staticmethod
    def get_user_journey_insights(session_id: str) -> Dict[str, Any]:
        """
        Analyze individual user journey through the chatbot

        Returns:
            dict: {
                'session_id': str,
                'messages': int,
                'duration_seconds': int,
                'intents_timeline': [...],
                'sentiment_trend': [...],
                'conversion_probability': float,
                'recommendations': [str, ...]
            }
        """
        # Get all messages for this session
        messages = (
            ChatAnalytics.query.filter_by(session_id=session_id)
            .order_by(ChatAnalytics.timestamp)
            .all()
        )

        if not messages:
            return {"error": "Session not found"}

        # Calculate session duration
        first_msg = messages[0].timestamp
        last_msg = messages[-1].timestamp
        duration = (last_msg - first_msg).total_seconds()

        # Build intents timeline
        intents_timeline = []
        sentiment_trend = []

        for msg in messages:
            intents_timeline.append(
                {
                    "timestamp": msg.timestamp.isoformat(),
                    "intent": msg.intent_detected,
                    "message_count": msg.message_count,
                }
            )

            if msg.sentiment:
                sentiment_trend.append(
                    {"timestamp": msg.timestamp.isoformat(), "sentiment": msg.sentiment}
                )

        # Calculate conversion probability based on patterns
        conversion_score = 0

        # Check for positive signals
        if len(messages) >= 5:
            conversion_score += 20
        if any(msg.intent_detected in ["pricing", "services"] for msg in messages):
            conversion_score += 25
        if any(msg.intent_detected in ["contact", "booking"] for msg in messages):
            conversion_score += 35
        if any(msg.sentiment == "positive" for msg in messages):
            conversion_score += 15
        if duration > 60:  # More than 1 minute
            conversion_score += 5

        conversion_score = min(100, conversion_score)

        # Generate recommendations
        recommendations = []
        if conversion_score >= 70:
            recommendations.append(
                "High conversion probability - follow up with personalized offer"
            )
        elif conversion_score >= 40:
            recommendations.append("Moderate interest - send additional portfolio examples")
        else:
            recommendations.append("Low engagement - consider A/B testing different responses")

        if not any(msg.intent_detected == "pricing" for msg in messages):
            recommendations.append("User hasn't asked about pricing - could be a barrier")

        if duration < 30:
            recommendations.append("Short session - improve initial engagement")

        return {
            "session_id": session_id,
            "total_messages": len(messages),
            "duration_seconds": int(duration),
            "intents_timeline": intents_timeline,
            "sentiment_trend": sentiment_trend,
            "conversion_probability": conversion_score,
            "recommendations": recommendations,
            "first_interaction": first_msg.isoformat(),
            "last_interaction": last_msg.isoformat(),
        }
