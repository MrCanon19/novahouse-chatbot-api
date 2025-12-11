"""
LLM Input Filter - Protection against prompt injection and malicious input
"""
import re
from typing import Dict, Tuple


class LLMInputFilter:
    """
    Filters and sanitizes user input before sending to LLM.
    Protects against prompt injection, system prompt extraction, and malicious content.
    """

    # Dangerous patterns that indicate prompt injection attempts
    INJECTION_PATTERNS = [
        # Direct prompt extraction attempts
        r"(?i)(pokaż|wyświetl|wypisz|wypluj|wydrukuj).*?(prompt|instrukcj|system|pierwotn|oryginaln)",
        r"(?i)(ignore|ignoruj|zignoruj).*?(poprzedni|wcześniejsz|instrukcj|zasady|reguły)",
        r"(?i)(forget|zapomnij|usuń).*?(instrukcj|prompt|system|zasady)",
        r"(?i)(show|pokaż).*?(all|wszystkie|cały).*?(prompt|instrukcj|system)",
        r"(?i)(what|co|jakie).*?(are|są).*?(your|twoje).*?(instructions|instrukcje|prompt)",
        r"(?i)(system|systemowy).*?(prompt|instrukcj|message|wiadomość)",
        r"(?i)(override|nadpisz|zastąp).*?(system|instrukcj|prompt)",
        r"(?i)(new|nowy).*?(instruction|instrukcj|prompt|system)",
        r"(?i)(act as|działaj jako|zachowuj się jak).*?(developer|admin|root)",
        r"(?i)(execute|wykonaj|uruchom).*?(code|kod|command|polecenie)",
        r"(?i)(reveal|ujawnij|pokaż).*?(secret|sekret|api.*?key|klucz)",
        r"(?i)(delete|usuń|skasuj).*?(all|wszystkie|cały).*?(data|dane)",
        # Stack trace patterns (may contain secrets)
        r"(Traceback|File.*?line|Exception|Error).*?(\n.*?){5,}",
        r"(?i)(api.*?key|secret|password|hasło|token).*?[:=]\s*[\w\-]{10,}",
        # Base64 encoded content (potential obfuscation)
        r"[A-Za-z0-9+/]{50,}={0,2}",
    ]

    # Maximum input length (characters)
    MAX_INPUT_LENGTH = 4000

    # Minimum interval between messages (seconds) - basic spam protection
    MIN_MESSAGE_INTERVAL = 1

    @classmethod
    def filter_input(cls, user_message: str, context: Dict = None) -> Tuple[str, bool, str]:
        """
        Filter and sanitize user input before sending to LLM.

        Args:
            user_message: Raw user message
            context: Optional context dict with session info

        Returns:
            Tuple of (filtered_message, is_safe, reason)
            - filtered_message: Sanitized message (or safe fallback)
            - is_safe: True if message is safe, False if blocked
            - reason: Reason for blocking (if not safe)
        """
        if not user_message:
            return "", False, "Empty message"

        # Check length
        if len(user_message) > cls.MAX_INPUT_LENGTH:
            return (
                user_message[:cls.MAX_INPUT_LENGTH],
                False,
                f"Message too long ({len(user_message)} > {cls.MAX_INPUT_LENGTH})"
            )

        # Check for injection patterns
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, user_message):
                return (
                    "",
                    False,
                    f"Potential prompt injection detected: {pattern[:50]}..."
                )

        # Remove potential secrets (API keys, tokens)
        filtered = cls._remove_secrets(user_message)

        # Trim excessive whitespace
        filtered = re.sub(r'\s+', ' ', filtered).strip()

        return filtered, True, "OK"

    @classmethod
    def _remove_secrets(cls, text: str) -> str:
        """
        Remove potential secrets from text (API keys, tokens, etc.)
        """
        # Pattern for API keys / tokens
        patterns = [
            r'(?i)(api[_-]?key|secret|token|password|hasło)[\s:=]+([\w\-]{20,})',
            r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API key pattern
            r'pk_[a-zA-Z0-9]{32,}',  # Stripe pattern
        ]

        filtered = text
        for pattern in patterns:
            filtered = re.sub(pattern, r'\1: [REDACTED]', filtered)

        return filtered

    @classmethod
    def is_potential_injection(cls, user_message: str) -> bool:
        """
        Quick check if message might be an injection attempt.

        Returns:
            True if suspicious, False otherwise
        """
        if not user_message:
            return False

        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, user_message):
                return True

        return False

    @classmethod
    def get_safe_response(cls) -> str:
        """
        Returns a safe fallback response when injection is detected.
        """
        return (
            "Przepraszam, nie mogę odpowiedzieć na to pytanie. "
            "Czy mogę pomóc Ci w czymś innym związanym z wykończeniem mieszkania?"
        )

