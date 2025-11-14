"""
Internationalization (i18n) Service
====================================
Multi-language support: PL (Polish), EN (English), DE (German)
Language detection and translation
"""

import re
from typing import Dict, Any, Optional, List
from langdetect import detect, LangDetectException

# Language translations dictionary
TRANSLATIONS = {
    'pl': {
        # Greetings
        'greeting': 'Cześć! Jestem asystentem NovaHouse. Jak mogę Ci pomóc?',
        'greeting_time_morning': 'Dzień dobry! Jestem asystentem NovaHouse. W czym mogę pomóc?',
        'greeting_time_evening': 'Dobry wieczór! Jestem asystentem NovaHouse. Jak mogę Ci pomóc?',
        
        # Quick actions
        'quick_action_portfolio': 'Zobacz portfolio',
        'quick_action_process': 'Jak działamy',
        'quick_action_pricing': 'Cennik',
        'quick_action_contact': 'Kontakt',
        
        # Bot responses
        'bot_name': 'Asystent NovaHouse',
        'help_message': 'Mogę odpowiedzieć na pytania o nasze usługi, cennik, portfolio, proces współpracy lub umówić spotkanie.',
        'error_message': 'Przepraszam, wystąpił błąd. Spróbuj ponownie lub napisz do nas na kontakt@novahouse.pl',
        'goodbye': 'Dziękuję za rozmowę! Do zobaczenia!',
        
        # Forms
        'form_name': 'Imię i nazwisko',
        'form_email': 'Email',
        'form_phone': 'Telefon',
        'form_message': 'Wiadomość',
        'form_submit': 'Wyślij',
        'form_success': 'Dziękujemy! Skontaktujemy się wkrótce.',
        
        # Services
        'service_renovation': 'Remonty',
        'service_finishing': 'Wykończenia',
        'service_design': 'Projektowanie',
        
        # Stats
        'stats_projects': 'Zrealizowanych projektów',
        'stats_satisfaction': 'Zadowolonych klientów',
        'stats_recommendations': 'Poleca nas',
        
        # Privacy
        'rodo_consent': 'Zgadzam się na przetwarzanie danych osobowych zgodnie z',
        'rodo_policy': 'Polityką Prywatności',
        
        # Booking
        'booking_title': 'Umów spotkanie',
        'booking_select_date': 'Wybierz datę',
        'booking_select_time': 'Wybierz godzinę',
        'booking_confirm': 'Potwierdź',
        'booking_success': 'Spotkanie umówione! Potwierdzenie zostało wysłane na Twój email.',
    },
    
    'en': {
        # Greetings
        'greeting': 'Hello! I\'m the NovaHouse assistant. How can I help you?',
        'greeting_time_morning': 'Good morning! I\'m the NovaHouse assistant. How can I help you?',
        'greeting_time_evening': 'Good evening! I\'m the NovaHouse assistant. How can I help you?',
        
        # Quick actions
        'quick_action_portfolio': 'View Portfolio',
        'quick_action_process': 'Our Process',
        'quick_action_pricing': 'Pricing',
        'quick_action_contact': 'Contact',
        
        # Bot responses
        'bot_name': 'NovaHouse Assistant',
        'help_message': 'I can answer questions about our services, pricing, portfolio, cooperation process, or schedule a meeting.',
        'error_message': 'Sorry, an error occurred. Please try again or email us at kontakt@novahouse.pl',
        'goodbye': 'Thank you for chatting! See you soon!',
        
        # Forms
        'form_name': 'Full Name',
        'form_email': 'Email',
        'form_phone': 'Phone',
        'form_message': 'Message',
        'form_submit': 'Submit',
        'form_success': 'Thank you! We\'ll contact you soon.',
        
        # Services
        'service_renovation': 'Renovation',
        'service_finishing': 'Finishing',
        'service_design': 'Design',
        
        # Stats
        'stats_projects': 'Completed Projects',
        'stats_satisfaction': 'Satisfied Clients',
        'stats_recommendations': 'Recommend Us',
        
        # Privacy
        'rodo_consent': 'I agree to the processing of personal data in accordance with',
        'rodo_policy': 'Privacy Policy',
        
        # Booking
        'booking_title': 'Schedule Meeting',
        'booking_select_date': 'Select Date',
        'booking_select_time': 'Select Time',
        'booking_confirm': 'Confirm',
        'booking_success': 'Meeting scheduled! Confirmation has been sent to your email.',
    },
    
    'de': {
        # Greetings
        'greeting': 'Hallo! Ich bin der NovaHouse-Assistent. Wie kann ich Ihnen helfen?',
        'greeting_time_morning': 'Guten Morgen! Ich bin der NovaHouse-Assistent. Wie kann ich Ihnen helfen?',
        'greeting_time_evening': 'Guten Abend! Ich bin der NovaHouse-Assistent. Wie kann ich Ihnen helfen?',
        
        # Quick actions
        'quick_action_portfolio': 'Portfolio ansehen',
        'quick_action_process': 'Unser Prozess',
        'quick_action_pricing': 'Preise',
        'quick_action_contact': 'Kontakt',
        
        # Bot responses
        'bot_name': 'NovaHouse-Assistent',
        'help_message': 'Ich kann Fragen zu unseren Dienstleistungen, Preisen, Portfolio, Zusammenarbeitsprozess beantworten oder ein Treffen vereinbaren.',
        'error_message': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut oder schreiben Sie uns an kontakt@novahouse.pl',
        'goodbye': 'Danke fürs Chatten! Bis bald!',
        
        # Forms
        'form_name': 'Vollständiger Name',
        'form_email': 'E-Mail',
        'form_phone': 'Telefon',
        'form_message': 'Nachricht',
        'form_submit': 'Absenden',
        'form_success': 'Vielen Dank! Wir werden Sie bald kontaktieren.',
        
        # Services
        'service_renovation': 'Renovierung',
        'service_finishing': 'Fertigstellung',
        'service_design': 'Design',
        
        # Stats
        'stats_projects': 'Abgeschlossene Projekte',
        'stats_satisfaction': 'Zufriedene Kunden',
        'stats_recommendations': 'Empfehlen uns',
        
        # Privacy
        'rodo_consent': 'Ich stimme der Verarbeitung personenbezogener Daten gemäß',
        'rodo_policy': 'Datenschutzrichtlinie',
        
        # Booking
        'booking_title': 'Termin vereinbaren',
        'booking_select_date': 'Datum wählen',
        'booking_select_time': 'Zeit wählen',
        'booking_confirm': 'Bestätigen',
        'booking_success': 'Termin vereinbart! Die Bestätigung wurde an Ihre E-Mail gesendet.',
    }
}

