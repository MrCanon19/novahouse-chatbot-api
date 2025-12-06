"""
Enhanced extract_context with safeguards
Integrates validation and regression detection
"""

import logging
import time
from typing import Any, Dict

from src.services.extraction_validator import get_safeguard, get_validator
from src.services.regression_detector import ExtractionMetrics, record_metrics

logger = logging.getLogger(__name__)


def extract_context_safe(message: str, existing_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Safe wrapper around extract_context with validation and monitoring

    Args:
        message: User message
        existing_context: Previous context to merge with

    Returns:
        Validated and safe context dict
    """
    import re

    from src.utils.polish_cities import PolishCities

    if existing_context is None:
        existing_context = {}

    start_time = time.time()
    get_safeguard()
    validator = get_validator()

    # Sanitize message first
    message = validator.sanitize_message(message)
    if not message:
        return existing_context

    message_lower = message.lower()

    try:
        # Extract name - only if looks like Polish name
        name_patterns = [
            r"(?:jestem|mam na imię|moje imię|to|[Ii] to)\s+([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+(?:\s+[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)?)",
            r"^([A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+(?:\s+[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)?)[\s,]",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1).strip()
                validated_name = validator.validate_name(name)
                if validated_name:
                    existing_context["name"] = validated_name
                    logger.debug(f"✓ Extracted name: {validated_name}")
                break

        # Extract email
        email_pattern = r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})"
        match = re.search(email_pattern, message)
        if match:
            email = match.group(1)
            validated_email = validator.validate_email(email)
            if validated_email:
                existing_context["email"] = validated_email
                logger.debug(f"✓ Extracted email: {validated_email}")

        # Extract phone
        phone_patterns = [
            r"(?:\+48|0048|48)?[\s-]?(\d{9})",  # Polish format
            r"\+?48\s?(?:\d\s?){8}\d",
            r"(?:\d{3}[\s.-]?){2}\d{3}",  # XXX-XXX-XXX format
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, message)
            if match:
                phone = match.group(0)
                validated_phone = validator.validate_phone(phone)
                if validated_phone:
                    existing_context["phone"] = validated_phone
                    logger.debug(f"✓ Extracted phone: {validated_phone}")
                break

        # Extract city using PolishCities utility
        polish_cities = PolishCities()

        # Try common Polish cities with their declension forms
        city_patterns = {
            "Warszawa": ["warszawa", "warszawy", "warszawie"],
            "Gdańsk": ["gdańsk", "gdańska", "gdańsku"],
            "Wrocław": ["wrocław", "wrocławia", "wrocławiu"],
            "Kraków": ["kraków", "krakowa", "krakowie"],
            "Poznań": ["poznań", "poznania", "poznaniu"],
            "Łódź": ["łódź", "łodzi"],
            "Sopot": ["sopot", "sopotu"],
            "Gdynia": ["gdynia", "gdyni"],
        }

        for city, patterns in city_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    validated_city = validator.validate_city(city)
                    if validated_city:
                        existing_context["city"] = validated_city
                        logger.debug(f"✓ Extracted city: {validated_city}")
                    break
            if existing_context.get("city"):
                break

        # Fall back to checking all known Polish cities
        if not existing_context.get("city"):
            all_cities = polish_cities.get_all_cities()
            for city in all_cities:
                if city.lower() in message_lower:
                    validated_city = validator.validate_city(city)
                    if validated_city:
                        existing_context["city"] = validated_city
                        logger.debug(f"✓ Extracted city (from GUS): {validated_city}")
                    break

        # Extract square meters
        sqm_patterns = [
            r"(\d+)\s*m²",
            r"(\d+)\s*metrów",
            r"(\d+)\s*m2",
            r"(\d+)\s*mkw",
        ]
        for pattern in sqm_patterns:
            match = re.search(pattern, message_lower)
            if match:
                try:
                    sqm = int(match.group(1))
                    validated_sqm = validator.validate_square_meters(sqm)
                    if validated_sqm:
                        existing_context["square_meters"] = validated_sqm
                        logger.debug(f"✓ Extracted sqm: {validated_sqm}")
                    break
                except (ValueError, TypeError):
                    logger.warning(f"Failed to parse sqm: {match.group(1)}")
                    break

        # Extract budget with safeguards
        budget_patterns = [
            r"(?:budżet|budzet|budget|mam|dysponuję|do wydania).*?(\d+)\s*(?:tys|tysiące|tysięcy|tyś|000)",
            r"(?:budżet|budzet|budget|mam|dysponuję).*?(\d[\d\s]{2,})\s*(?:zł|złotych|pln)",
            r"(\d+)\s*(?:tys|tysiące|tysięcy|tyś).*?(?:zł|złotych|pln)",
            r"(\d[\d\s]{5,})\s*(?:zł|złotych|pln)",
        ]
        for pattern in budget_patterns:
            match = re.search(pattern, message_lower)
            if match:
                try:
                    budget_str = match.group(1).replace(" ", "")
                    # Convert to full number
                    if "tys" in message_lower or "tyś" in message_lower:
                        budget = int(budget_str) * 1000
                    else:
                        budget = int(budget_str)
                    # Validate budget
                    validated_budget = validator.validate_budget(budget)
                    if validated_budget:
                        existing_context["budget"] = validated_budget
                        logger.debug(f"✓ Extracted budget: {validated_budget}")
                    break
                except (ValueError, TypeError):
                    logger.warning(f"Failed to parse budget: {match.group(1)}")
                    break

        # Extract interested package with flexible matching
        packages = ["express", "comfort", "premium", "indywidualny"]
        for pkg in packages:
            if pkg == "indywidualny":
                # Match with Polish declension
                if re.search(r"indywidualne?\w*", message_lower):
                    existing_context["package"] = "Indywidualny"
                    logger.debug("✓ Extracted package: Indywidualny")
                    break
            else:
                if pkg in message_lower:
                    existing_context["package"] = pkg.title()
                    logger.debug(f"✓ Extracted package: {pkg.title()}")
                    break

        # Final validation of entire context
        existing_context = validator.validate_context(existing_context)

        # Record metrics
        elapsed_ms = (time.time() - start_time) * 1000
        extracted_count = sum(
            1
            for k in ["name", "email", "phone", "city", "square_meters", "budget", "package"]
            if k in existing_context
        )

        metrics = ExtractionMetrics(
            timestamp=str(time.time()),
            total_extractions=1,
            successful_extractions=1,
            failed_extractions=0,
            validation_failures=0,
            avg_extraction_time_ms=elapsed_ms,
            cities_extracted=1 if "city" in existing_context else 0,
            packages_extracted=1 if "package" in existing_context else 0,
            budgets_extracted=1 if "budget" in existing_context else 0,
            emails_extracted=1 if "email" in existing_context else 0,
            phones_extracted=1 if "phone" in existing_context else 0,
            names_extracted=1 if "name" in existing_context else 0,
        )

        alerts = record_metrics(metrics)

        # Log any alerts
        for alert in alerts:
            logger.warning(f"Alert: {alert.message}")

        logger.info(f"Extracted: {extracted_count} fields in {elapsed_ms:.1f}ms")

        return existing_context

    except Exception as e:
        logger.error(f"Extraction failed with exception: {str(e)}", exc_info=True)
        # Return partial context we managed to extract
        return existing_context


def get_extraction_health() -> Dict[str, Any]:
    """Get extraction system health status"""
    from src.services.regression_detector import get_detector

    detector = get_detector()
    trend = detector.get_trend(last_n=20)
    alerts = detector.get_alerts(last_n=10)

    return {
        "status": "healthy" if trend.get("avg_success_rate", 100) > 95 else "degraded",
        "trend": trend,
        "recent_alerts": alerts,
    }
