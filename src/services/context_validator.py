"""
Context Memory Validator
Validates and sanitizes user data collected in conversations
"""

import re
from typing import Any, Dict, Optional, Tuple


class ContextValidator:
    """Validates and sanitizes context memory fields"""

    # Polish phone patterns
    PHONE_PATTERNS = [
        r"^\+48\s?\d{3}\s?\d{3}\s?\d{3}$",  # +48 123 456 789
        r"^48\d{9}$",  # 48123456789
        r"^\d{9}$",  # 123456789
        r"^\d{3}\s?\d{3}\s?\d{3}$",  # 123 456 789
    ]

    # Email pattern
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Valid cities (major Polish cities)
    VALID_CITIES = {
        "warszawa",
        "kraków",
        "wrocław",
        "poznań",
        "gdańsk",
        "szczecin",
        "bydgoszcz",
        "lublin",
        "katowice",
        "białystok",
        "gdynia",
        "częstochowa",
        "radom",
        "sosnowiec",
        "toruń",
        "kielce",
        "gliwice",
        "zabrze",
        "bytom",
        "olsztyn",
        "bielsko-biała",
        "rzeszów",
        "ruda śląska",
        "rybnik",
        "tychy",
        "dąbrowa górnicza",
        "płock",
        "elbląg",
        "opole",
        "gorzów wielkopolski",
    }

    # Valid packages
    VALID_PACKAGES = {
        "express",
        "express plus",
        "comfort",
        "comfort plus",
        "premium",
        "szafranowy",
        "turkusowy",
        "miętowy",
    }

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate email address

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not email or not isinstance(email, str):
            return False, None, "Email is empty"

        email = email.strip().lower()

        if not re.match(ContextValidator.EMAIL_PATTERN, email):
            return False, None, "Invalid email format"

        if len(email) > 100:
            return False, None, "Email too long"

        return True, email, None

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate and normalize phone number

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not phone or not isinstance(phone, str):
            return False, None, "Phone is empty"

        # Remove common separators
        phone = phone.strip().replace("-", " ").replace("(", "").replace(")", "")

        # Check against patterns
        for pattern in ContextValidator.PHONE_PATTERNS:
            if re.match(pattern, phone):
                # Normalize to +48XXXXXXXXX format
                digits = re.sub(r"\D", "", phone)
                if len(digits) == 9:
                    return True, f"+48{digits}", None
                elif len(digits) == 11 and digits.startswith("48"):
                    return True, f"+{digits}", None

        return False, None, "Invalid phone format (expected Polish number)"

    @staticmethod
    def validate_city(city: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate city name

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not city or not isinstance(city, str):
            return False, None, "City is empty"

        city = city.strip().lower()

        # Remove accents for comparison
        city_normalized = (
            city.replace("ł", "l")
            .replace("ą", "a")
            .replace("ę", "e")
            .replace("ć", "c")
            .replace("ń", "n")
            .replace("ó", "o")
            .replace("ś", "s")
            .replace("ź", "z")
            .replace("ż", "z")
        )

        if city_normalized in ContextValidator.VALID_CITIES:
            return True, city.title(), None

        # Fuzzy match (close enough)
        for valid_city in ContextValidator.VALID_CITIES:
            if city_normalized in valid_city or valid_city in city_normalized:
                return True, valid_city.title(), None

        # Accept anyway but warn
        return True, city.title(), "City not in major cities list (accepted anyway)"

    @staticmethod
    def validate_square_meters(sqm: Any) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Validate square meters

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not sqm:
            return False, None, "Square meters is empty"

        # Convert to int
        try:
            if isinstance(sqm, str):
                # Remove non-digit characters
                sqm = re.sub(r"\D", "", sqm)
            sqm_int = int(sqm)
        except (ValueError, TypeError):
            return False, None, "Square meters must be a number"

        # Reasonable range for apartments
        if sqm_int < 15:
            return False, None, "Square meters too small (minimum 15m²)"
        if sqm_int > 500:
            return False, None, "Square meters too large (maximum 500m²)"

        return True, sqm_int, None

    @staticmethod
    def validate_package(package: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate package name

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not package or not isinstance(package, str):
            return False, None, "Package is empty"

        package = package.strip().lower()

        if package in ContextValidator.VALID_PACKAGES:
            return True, package.title(), None

        # Fuzzy match
        for valid_pkg in ContextValidator.VALID_PACKAGES:
            if package in valid_pkg or valid_pkg in package:
                return True, valid_pkg.title(), None

        return (
            False,
            None,
            f"Unknown package (expected one of: {', '.join(ContextValidator.VALID_PACKAGES)})",
        )

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate name

        Returns:
            (is_valid, sanitized_value, error_message)
        """
        if not name or not isinstance(name, str):
            return False, None, "Name is empty"

        name = name.strip()

        if len(name) < 2:
            return False, None, "Name too short"
        if len(name) > 100:
            return False, None, "Name too long"

        # Must contain at least letters
        if not re.search(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", name):
            return False, None, "Name must contain letters"

        return True, name.title(), None

    @classmethod
    def validate_context(cls, context_memory: Dict) -> Tuple[bool, Dict, Dict]:
        """
        Validate entire context memory

        Returns:
            (is_valid, sanitized_context, errors)
        """
        sanitized = {}
        errors = {}

        # Validate each field if present
        if context_memory.get("email"):
            valid, value, error = cls.validate_email(context_memory["email"])
            if valid:
                sanitized["email"] = value
            else:
                errors["email"] = error

        if context_memory.get("phone"):
            valid, value, error = cls.validate_phone(context_memory["phone"])
            if valid:
                sanitized["phone"] = value
            else:
                errors["phone"] = error

        if context_memory.get("city"):
            valid, value, error = cls.validate_city(context_memory["city"])
            if valid:
                sanitized["city"] = value
            if error:  # Warning, not blocker
                errors["city"] = error

        if context_memory.get("square_meters"):
            valid, value, error = cls.validate_square_meters(context_memory["square_meters"])
            if valid:
                sanitized["square_meters"] = value
            else:
                errors["square_meters"] = error

        if context_memory.get("package"):
            valid, value, error = cls.validate_package(context_memory["package"])
            if valid:
                sanitized["package"] = value
            else:
                errors["package"] = error

        if context_memory.get("name"):
            valid, value, error = cls.validate_name(context_memory["name"])
            if valid:
                sanitized["name"] = value
            else:
                errors["name"] = error

        # Keep other fields as-is
        for key, value in context_memory.items():
            if key not in sanitized and key not in errors:
                sanitized[key] = value

        is_valid = len(errors) == 0
        return is_valid, sanitized, errors