# FAQ translations
FAQ_TRANSLATIONS = {
    'pl': {
        'pricing': 'Cennik zależy od zakresu prac. Oferujemy pakiety S (do 50m²), M (50-100m²), L (powyżej 100m²). Napisz nam szczegóły, aby otrzymać wycenę!',
        'timeline': 'Standardowy remont trwa 6-12 tygodni w zależności od wielkości i zakresu. Jesteśmy znani z terminowości!',
        'services': 'Oferujemy kompleksowe remonty, wykończenia wnętrz, projektowanie, oraz doradztwo. Współpracujemy z 17 najlepszymi markami!',
        'process': 'Nasz proces: 1) Konsultacja i wycena 2) Projekt i plan 3) Realizacja 4) Odbiór. Proste i przejrzyste!',
    },
    'en': {
        'pricing': 'Pricing depends on the scope of work. We offer packages S (up to 50m²), M (50-100m²), L (over 100m²). Share details to get a quote!',
        'timeline': 'Standard renovation takes 6-12 weeks depending on size and scope. We\'re known for punctuality!',
        'services': 'We offer comprehensive renovations, interior finishing, design, and consulting. We work with 17 top brands!',
        'process': 'Our process: 1) Consultation & quote 2) Design & plan 3) Implementation 4) Handover. Simple and transparent!',
    },
    'de': {
        'pricing': 'Die Preise hängen vom Arbeitsumfang ab. Wir bieten Pakete S (bis 50m²), M (50-100m²), L (über 100m²). Teilen Sie Details für ein Angebot!',
        'timeline': 'Standard-Renovierung dauert 6-12 Wochen je nach Größe und Umfang. Wir sind für Pünktlichkeit bekannt!',
        'services': 'Wir bieten umfassende Renovierungen, Innenausbau, Design und Beratung. Wir arbeiten mit 17 Top-Marken!',
        'process': 'Unser Prozess: 1) Beratung & Angebot 2) Design & Plan 3) Umsetzung 4) Übergabe. Einfach und transparent!',
    }
}

