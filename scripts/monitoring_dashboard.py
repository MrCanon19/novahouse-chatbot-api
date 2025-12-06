#!/usr/bin/env python3
"""
Extraction Quality Dashboard
Real-time monitoring of extraction system health
Can be run locally or deployed as a background process
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.extraction_validator import get_validator
from src.services.regression_detector import get_detector


def clear_screen():
    """Clear terminal screen"""
    print("\033[2J\033[H", end="")


def print_header():
    """Print dashboard header"""
    print("=" * 80)
    print("📊 CHATBOT EXTRACTION QUALITY DASHBOARD")
    print("=" * 80)
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_metrics(detector):
    """Print extraction metrics"""
    trend = detector.get_trend(last_n=100)

    print("📈 EXTRACTION METRICS (last 100 measurements)")
    print("-" * 80)

    avg_rate = trend.get("avg_success_rate", 0)
    validation_rate = trend.get("validation_failure_rate", 0)
    total_extractions = trend.get("total_extractions", 0)

    # Color-coded success rate
    if avg_rate > 95:
        rate_indicator = "🟢 HEALTHY"
    elif avg_rate > 85:
        rate_indicator = "🟡 DEGRADED"
    else:
        rate_indicator = "🔴 CRITICAL"

    print(f"Success Rate: {avg_rate:.1f}% {rate_indicator}")
    print(f"Validation Failure Rate: {validation_rate:.1f}%")
    print(f"Total Extractions: {total_extractions:,}")
    print(f"Trend: {trend.get('trend', 'unknown')}")
    print()


def print_alerts(detector):
    """Print recent alerts"""
    alerts = detector.get_alerts(last_n=10)

    print("🚨 RECENT ALERTS (last 10)")
    print("-" * 80)

    if not alerts:
        print("✅ No alerts")
    else:
        for i, alert in enumerate(alerts, 1):
            severity = alert.get("severity", "unknown")
            alert_type = alert.get("alert_type", "unknown")
            message = alert.get("message", "")

            if severity == "critical":
                indicator = "🔴"
            else:
                indicator = "🟡"

            print(f"{i}. {indicator} [{alert_type}] {message}")

    print()


def print_validation_config(validator):
    """Print validation configuration"""
    print("⚙️  VALIDATION RULES")
    print("-" * 80)

    ranges = validator.VALID_RANGES
    print(f"Budget: {ranges['budget'][0]:,} - {ranges['budget'][1]:,} PLN")
    print(f"Square Meters: {ranges['square_meters'][0]} - {ranges['square_meters'][1]} m²")
    print(f"Lead Score: {ranges['lead_score'][0]} - {ranges['lead_score'][1]} points")
    print()

    print(f"Known Cities: {len(validator.KNOWN_CITIES)}")
    print(f"Valid Packages: {', '.join(validator.VALID_PACKAGES)}")
    print()


def print_recommendations(detector):
    """Print recommendations based on metrics"""
    trend = detector.get_trend(last_n=100)
    avg_rate = trend.get("avg_success_rate", 100)

    print("💡 RECOMMENDATIONS")
    print("-" * 80)

    if avg_rate > 95:
        print("✅ System performing normally. Continue monitoring.")
    elif avg_rate > 85:
        print("⚠️  Success rate declining. Review recent changes to extraction logic.")
        print("    - Check for new edge cases in user messages")
        print("    - Review package/city matching patterns")
    elif avg_rate > 75:
        print("🚨 CRITICAL: Success rate is low. Immediate investigation needed:")
        print("    1. Check regression_detector alerts for patterns")
        print("    2. Review validation_rules endpoint for bounds issues")
        print("    3. Run test suite: make test")
        print("    4. Check chatbot.py extract_context() function")
    else:
        print("🚨🚨 CRITICAL: System failure detected!")
        print("    IMMEDIATE ACTION REQUIRED:")
        print("    1. Review all recent code changes")
        print("    2. Check system logs for exceptions")
        print("    3. Run: python tests/test_customer_journey_comprehensive.py")
        print("    4. Consider rollback of recent changes")

    print()


def print_footer():
    """Print dashboard footer"""
    print("=" * 80)
    print("📍 Endpoints for detailed monitoring:")
    print("  - /api/monitoring/extraction-quality")
    print("  - /api/monitoring/regression-history")
    print("  - /api/monitoring/validation-rules")
    print("  - /api/monitoring/extraction-errors")
    print()
    print("Press Ctrl+C to exit")
    print("=" * 80)


def main():
    """Main dashboard loop"""
    detector = get_detector()
    validator = get_validator()

    try:
        while True:
            clear_screen()
            print_header()
            print_metrics(detector)
            print_alerts(detector)
            print_validation_config(validator)
            print_recommendations(detector)
            print_footer()

            time.sleep(10)  # Update every 10 seconds

    except KeyboardInterrupt:
        print("\n\n👋 Dashboard closed")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
