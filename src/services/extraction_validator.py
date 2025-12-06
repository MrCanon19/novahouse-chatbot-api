"""
Extraction Validator & Safeguard System
Prevents common extraction failures and auto-recovers from errors
"""

import logging
import re
from typing import Any, Callable, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ExtractionValidator:
    """
    Validates extracted data and prevents invalid states
    Provides auto-recovery and fallback mechanisms
    """

    # Define valid ranges and patterns
    VALID_RANGES = {
        "square_meters": (10, 1000),  # m² - apartment to estate
        "budget": (50000, 5000000),  # PLN - residential range
        "lead_score": (0, 100),  # Points
        "message_count": (1, 1000),  # Messages in conversation
    }

    VALID_FORMATS = {
        "email": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",
        "phone": r"^\+?48\d{9}$|^\d{3}\s?\d{3}\s?\d{3}$|^\d{9}$",
        "name": r"^[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+(?: [A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)?$",
    }

    KNOWN_CITIES = {
        "warszawa",
        "gdańsk",
        "wrocław",
        "kraków",
        "poznań",
        "łódź",
        "sopot",
        "gdynia",
    }

    VALID_PACKAGES = {"express", "comfort", "premium", "indywidualny"}

    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        """Validate and normalize email"""
        if not email:
            return None

        email = email.strip().lower()

        # Check format
        if not re.match(ExtractionValidator.VALID_FORMATS["email"], email):
            logger.warning(f"Invalid email format: {email}")
            return None

        # Check length
        if len(email) > 254:  # RFC 5321
            logger.warning(f"Email too long: {email}")
            return None

        return email

    @staticmethod
    def validate_phone(phone: Optional[str]) -> Optional[str]:
        """Validate and normalize phone"""
        if not phone:
            return None

        phone = phone.strip().replace(" ", "")

        # Check format
        if not re.match(ExtractionValidator.VALID_FORMATS["phone"], phone):
            logger.warning(f"Invalid phone format: {phone}")
            return None

        # Normalize to consistent format
        if phone.startswith("+48"):
            return phone
        if phone.startswith("48"):
            return "+" + phone
        if len(phone) == 9 and phone.isdigit():
            return "+48" + phone

        return phone

    @staticmethod
    def validate_name(name: Optional[str]) -> Optional[str]:
        """Validate and normalize name"""
        if not name:
            return None

        name = name.strip()

        # Check if starts with uppercase (Polish names)
        if not name or not name[0].isupper():
            logger.warning(f"Name doesn't start with uppercase: {name}")
            return None

        # Check length
        if len(name) < 2 or len(name) > 100:
            logger.warning(f"Name length invalid: {name}")
            return None

        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(
            r"^[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+(?:(?:[\s'-])[A-ZŚŻŹĆŃĄĘÓŁ][a-ząęółćżźśń]+)*$", name
        ):
            logger.warning(f"Invalid characters in name: {name}")
            return None

        return name

    @staticmethod
    def validate_city(city: Optional[str]) -> Optional[str]:
        """Validate and normalize city"""
        if not city:
            return None

        city = city.strip().title()

        # Check known cities (normalized)
        if city.lower() in ExtractionValidator.KNOWN_CITIES:
            return city

        # Allow any city-like name (3+ letters, no numbers)
        if len(city) >= 3 and not any(char.isdigit() for char in city):
            return city

        logger.warning(f"Invalid city: {city}")
        return None

    @staticmethod
    def validate_square_meters(sqm: Optional[int]) -> Optional[int]:
        """Validate square meters"""
        if sqm is None:
            return None

        min_sqm, max_sqm = ExtractionValidator.VALID_RANGES["square_meters"]

        if not isinstance(sqm, int) or sqm < min_sqm or sqm > max_sqm:
            logger.warning(f"Invalid square_meters: {sqm} (valid: {min_sqm}-{max_sqm})")
            return None

        return sqm

    @staticmethod
    def validate_budget(budget: Optional[int]) -> Optional[int]:
        """Validate budget amount"""
        if budget is None:
            return None

        min_budget, max_budget = ExtractionValidator.VALID_RANGES["budget"]

        if not isinstance(budget, int) or budget < min_budget or budget > max_budget:
            logger.warning(f"Invalid budget: {budget} (valid: {min_budget}-{max_budget})")
            return None

        return budget

    @staticmethod
    def validate_package(package: Optional[str]) -> Optional[str]:
        """Validate and normalize package"""
        if not package:
            return None

        package_lower = package.lower()

        # Normalize Polish declension
        if "indywidualny" in package_lower or "indywidualn" in package_lower:
            return "Indywidualny"

        for valid_pkg in ExtractionValidator.VALID_PACKAGES:
            if valid_pkg in package_lower:
                return valid_pkg.title()

        logger.warning(f"Invalid package: {package}")
        return None

    @staticmethod
    def validate_lead_score(score: Optional[int]) -> Optional[int]:
        """Validate lead score"""
        if score is None:
            return None

        min_score, max_score = ExtractionValidator.VALID_RANGES["lead_score"]

        if not isinstance(score, int) or score < min_score or score > max_score:
            logger.warning(f"Invalid lead_score: {score} (valid: {min_score}-{max_score})")
            return None

        return score

    @staticmethod
    def validate_context(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate entire context dict and remove invalid fields
        Returns cleaned context with only valid values
        """
        if not isinstance(context, dict):
            logger.error(f"Context is not a dict: {type(context)}")
            return {}

        cleaned = {}

        # Validate each field
        validation_map = {
            "email": ExtractionValidator.validate_email,
            "phone": ExtractionValidator.validate_phone,
            "name": ExtractionValidator.validate_name,
            "city": ExtractionValidator.validate_city,
            "square_meters": ExtractionValidator.validate_square_meters,
            "budget": ExtractionValidator.validate_budget,
            "package": ExtractionValidator.validate_package,
            "lead_score": ExtractionValidator.validate_lead_score,
        }

        for key, value in context.items():
            if key in validation_map:
                validator = validation_map[key]
                try:
                    validated_value = validator(value)
                    if validated_value is not None:
                        cleaned[key] = validated_value
                    else:
                        logger.warning(f"Validation failed for {key}: {value}")
                except Exception as e:
                    logger.error(f"Exception validating {key}: {str(e)}")
            else:
                # Keep other fields as-is
                cleaned[key] = value

        return cleaned

    @staticmethod
    def with_fallback(
        primary_func: Callable[[], T],
        fallback_func: Callable[[], T],
        error_message: str = "Primary function failed",
    ) -> T:
        """
        Try primary function, fall back to secondary if it fails
        Prevents cascading failures
        """
        try:
            result = primary_func()
            if result is not None:
                return result
        except Exception as e:
            logger.warning(f"{error_message}: {str(e)}")

        try:
            result = fallback_func()
            if result is not None:
                logger.info("Using fallback result")
                return result
        except Exception as e:
            logger.error(f"Fallback also failed: {str(e)}")

        return None

    @staticmethod
    def sanitize_message(message: str) -> str:
        """
        Clean message before extraction
        Remove emojis, extra spaces, etc.
        """
        if not isinstance(message, str):
            logger.warning(f"Message is not a string: {type(message)}")
            return ""

        # Remove emojis
        message = message.encode("ascii", "ignore").decode("ascii")  # Strip non-ASCII

        # Remove extra whitespace
        message = " ".join(message.split())

        # Limit length
        if len(message) > 5000:
            logger.warning(f"Message too long ({len(message)} chars), truncating")
            message = message[:5000]

        return message


class ExtractionSafeguard:
    """
    Wraps extraction functions with error handling and recovery
    """

    def __init__(self):
        self.extraction_errors = []
        self.validation_failures = []

    def safe_extract(self, extraction_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Safely run extraction function with error handling
        """
        try:
            result = extraction_func(*args, **kwargs)

            if not isinstance(result, dict):
                logger.error(f"Extraction result is not dict: {type(result)}")
                return {}

            # Validate before returning
            cleaned = ExtractionValidator.validate_context(result)
            return cleaned

        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            self.extraction_errors.append(
                {
                    "func": extraction_func.__name__,
                    "error": str(e),
                    "args": str(args)[:100],  # Limit size
                }
            )
            return {}

    def report(self) -> Dict[str, Any]:
        """Get error report"""
        return {
            "extraction_errors": len(self.extraction_errors),
            "validation_failures": len(self.validation_failures),
            "last_errors": self.extraction_errors[-5:],  # Last 5 errors
        }


# Global instance for convenience
_validator = ExtractionValidator()
_safeguard = ExtractionSafeguard()


def get_validator() -> ExtractionValidator:
    """Get global validator instance"""
    return _validator


def get_safeguard() -> ExtractionSafeguard:
    """Get global safeguard instance"""
    return _safeguard