class I18nService:
    """Internationalization service"""
    
    SUPPORTED_LANGUAGES = ['pl', 'en', 'de']
    DEFAULT_LANGUAGE = 'pl'
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language from text
        
        Args:
            text: Input text
            
        Returns:
            Language code ('pl', 'en', 'de') or default
        """
        try:
            # Use langdetect library
            detected = detect(text)
            
            # Map to supported languages
            if detected in I18nService.SUPPORTED_LANGUAGES:
                return detected
            
            # Fallback to default
            return I18nService.DEFAULT_LANGUAGE
            
        except LangDetectException:
            # If detection fails, try simple heuristics
            return I18nService._detect_language_heuristic(text)
    
    @staticmethod
    def _detect_language_heuristic(text: str) -> str:
        """Fallback language detection using keywords"""
        text_lower = text.lower()
        
        # Polish keywords
        pl_keywords = ['tak', 'nie', 'dzień dobry', 'cześć', 'proszę', 'dziękuję', 'remont', 'cennik']
        # English keywords
        en_keywords = ['yes', 'no', 'hello', 'hi', 'please', 'thank you', 'renovation', 'price']
        # German keywords
        de_keywords = ['ja', 'nein', 'hallo', 'bitte', 'danke', 'renovierung', 'preis']
        
        pl_score = sum(1 for kw in pl_keywords if kw in text_lower)
        en_score = sum(1 for kw in en_keywords if kw in text_lower)
        de_score = sum(1 for kw in de_keywords if kw in text_lower)
        
        max_score = max(pl_score, en_score, de_score)
        
        if max_score == 0:
            return I18nService.DEFAULT_LANGUAGE
        
        if pl_score == max_score:
            return 'pl'
        elif en_score == max_score:
            return 'en'
        else:
            return 'de'
    
    @staticmethod
    def translate(key: str, language: str = None) -> str:
        """
        Get translation for a key
        
        Args:
            key: Translation key (e.g., 'greeting', 'form_name')
            language: Target language code (pl/en/de)
            
        Returns:
            Translated string or key if not found
        """
        if not language or language not in I18nService.SUPPORTED_LANGUAGES:
            language = I18nService.DEFAULT_LANGUAGE
        
        translations = TRANSLATIONS.get(language, TRANSLATIONS[I18nService.DEFAULT_LANGUAGE])
        return translations.get(key, key)
    
    @staticmethod
    def translate_faq(intent: str, language: str = None) -> Optional[str]:
        """
        Get FAQ translation for an intent
        
        Args:
            intent: Intent name (pricing, timeline, services, etc.)
            language: Target language code
            
        Returns:
            Translated FAQ response or None
        """
        if not language or language not in I18nService.SUPPORTED_LANGUAGES:
            language = I18nService.DEFAULT_LANGUAGE
        
        faq = FAQ_TRANSLATIONS.get(language, FAQ_TRANSLATIONS[I18nService.DEFAULT_LANGUAGE])
        return faq.get(intent)
    
    @staticmethod
    def get_all_translations(language: str = None) -> Dict[str, str]:
        """
        Get all translations for a language
        
        Args:
            language: Target language code
            
        Returns:
            Dictionary of all translations
        """
        if not language or language not in I18nService.SUPPORTED_LANGUAGES:
            language = I18nService.DEFAULT_LANGUAGE
        
        return TRANSLATIONS.get(language, TRANSLATIONS[I18nService.DEFAULT_LANGUAGE])
    
    @staticmethod
    def translate_system_prompt(base_prompt: str, language: str) -> str:
        """
        Translate system prompt for chatbot
        
        Args:
            base_prompt: Base system prompt in Polish
            language: Target language
            
        Returns:
            Translated system prompt
        """
        if language == 'pl':
            return base_prompt
        
        # Language-specific system prompts
        system_prompts = {
            'en': """You are a helpful assistant for NovaHouse - a company specializing in comprehensive renovations and interior finishing in Warsaw, Poland.

Key Information:
- 30+ completed projects
- 95% client satisfaction rate
- 94% recommendation rate
- Coverage: Warsaw (Mokotów, Wilanów, Ochota), Piaseczno, Konstancin-Jeziorna
- Services: Complete renovations, Interior finishing, Design, Consulting
- Partners: 17 premium brands (Tubądzin, Paradyż, Cerrad, Opoczno, etc.)

Process:
1. Consultation & Quote (free)
2. Design & Planning
3. Implementation (with supervision)
4. Handover & Warranty

Be professional, friendly, and helpful. Focus on understanding client needs and guiding them through our services.""",
            
            'de': """Sie sind ein hilfreicher Assistent für NovaHouse - ein Unternehmen, das sich auf umfassende Renovierungen und Innenausbau in Warschau, Polen spezialisiert hat.

Wichtige Informationen:
- 30+ abgeschlossene Projekte
- 95% Kundenzufriedenheit
- 94% Empfehlungsrate
- Abdeckung: Warschau (Mokotów, Wilanów, Ochota), Piaseczno, Konstancin-Jeziorna
- Dienstleistungen: Komplette Renovierungen, Innenausbau, Design, Beratung
- Partner: 17 Premium-Marken (Tubądzin, Paradyż, Cerrad, Opoczno, etc.)

Prozess:
1. Beratung & Angebot (kostenlos)
2. Design & Planung
3. Umsetzung (mit Überwachung)
4. Übergabe & Garantie

Seien Sie professionell, freundlich und hilfsbereit. Konzentrieren Sie sich darauf, die Bedürfnisse des Kunden zu verstehen und ihn durch unsere Dienstleistungen zu führen."""
        }
        
        return system_prompts.get(language, base_prompt)
    
    @staticmethod
    def format_language_switcher() -> List[Dict[str, str]]:
        """
        Get language switcher data for UI
        
        Returns:
            List of language options with codes and names
        """
        return [
            {'code': 'pl', 'name': 'Polski', 'flag': '🇵🇱'},
            {'code': 'en', 'name': 'English', 'flag': '🇬🇧'},
            {'code': 'de', 'name': 'Deutsch', 'flag': '🇩🇪'}
        ]
