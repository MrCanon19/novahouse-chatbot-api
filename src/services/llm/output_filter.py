"""
LLM Output Filter - Validates and sanitizes LLM responses
"""
import re
from typing import Dict, Tuple, Optional


class LLMOutputFilter:
    """
    Filters and validates LLM output before sending to user.
    Protects against data leakage, API keys, and inappropriate content.
    """

    # Patterns that indicate data leakage
    LEAKAGE_PATTERNS = [
        # API keys and secrets
        r'(?i)(api[_-]?key|secret|token|password|hasło)[\s:=]+([\w\-]{20,})',
        r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API key
        r'pk_[a-zA-Z0-9]{32,}',  # Stripe key
        r'Bearer\s+[\w\-]{20,}',  # Bearer tokens
        # Database connection strings
        r'(?i)(postgresql|mysql|mongodb)://[^\s]+',
        r'(?i)(host|database|user|password)=[^\s]+',
        # Email addresses (might leak other users' data)
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        # Phone numbers (might leak other users' data)
        r'\+?\d{1,3}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',
        # Stack traces (might contain secrets)
        r'(Traceback|File.*?line|Exception|Error).*?(\n.*?){5,}',
        # Configuration dumps
        r'(?i)(config|konfiguracj|settings|ustawienia).*?[:=].*?\{.*?\}',
    ]

    # Maximum response length
    MAX_RESPONSE_LENGTH = 2000

    # Minimum response length (too short might indicate error)
    MIN_RESPONSE_LENGTH = 10

    @classmethod
    def filter_output(
        cls,
        llm_response: str,
        context: Optional[Dict] = None
    ) -> Tuple[str, bool, str]:
        """
        Filter and validate LLM response before sending to user.

        Args:
            llm_response: Raw response from LLM
            context: Optional context dict

        Returns:
            Tuple of (filtered_response, is_safe, reason)
            - filtered_response: Sanitized response (or safe fallback)
            - is_safe: True if response is safe, False if blocked
            - reason: Reason for blocking (if not safe)
        """
        if not llm_response:
            return "", False, "Empty response"

        # Check length
        if len(llm_response) > cls.MAX_RESPONSE_LENGTH:
            return (
                llm_response[:cls.MAX_RESPONSE_LENGTH] + "...",
                False,
                f"Response too long ({len(llm_response)} > {cls.MAX_RESPONSE_LENGTH})"
            )

        if len(llm_response.strip()) < cls.MIN_RESPONSE_LENGTH:
            return "", False, f"Response too short ({len(llm_response)} < {cls.MIN_RESPONSE_LENGTH})"

        # Check for data leakage
        for pattern in cls.LEAKAGE_PATTERNS:
            matches = re.findall(pattern, llm_response)
            if matches:
                # Log but don't block - might be legitimate (e.g., user's own email)
                # But sanitize sensitive patterns
                filtered = cls._sanitize_leakage(llm_response, pattern)
                return filtered, True, f"Sanitized potential leakage: {pattern[:50]}"

        # Check for inappropriate content (basic check)
        if cls._contains_inappropriate_content(llm_response):
            return "", False, "Inappropriate content detected"

        return llm_response, True, "OK"

    @classmethod
    def _sanitize_leakage(cls, text: str, pattern: str) -> str:
        """
        Sanitize potential data leakage in text.
        """
        # Remove API keys
        text = re.sub(r'sk-[a-zA-Z0-9]{32,}', '[API_KEY_REDACTED]', text)
        text = re.sub(r'pk_[a-zA-Z0-9]{32,}', '[API_KEY_REDACTED]', text)
        text = re.sub(r'Bearer\s+[\w\-]{20,}', '[TOKEN_REDACTED]', text)

        # Remove connection strings
        text = re.sub(r'(?i)(postgresql|mysql|mongodb)://[^\s]+', '[CONNECTION_STRING_REDACTED]', text)

        # Remove stack traces
        text = re.sub(r'(Traceback|File.*?line).*?(\n.*?){5,}', '[STACK_TRACE_REDACTED]', text, flags=re.DOTALL)

        return text

    @classmethod
    def _contains_inappropriate_content(cls, text: str) -> bool:
        """
        Basic check for inappropriate content.
        """
        inappropriate_patterns = [
            r'(?i)(hack|exploit|vulnerability|exploitacja)',
            r'(?i)(bypass|obchodzenie|omijanie).*?(security|bezpieczeństwo)',
        ]

        for pattern in inappropriate_patterns:
            if re.search(pattern, text):
                return True

        return False

    @classmethod
    def get_safe_fallback(cls) -> str:
        """
        Returns a safe fallback response when output is blocked.
        """
        return (
            "Przepraszam, wystąpił problem z wygenerowaniem odpowiedzi. "
            "Czy mogę pomóc Ci w czymś innym związanym z wykończeniem mieszkania?"
        )

