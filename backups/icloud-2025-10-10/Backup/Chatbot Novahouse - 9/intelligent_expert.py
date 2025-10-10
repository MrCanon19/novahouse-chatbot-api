"""
Inteligentny ekspert NovaHouse - zaawansowana analiza kontekstu i przewidywanie potrzeb
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class IntelligentExpert:
    """Inteligentny ekspert z zaawansowaną analizą kontekstu"""
    
    def __init__(self):
        self.context_patterns = self._load_context_patterns()
        self.smart_responses = self._load_smart_responses()
        self.client_profiles = self._load_client_profiles()
    
    def _load_context_patterns(self) -> Dict:
        """Wzorce kontekstowe do rozpoznawania sytuacji klienta"""
        return {
            "first_time_buyer": {
                "keywords": ["pierwszy raz", "nie wiem", "nie znam się", "początkujący", "nowy"],
                "indicators": ["jak to działa", "od czego zacząć", "co powinienem wiedzieć"]
            },
            "budget_conscious": {
                "keywords": ["tani", "najtańszy", "oszczędność", "budżet", "nie stać", "za drogo"],
                "indicators": ["ile minimum", "czy można taniej", "podstawowy pakiet"]
            },
            "quality_focused": {
                "keywords": ["najlepszy", "premium", "jakość", "trwałość", "solidny", "ekskluzywny"],
                "indicators": ["nie oszczędzam", "zależy mi na jakości", "najdroższy"]
            },
            "time_pressed": {
                "keywords": ["szybko", "pilnie", "natychmiast", "jak najszybciej", "termin"],
                "indicators": ["muszę się wprowadzić", "deadline", "czas nagli"]
            },
            "experienced_renovator": {
                "keywords": ["już robiłem", "wiem jak", "doświadczenie", "kolejny remont"],
                "indicators": ["porównuję", "sprawdzam", "analizuję opcje"]
            },
            "family_oriented": {
                "keywords": ["dzieci", "rodzina", "bezpieczny", "ekologiczny", "zdrowy"],
                "indicators": ["dla dziecka", "pokój dziecięcy", "bezpieczeństwo"]
            },
            "investment_minded": {
                "keywords": ["inwestycja", "wynajem", "sprzedaż", "wartość", "zwrot"],
                "indicators": ["pod wynajem", "na sprzedaż", "ROI", "opłacalność"]
            }
        }
    
    def _load_smart_responses(self) -> Dict:
        """Inteligentne odpowiedzi dostosowane do profilu klienta"""
        return {
            "first_time_buyer": {
                "tone": "edukacyjny, cierpliwy, szczegółowy",
                "approach": "krok po kroku, wyjaśnianie podstaw",
                "recommendations": "Pakiet Pomarańczowy - optymalny na start",
                "warnings": "Unikaj najtańszych opcji - będziesz żałować",
                "next_steps": "Zacznijmy od bezpłatnej konsultacji"
            },
            "budget_conscious": {
                "tone": "praktyczny, oszczędny, konkretny",
                "approach": "maksymalna wartość za pieniądze",
                "recommendations": "Pakiet Waniliowy + selektywne ulepszenia",
                "warnings": "Nie oszczędzaj na instalacjach - to się nie opłaca",
                "next_steps": "Pokażę Ci jak zoptymalizować koszty"
            },
            "quality_focused": {
                "tone": "eksperci, prestiżowy, szczegółowy",
                "approach": "najlepsze materiały i wykonanie",
                "recommendations": "Pakiet Cynamonowy lub Szafranowy",
                "warnings": "Jakość ma swoją cenę, ale się opłaca",
                "next_steps": "Przedstawię Ci premium opcje"
            },
            "time_pressed": {
                "tone": "sprawny, konkretny, zorientowany na działanie",
                "approach": "szybkie decyzje, jasne terminy",
                "recommendations": "Pakiet gotowy do realizacji",
                "warnings": "Pośpiech może kosztować - planuj z wyprzedzeniem",
                "next_steps": "Sprawdzę dostępne terminy"
            },
            "experienced_renovator": {
                "tone": "profesjonalny, techniczny, szczegółowy",
                "approach": "konkretne specyfikacje, porównania",
                "recommendations": "Dostosowany pakiet według doświadczenia",
                "warnings": "Każdy projekt jest inny - nie zakładaj",
                "next_steps": "Omówmy szczegóły techniczne"
            },
            "family_oriented": {
                "tone": "troskliwy, bezpieczny, odpowiedzialny",
                "approach": "bezpieczeństwo i komfort rodziny",
                "recommendations": "Materiały bezpieczne dla dzieci",
                "warnings": "Nie oszczędzaj na bezpieczeństwie",
                "next_steps": "Pokażę Ci rodzinne rozwiązania"
            },
            "investment_minded": {
                "tone": "biznesowy, analityczny, ROI-focused",
                "approach": "zwrot z inwestycji, wartość rynkowa",
                "recommendations": "Pakiet zwiększający wartość nieruchomości",
                "warnings": "Nie przeinwestowuj - znajdź balans",
                "next_steps": "Przeanalizujemy opłacalność"
            }
        }
    
    def _load_client_profiles(self) -> Dict:
        """Profile klientów z typowymi potrzebami"""
        return {
            "młoda_para": {
                "typical_budget": "80-150k",
                "typical_size": "40-70m2",
                "priorities": ["nowoczesność", "funkcjonalność", "budżet"],
                "concerns": ["pierwszy remont", "ograniczony budżet", "praktyczność"],
                "recommendations": "Pakiet Pomarańczowy - idealny balans"
            },
            "rodzina_z_dziećmi": {
                "typical_budget": "120-250k",
                "typical_size": "60-100m2",
                "priorities": ["bezpieczeństwo", "trwałość", "funkcjonalność"],
                "concerns": ["materiały bezpieczne", "łatwość czyszczenia", "hałas"],
                "recommendations": "Pakiet Cynamonowy - trwały i bezpieczny"
            },
            "singiel_profesjonalista": {
                "typical_budget": "100-200k",
                "typical_size": "30-60m2",
                "priorities": ["design", "jakość", "wygoda"],
                "concerns": ["estetyka", "funkcjonalność", "czas realizacji"],
                "recommendations": "Pakiet Cynamonowy - stylowy i funkcjonalny"
            },
            "inwestor": {
                "typical_budget": "60-120k",
                "typical_size": "40-80m2",
                "priorities": ["ROI", "uniwersalność", "szybkość"],
                "concerns": ["koszty", "atrakcyjność dla najemców", "trwałość"],
                "recommendations": "Pakiet Pomarańczowy - optymalny ROI"
            },
            "senior": {
                "typical_budget": "150-300k",
                "typical_size": "60-120m2",
                "priorities": ["komfort", "bezpieczeństwo", "jakość"],
                "concerns": ["dostępność", "łatwość użytkowania", "trwałość"],
                "recommendations": "Pakiet Szafranowy - komfort i bezpieczeństwo"
            }
        }
    
    def analyze_client_context(self, message: str, entities: Dict) -> Dict:
        """Analiza kontekstu klienta na podstawie wiadomości i encji"""
        
        context = {
            "client_type": self._identify_client_type(message, entities),
            "urgency_level": self._assess_urgency(message),
            "budget_range": self._estimate_budget_range(message, entities),
            "experience_level": self._assess_experience(message),
            "main_concerns": self._identify_concerns(message),
            "decision_stage": self._assess_decision_stage(message)
        }
        
        return context
    
    def _identify_client_type(self, message: str, entities: Dict) -> str:
        """Identyfikacja typu klienta"""
        message_lower = message.lower()
        
        # Sprawdź bezpośrednie wskazówki
        if any(word in message_lower for word in ["para", "razem", "narzeczeni", "małżeństwo"]):
            return "młoda_para"
        elif any(word in message_lower for word in ["dzieci", "dziecko", "rodzina", "syn", "córka"]):
            return "rodzina_z_dziećmi"
        elif any(word in message_lower for word in ["inwestycja", "wynajem", "sprzedaż", "ROI"]):
            return "inwestor"
        elif any(word in message_lower for word in ["emeryt", "senior", "wiek", "starszy"]):
            return "senior"
        
        # Analiza na podstawie budżetu i metrażu
        budget = entities.get('budżet_klienta', '')
        metraz = entities.get('metraz_mieszkania', '')
        
        if budget and metraz:
            budget_num = self._extract_number(budget)
            metraz_num = self._extract_number(metraz)
            
            if budget_num and metraz_num:
                ratio = budget_num / metraz_num
                if ratio < 1500:
                    return "inwestor"
                elif ratio > 3000:
                    return "senior"
                elif metraz_num < 50:
                    return "singiel_profesjonalista"
        
        return "młoda_para"  # domyślny
    
    def _assess_urgency(self, message: str) -> str:
        """Ocena pilności projektu"""
        message_lower = message.lower()
        
        high_urgency = ["pilnie", "szybko", "natychmiast", "jak najszybciej", "deadline", "termin"]
        medium_urgency = ["niedługo", "wkrótce", "planujemy", "chcemy zacząć"]
        
        if any(word in message_lower for word in high_urgency):
            return "wysoka"
        elif any(word in message_lower for word in medium_urgency):
            return "średnia"
        else:
            return "niska"
    
    def _estimate_budget_range(self, message: str, entities: Dict) -> str:
        """Oszacowanie zakresu budżetowego"""
        budget = entities.get('budżet_klienta', '')
        if budget:
            return budget
        
        # Analiza kontekstowa
        message_lower = message.lower()
        if any(word in message_lower for word in ["tani", "najtańszy", "oszczędność", "minimum"]):
            return "budżetowy (do 100k)"
        elif any(word in message_lower for word in ["średni", "normalny", "standardowy"]):
            return "średni (100-200k)"
        elif any(word in message_lower for word in ["premium", "najlepszy", "ekskluzywny", "nie oszczędzam"]):
            return "wysoki (200k+)"
        
        return "do ustalenia"
    
    def _assess_experience(self, message: str) -> str:
        """Ocena doświadczenia klienta"""
        message_lower = message.lower()
        
        experienced = ["już robiłem", "doświadczenie", "wiem jak", "kolejny remont", "porównuję"]
        beginner = ["pierwszy raz", "nie wiem", "nie znam się", "początkujący", "jak to działa"]
        
        if any(phrase in message_lower for phrase in experienced):
            return "doświadczony"
        elif any(phrase in message_lower for phrase in beginner):
            return "początkujący"
        else:
            return "średni"
    
    def _identify_concerns(self, message: str) -> List[str]:
        """Identyfikacja głównych obaw klienta"""
        concerns = []
        message_lower = message.lower()
        
        concern_map = {
            "budżet": ["koszt", "cena", "drogo", "budżet", "oszczędność"],
            "czas": ["jak długo", "kiedy", "termin", "szybko", "czas"],
            "jakość": ["jakość", "trwałość", "solidny", "dobry", "najlepszy"],
            "bezpieczeństwo": ["bezpieczny", "dzieci", "zdrowy", "ekologiczny"],
            "design": ["wygląd", "piękny", "nowoczesny", "stylowy", "design"],
            "praktyczność": ["funkcjonalny", "praktyczny", "wygodny", "użyteczny"]
        }
        
        for concern, keywords in concern_map.items():
            if any(keyword in message_lower for keyword in keywords):
                concerns.append(concern)
        
        return concerns if concerns else ["ogólne"]
    
    def _assess_decision_stage(self, message: str) -> str:
        """Ocena etapu decyzyjnego"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["umówić", "spotkanie", "kiedy zaczynamy", "decydujemy"]):
            return "gotowy do decyzji"
        elif any(word in message_lower for word in ["porównuję", "sprawdzam", "analizuję", "rozważam"]):
            return "porównywanie opcji"
        elif any(word in message_lower for word in ["ile kosztuje", "jaka cena", "cennik"]):
            return "zbieranie informacji"
        else:
            return "wstępne zainteresowanie"
    
    def generate_intelligent_response(self, message: str, intent: str, entities: Dict, context: Dict) -> str:
        """Generowanie inteligentnej odpowiedzi na podstawie kontekstu"""
        
        client_type = context.get('client_type', 'młoda_para')
        urgency = context.get('urgency_level', 'niska')
        concerns = context.get('main_concerns', ['ogólne'])
        decision_stage = context.get('decision_stage', 'wstępne zainteresowanie')
        
        # Pobierz profil klienta
        profile = self.client_profiles.get(client_type, self.client_profiles['młoda_para'])
        
        # Buduj odpowiedź
        response_parts = []
        
        # Personalizowane powitanie
        if decision_stage == "wstępne zainteresowanie":
            response_parts.append(self._get_personalized_greeting(client_type))
        
        # Główna treść odpowiedzi
        if intent in ['wycena_konkretna', 'zapytanie_o_pakiety']:
            response_parts.append(self._get_pricing_response(client_type, entities, context))
        elif intent == 'umowienie_spotkania':
            response_parts.append(self._get_meeting_response(urgency, client_type))
        elif intent in ['porady_eksperckie', 'porownanie_pakietow']:
            response_parts.append(self._get_expert_advice(client_type, concerns))
        else:
            response_parts.append(self._get_general_response(client_type, concerns))
        
        # Proaktywne sugestie
        response_parts.append(self._get_proactive_suggestions(context, entities))
        
        return "\n\n".join(filter(None, response_parts))
    
    def _get_personalized_greeting(self, client_type: str) -> str:
        """Personalizowane powitanie"""
        greetings = {
            "młoda_para": "Świetnie, że planujecie swoje pierwsze wspólne mieszkanie! 💕",
            "rodzina_z_dziećmi": "Rozumiem, jak ważne jest stworzenie bezpiecznego domu dla rodziny 👨‍👩‍👧‍👦",
            "singiel_profesjonalista": "Doskonały moment na stworzenie idealnej przestrzeni do życia i pracy 🏢",
            "inwestor": "Inteligentne podejście do inwestycji w nieruchomości 📈",
            "senior": "Cieszę się, że myślicie o komfortowym i bezpiecznym wnętrzu 🏡"
        }
        return greetings.get(client_type, "")
    
    def _get_pricing_response(self, client_type: str, entities: Dict, context: Dict) -> str:
        """Odpowiedź cenowa dostosowana do profilu"""
        profile = self.client_profiles[client_type]
        
        response = f"**Dla {client_type.replace('_', ' ')} polecam:**\n\n"
        response += f"🎯 **{profile['recommendations']}**\n\n"
        
        # Dodaj konkretne ceny jeśli mamy metraż
        metraz = entities.get('metraz_mieszkania', '')
        if metraz:
            metraz_num = self._extract_number(metraz)
            if metraz_num:
                response += self._calculate_specific_prices(metraz_num, client_type)
        
        # Dodaj ostrzeżenia specyficzne dla profilu
        response += f"\n⚠️ **Ważne:** {profile['concerns'][0]} - {self._get_specific_warning(client_type)}"
        
        return response
    
    def _get_meeting_response(self, urgency: str, client_type: str) -> str:
        """Odpowiedź na prośbę o spotkanie"""
        if urgency == "wysoka":
            return "Rozumiem pilność! Sprawdzę dostępność na najbliższe dni. Możemy umówić się nawet jutro."
        elif urgency == "średnia":
            return "Świetnie! Umówimy się w dogodnym dla Ciebie terminie w ciągu tygodnia."
        else:
            return "Doskonale! Mamy elastyczne terminy - wybierzemy najlepszy dla Ciebie."
    
    def _get_expert_advice(self, client_type: str, concerns: List[str]) -> str:
        """Ekspercka porada dostosowana do profilu"""
        profile = self.client_profiles[client_type]
        
        advice = f"**Moja ekspercka rada dla {client_type.replace('_', ' ')}:**\n\n"
        
        # Główne priorytety
        priorities = profile['priorities']
        advice += f"🎯 **Twoje priorytety:** {', '.join(priorities)}\n\n"
        
        # Specyficzne porady
        if "budżet" in concerns:
            advice += "💰 **Optymalizacja budżetu:** Lepiej mniejszy metraż w wyższym standardzie niż większy w niskim\n\n"
        
        if "jakość" in concerns:
            advice += "⭐ **Jakość:** Inwestuj w instalacje i materiały podstawowe - to się zwraca\n\n"
        
        if "czas" in concerns:
            advice += "⏰ **Czas realizacji:** Planuj z 20% buforem - lepiej być przygotowanym\n\n"
        
        return advice
    
    def _get_general_response(self, client_type: str, concerns: List[str]) -> str:
        """Ogólna odpowiedź dostosowana do profilu"""
        profile = self.client_profiles[client_type]
        
        response = f"**Idealnie dopasowane rozwiązanie:**\n\n"
        response += f"📋 **Typowy budżet:** {profile['typical_budget']}\n"
        response += f"📐 **Typowy metraż:** {profile['typical_size']}\n"
        response += f"🎯 **Rekomendacja:** {profile['recommendations']}\n\n"
        
        return response
    
    def _get_proactive_suggestions(self, context: Dict, entities: Dict) -> str:
        """Proaktywne sugestie następnych kroków"""
        decision_stage = context.get('decision_stage', '')
        
        if decision_stage == "gotowy do decyzji":
            return "🚀 **Następny krok:** Umówmy bezpłatną konsultację - przygotujemy szczegółową wycenę"
        elif decision_stage == "porównywanie opcji":
            return "📊 **Pomogę Ci:** Porównajmy konkretne opcje - pokażę różnice w praktyce"
        elif decision_stage == "zbieranie informacji":
            return "💡 **Sugestia:** Podaj metraż i lokalizację - dam Ci precyzyjną kalkulację"
        else:
            return "❓ **Masz pytania?** Napisz konkretnie czego potrzebujesz - odpowiem profesjonalnie"
    
    def _calculate_specific_prices(self, metraz: int, client_type: str) -> str:
        """Kalkulacja konkretnych cen"""
        packages = {
            "Waniliowy": (1200, 1500),
            "Pomarańczowy": (1800, 2200),
            "Cynamonowy": (2500, 3000),
            "Szafranowy": (3500, 4500)
        }
        
        response = "**Konkretne kalkulacje dla Twojego metrażu:**\n\n"
        
        for package, (min_price, max_price) in packages.items():
            min_total = metraz * min_price
            max_total = metraz * max_price
            response += f"• **{package}:** {min_total:,} - {max_total:,} zł\n"
        
        return response
    
    def _get_specific_warning(self, client_type: str) -> str:
        """Specyficzne ostrzeżenie dla typu klienta"""
        warnings = {
            "młoda_para": "nie oszczędzajcie na instalacjach - to podstawa",
            "rodzina_z_dziećmi": "bezpieczeństwo dzieci to priorytet",
            "singiel_profesjonalista": "jakość materiałów wpływa na komfort życia",
            "inwestor": "nie przeinwestowuj - znajdź optymalny balans",
            "senior": "komfort użytkowania to najważniejsze"
        }
        return warnings.get(client_type, "jakość to inwestycja w przyszłość")
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Wyciągnięcie liczby z tekstu"""
        numbers = re.findall(r'\d+', str(text))
        return int(numbers[0]) if numbers else None

# Globalna instancja
intelligent_expert = IntelligentExpert()
