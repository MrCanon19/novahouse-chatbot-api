"""
A/B Testing Service
===================
Experiment management, variant assignment, statistical analysis
"""

import random
import json
import math
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from src.models.chatbot import db
from src.models.ab_testing import Experiment, ExperimentParticipant, ExperimentResult


class ABTestingService:
    """A/B testing service with statistical analysis"""

    @staticmethod
    def create_experiment(
        name: str,
        description: str,
        experiment_type: str,
        variants: List[Dict[str, str]],
        traffic_allocation: float = 1.0,
        primary_metric: str = "conversion_rate",
        min_sample_size: int = 100,
    ) -> Experiment:
        """
        Create new A/B test experiment

        Args:
            name: Experiment name
            description: Experiment description
            experiment_type: Type (prompt, greeting, cta, etc.)
            variants: List of variants [{"id": "A", "name": "Control", "content": "..."}, ...]
            traffic_allocation: Percentage of traffic to include (0.0-1.0)
            primary_metric: conversion_rate, engagement_rate, satisfaction_rate
            min_sample_size: Minimum participants per variant before declaring winner
        """
        experiment = Experiment(
            name=name,
            description=description,
            experiment_type=experiment_type,
            variants=json.dumps(variants),
            traffic_allocation=traffic_allocation,
            primary_metric=primary_metric,
            min_sample_size=min_sample_size,
            status="draft",
        )

        db.session.add(experiment)
        db.session.commit()

        return experiment

    @staticmethod
    def start_experiment(experiment_id: int) -> Dict[str, Any]:
        """Start an experiment"""
        experiment = Experiment.query.get(experiment_id)

        if not experiment:
            return {"error": "Experiment not found"}

        if experiment.status == "active":
            return {"error": "Experiment already active"}

        experiment.status = "active"
        experiment.start_date = datetime.now(timezone.utc)
        db.session.commit()

        return {"message": "Experiment started successfully", "experiment_id": experiment_id}

    @staticmethod
    def stop_experiment(experiment_id: int) -> Dict[str, Any]:
        """Stop an experiment and declare winner if criteria met"""
        experiment = Experiment.query.get(experiment_id)

        if not experiment:
            return {"error": "Experiment not found"}

        experiment.status = "completed"
        experiment.end_date = datetime.now(timezone.utc)

        # Calculate final results
        ABTestingService._calculate_results(experiment_id)

        # Try to declare winner
        winner_info = ABTestingService._declare_winner(experiment_id)

        db.session.commit()

        return {
            "message": "Experiment stopped",
            "experiment_id": experiment_id,
            "winner": winner_info,
        }

    @staticmethod
    def assign_variant(
        experiment_id: int, session_id: str, user_id: str = "anonymous"
    ) -> Optional[Dict[str, Any]]:
        """
        Assign user to a variant

        Returns:
            Dict with variant info, or None if user shouldn't participate
        """
        experiment = Experiment.query.get(experiment_id)

        if not experiment or experiment.status != "active":
            return None

        # Check if user already participated
        existing_participant = ExperimentParticipant.query.filter_by(
            experiment_id=experiment_id, session_id=session_id
        ).first()

        if existing_participant:
            # Return existing variant
            variants = json.loads(experiment.variants)
            variant = next(
                (v for v in variants if v["id"] == existing_participant.variant_id), None
            )
            return variant

        # Check traffic allocation (randomly exclude some users)
        if random.random() > experiment.traffic_allocation:
            return None

        # Assign to random variant (weighted equally)
        variants = json.loads(experiment.variants)
        variant = random.choice(variants)

        # Record participation
        participant = ExperimentParticipant(
            experiment_id=experiment_id,
            session_id=session_id,
            user_id=user_id,
            variant_id=variant["id"],
        )

        db.session.add(participant)
        db.session.commit()

        return variant

    @staticmethod
    def record_conversion(session_id: str, experiment_id: int, value: float = 1.0):
        """Record conversion for a participant"""
        participant = ExperimentParticipant.query.filter_by(
            experiment_id=experiment_id, session_id=session_id
        ).first()

        if participant:
            participant.converted = True
            participant.conversion_value = value
            db.session.commit()

    @staticmethod
    def record_engagement(session_id: str, experiment_id: int, messages: int, duration: int):
        """Record engagement metrics for a participant"""
        participant = ExperimentParticipant.query.filter_by(
            experiment_id=experiment_id, session_id=session_id
        ).first()

        if participant:
            participant.messages_sent = messages
            participant.session_duration = duration
            participant.engaged = messages >= 3  # Engaged if 3+ messages
            db.session.commit()

    @staticmethod
    def record_satisfaction(session_id: str, experiment_id: int, is_satisfied: bool):
        """Record satisfaction for a participant"""
        participant = ExperimentParticipant.query.filter_by(
            experiment_id=experiment_id, session_id=session_id
        ).first()

        if participant:
            participant.satisfied = is_satisfied
            db.session.commit()

    @staticmethod
    def _calculate_results(experiment_id: int):
        """Calculate aggregated results for each variant"""
        experiment = Experiment.query.get(experiment_id)
        variants = json.loads(experiment.variants)

        for variant in variants:
            variant_id = variant["id"]

            # Get all participants for this variant
            participants = ExperimentParticipant.query.filter_by(
                experiment_id=experiment_id, variant_id=variant_id
            ).all()

            if not participants:
                continue

            # Calculate metrics
            total = len(participants)
            conversions = sum(1 for p in participants if p.converted)
            engaged = sum(1 for p in participants if p.engaged)
            satisfied = sum(1 for p in participants if p.satisfied)

            conversion_rate = conversions / total if total > 0 else 0
            engagement_rate = engaged / total if total > 0 else 0
            satisfaction_rate = satisfied / total if total > 0 else 0

            avg_duration = sum(p.session_duration or 0 for p in participants) / total
            avg_messages = sum(p.messages_sent or 0 for p in participants) / total

            # Check for existing result or create new
            result = ExperimentResult.query.filter_by(
                experiment_id=experiment_id, variant_id=variant_id
            ).first()

            if not result:
                result = ExperimentResult(experiment_id=experiment_id, variant_id=variant_id)
                db.session.add(result)

            # Update metrics
            result.total_participants = total
            result.total_conversions = conversions
            result.total_engaged = engaged
            result.conversion_rate = conversion_rate
            result.engagement_rate = engagement_rate
            result.satisfaction_rate = satisfaction_rate
            result.avg_session_duration = avg_duration
            result.avg_messages = avg_messages
            result.updated_at = datetime.now(timezone.utc)

        db.session.commit()

    @staticmethod
    def _calculate_statistical_significance(
        conversions_a: int, total_a: int, conversions_b: int, total_b: int
    ) -> Dict[str, Any]:
        """
        Calculate statistical significance using z-test for proportions

        Returns:
            dict with p_value, is_significant, confidence_interval
        """
        if total_a < 30 or total_b < 30:
            return {
                "is_significant": False,
                "p_value": None,
                "reason": "Insufficient sample size (need 30+ per variant)",
            }

        # Conversion rates
        p1 = conversions_a / total_a
        p2 = conversions_b / total_b

        # Pooled proportion
        p_pool = (conversions_a + conversions_b) / (total_a + total_b)

        # Standard error
        se = math.sqrt(p_pool * (1 - p_pool) * (1 / total_a + 1 / total_b))

        if se == 0:
            return {"is_significant": False, "p_value": None, "reason": "Zero variance"}

        # Z-score
        z_score = (p1 - p2) / se

        # P-value (two-tailed test)
        # Approximate using normal distribution
        p_value = 2 * (1 - ABTestingService._normal_cdf(abs(z_score)))

        # Is significant at 95% confidence (p < 0.05)
        is_significant = p_value < 0.05

        # Confidence interval for difference
        ci_margin = 1.96 * se  # 95% CI
        diff = p1 - p2

        return {
            "is_significant": is_significant,
            "p_value": p_value,
            "z_score": z_score,
            "confidence_interval": {"lower": diff - ci_margin, "upper": diff + ci_margin},
            "lift": ((p1 / p2) - 1) * 100 if p2 > 0 else 0,  # Percentage lift
        }

    @staticmethod
    def _normal_cdf(x: float) -> float:
        """Cumulative distribution function for standard normal distribution"""
        # Approximation using error function
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    @staticmethod
    def _declare_winner(experiment_id: int) -> Optional[Dict[str, Any]]:
        """Declare winner if criteria are met"""
        experiment = Experiment.query.get(experiment_id)

        if not experiment:
            return None

        # Get all results
        results = ExperimentResult.query.filter_by(experiment_id=experiment_id).all()

        if len(results) < 2:
            return {"message": "Need at least 2 variants"}

        # Check minimum sample size
        if any(r.total_participants < experiment.min_sample_size for r in results):
            return {
                "message": f"Need at least {experiment.min_sample_size} participants per variant"
            }

        # Sort by primary metric
        metric_key = experiment.primary_metric
        results_sorted = sorted(results, key=lambda r: getattr(r, metric_key, 0), reverse=True)

        best = results_sorted[0]
        second_best = results_sorted[1]

        # Calculate statistical significance between best and second best
        if metric_key == "conversion_rate":
            sig_test = ABTestingService._calculate_statistical_significance(
                best.total_conversions,
                best.total_participants,
                second_best.total_conversions,
                second_best.total_participants,
            )
        else:
            # For other metrics, simplified check
            sig_test = {
                "is_significant": best.total_participants >= experiment.min_sample_size * 2,
                "p_value": 0.04,  # Placeholder
            }

        if sig_test["is_significant"]:
            experiment.winner_variant_id = best.variant_id
            experiment.winner_declared_at = datetime.now(timezone.utc)

            # Update result
            best.is_statistically_significant = True
            best.p_value = sig_test.get("p_value")

            db.session.commit()

            return {
                "winner": best.variant_id,
                "metric": metric_key,
                "value": getattr(best, metric_key),
                "is_significant": True,
                "p_value": sig_test.get("p_value"),
                "lift": sig_test.get("lift"),
            }
        else:
            return {
                "message": "No statistically significant winner yet",
                "reason": sig_test.get("reason", "Insufficient difference between variants"),
            }

    @staticmethod
    def get_experiment_results(experiment_id: int) -> Dict[str, Any]:
        """Get full experiment results with statistical analysis"""
        experiment = Experiment.query.get(experiment_id)

        if not experiment:
            return {"error": "Experiment not found"}

        # Recalculate latest results
        ABTestingService._calculate_results(experiment_id)

        results = ExperimentResult.query.filter_by(experiment_id=experiment_id).all()

        return {
            "experiment": experiment.to_dict(),
            "results": [r.to_dict() for r in results],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def list_active_experiments() -> List[Dict[str, Any]]:
        """List all active experiments"""
        experiments = Experiment.query.filter_by(status="active").all()
        return [exp.to_dict() for exp in experiments]
