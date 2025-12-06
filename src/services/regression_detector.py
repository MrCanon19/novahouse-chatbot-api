"""
Regression Detection & Prevention System
Monitors extract_context() output and alerts on quality degradation
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class ExtractionMetrics:
    """Tracks extraction quality metrics"""

    timestamp: str
    total_extractions: int
    successful_extractions: int
    failed_extractions: int
    validation_failures: int
    avg_extraction_time_ms: float
    cities_extracted: int
    packages_extracted: int
    budgets_extracted: int
    emails_extracted: int
    phones_extracted: int
    names_extracted: int

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_extractions == 0:
            return 0.0
        return (self.successful_extractions / self.total_extractions) * 100

    @property
    def validation_failure_rate(self) -> float:
        """Calculate validation failure rate"""
        if self.successful_extractions == 0:
            return 0.0
        return (self.validation_failures / self.successful_extractions) * 100


@dataclass
class RegressionAlert:
    """Alert when metrics degrade"""

    timestamp: str
    alert_type: str  # 'success_rate_drop', 'extraction_failures', 'validation_spike'
    severity: str  # 'warning', 'critical'
    message: str
    previous_value: float
    current_value: float
    threshold: float


class RegressionDetector:
    """
    Monitors extraction quality and detects regressions
    Maintains historical data for trend analysis
    """

    def __init__(self, max_history: int = 1000):
        self.metrics_history: List[ExtractionMetrics] = []
        self.alerts_history: List[RegressionAlert] = []
        self.max_history = max_history

        # Thresholds for alerts
        self.success_rate_threshold = 95.0  # %
        self.validation_failure_threshold = 5.0  # %
        self.extraction_failure_spike = 0.10  # 10% increase

    def record_metrics(self, metrics: ExtractionMetrics) -> List[RegressionAlert]:
        """
        Record new metrics and check for regressions
        Returns list of alerts (if any)
        """
        alerts = []

        # Check for regressions
        if self.metrics_history:
            previous = self.metrics_history[-1]
            alerts.extend(self._check_success_rate(metrics, previous))
            alerts.extend(self._check_validation_failures(metrics, previous))
            alerts.extend(self._check_extraction_failures(metrics, previous))

        # Store metrics
        self.metrics_history.append(metrics)

        # Trim history if too large
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history :]

        # Store alerts
        self.alerts_history.extend(alerts)

        # Log alerts
        for alert in alerts:
            if alert.severity == "critical":
                logger.critical(f"🚨 {alert.message}")
            else:
                logger.warning(f"⚠️  {alert.message}")

        return alerts

    def _check_success_rate(
        self, current: ExtractionMetrics, previous: ExtractionMetrics
    ) -> List[RegressionAlert]:
        """Check if success rate dropped"""
        alerts = []

        if current.success_rate < self.success_rate_threshold:
            # Too low
            severity = "critical" if current.success_rate < 80.0 else "warning"
            alerts.append(
                RegressionAlert(
                    timestamp=datetime.now().isoformat(),
                    alert_type="success_rate_drop",
                    severity=severity,
                    message=f"Success rate low: {current.success_rate:.1f}% (threshold: {self.success_rate_threshold}%)",
                    previous_value=previous.success_rate,
                    current_value=current.success_rate,
                    threshold=self.success_rate_threshold,
                )
            )

        elif current.success_rate < previous.success_rate - 5.0:
            # Significant drop
            alerts.append(
                RegressionAlert(
                    timestamp=datetime.now().isoformat(),
                    alert_type="success_rate_drop",
                    severity="warning",
                    message=f"Success rate dropped: {previous.success_rate:.1f}% → {current.success_rate:.1f}%",
                    previous_value=previous.success_rate,
                    current_value=current.success_rate,
                    threshold=self.success_rate_threshold,
                )
            )

        return alerts

    def _check_validation_failures(
        self, current: ExtractionMetrics, previous: ExtractionMetrics
    ) -> List[RegressionAlert]:
        """Check if validation failures spiked"""
        alerts = []

        if current.validation_failure_rate > self.validation_failure_threshold:
            alerts.append(
                RegressionAlert(
                    timestamp=datetime.now().isoformat(),
                    alert_type="validation_spike",
                    severity="warning",
                    message=f"Validation failures high: {current.validation_failure_rate:.1f}% (threshold: {self.validation_failure_threshold}%)",
                    previous_value=previous.validation_failure_rate,
                    current_value=current.validation_failure_rate,
                    threshold=self.validation_failure_threshold,
                )
            )

        elif current.validation_failure_rate > previous.validation_failure_rate * (
            1 + self.extraction_failure_spike
        ):
            alerts.append(
                RegressionAlert(
                    timestamp=datetime.now().isoformat(),
                    alert_type="validation_spike",
                    severity="warning",
                    message=f"Validation failures spiked: {previous.validation_failure_rate:.1f}% → {current.validation_failure_rate:.1f}%",
                    previous_value=previous.validation_failure_rate,
                    current_value=current.validation_failure_rate,
                    threshold=self.validation_failure_threshold,
                )
            )

        return alerts

    def _check_extraction_failures(
        self, current: ExtractionMetrics, previous: ExtractionMetrics
    ) -> List[RegressionAlert]:
        """Check if extraction failures increased"""
        alerts = []

        current_fail_rate = (
            current.failed_extractions / current.total_extractions
            if current.total_extractions > 0
            else 0.0
        )
        previous_fail_rate = (
            previous.failed_extractions / previous.total_extractions
            if previous.total_extractions > 0
            else 0.0
        )

        if current_fail_rate > previous_fail_rate * (1 + self.extraction_failure_spike):
            alerts.append(
                RegressionAlert(
                    timestamp=datetime.now().isoformat(),
                    alert_type="extraction_failures",
                    severity="warning",
                    message=f"Extraction failures increased: {(previous_fail_rate * 100):.1f}% → {(current_fail_rate * 100):.1f}%",
                    previous_value=previous_fail_rate * 100,
                    current_value=current_fail_rate * 100,
                    threshold=10.0,
                )
            )

        return alerts

    def get_trend(self, last_n: int = 10) -> Dict[str, Any]:
        """
        Get trend data for monitoring dashboard
        """
        if not self.metrics_history:
            return {}

        recent = self.metrics_history[-last_n:]

        return {
            "period": f"last {len(recent)} measurements",
            "success_rates": [m.success_rate for m in recent],
            "avg_success_rate": sum(m.success_rate for m in recent) / len(recent),
            "total_extractions": sum(m.total_extractions for m in recent),
            "validation_failure_rate": sum(m.validation_failure_rate for m in recent) / len(recent),
            "trend": (
                "stable"
                if len(recent) < 2
                else (
                    "improving" if recent[-1].success_rate > recent[0].success_rate else "degrading"
                )
            ),
        }

    def get_alerts(self, last_n: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        return [asdict(a) for a in self.alerts_history[-last_n:]]

    def export_metrics(self, filepath: str) -> None:
        """Export metrics history to JSON file"""
        try:
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_metrics": len(self.metrics_history),
                "metrics": [asdict(m) for m in self.metrics_history],
                "alerts": [asdict(a) for a in self.alerts_history],
                "current_trend": self.get_trend(),
            }

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

            logger.info(f"Metrics exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export metrics: {str(e)}")


# Global instance
_detector = RegressionDetector()


def get_detector() -> RegressionDetector:
    """Get global detector instance"""
    return _detector


def record_metrics(metrics: ExtractionMetrics) -> List[RegressionAlert]:
    """Record metrics and check for regressions"""
    return _detector.record_metrics(metrics)
