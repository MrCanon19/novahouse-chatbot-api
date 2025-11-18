"""
NovaHouse Knowledge Base System
Ekspert z 40-letnim doświadczeniem - implementacja RAG z OpenAI
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from openai import OpenAI
import tiktoken
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import logging

# Konfiguracja OpenAI - lazy loading
def get_openai_client():
    """Lazy loading OpenAI client"""
    try:
        return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    except Exception as e:
        logging.error(f"Błąd inicjalizacji OpenAI client: {e}")
        return None

class NovaHouseKnowledgeBase:
    """Inteligentna baza wiedzy NovaHouse z RAG (Retrieval-Augmented Generation)"""
    
    def __init__(self):
        self.knowledge_chunks = []
        self.embeddings = []
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.max_chunk_size = 1000
        self.overlap_size = 200
        
        # Inicjalizacja bazy wiedzy
        self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """Ładowanie i przetwarzanie bazy wiedzy NovaHouse"""
        
        # Podstawowa wiedza o NovaHouse
        base_knowledge = {
            "firma": {
                "nazwa": "NovaHouse",
                "specjalizacja": "Wykończenia wnętrz i domy pasywne",
                "doświadczenie": "Wieloletnie doświadczenie w branży budowlanej",
                "lokalizacja": "Polska"
            },
            
            "pakiety_wykonczeniowe": {
                "comfort": {
                    "nazwa": "Comfort",
                    "opis": "Pakiet podstawowy z wysokiej jakości materiałami",
                    "zakres": "Kompleksowe wykończenie mieszkania",
                    "metraż": "Do 40m²",
                    "czas_realizacji": "4-6 tygodni",
                    "materiały": "Wysokiej jakości materiały wykończeniowe"
                },
                "express_plus": {
                    "nazwa": "Express Plus + Z2",
                    "opis": "Pakiet premium z dodatkowymi udogodnieniami",
                    "zakres": "Kompleksowe wykończenie z dodatkami",
                    "metraż": "Do 90m²",
                    "czas_realizacji": "6-10 tygodni",
                    "materiały": "Materiały premium z dodatkowymi opcjami"
                }
            },
            
            "usługi": {
                "konsultacje": {
                    "rodzaje": ["Konsultacja z projektantem", "Wycena", "Prezentacja materiałów"],
                    "formy": ["Stacjonarne", "Online", "W showroomie"],
                    "rezerwacja": "Przez Booksy lub bezpośredni kontakt"
                },
                "realizacja": {
                    "etapy": [
                        "Projekt i planowanie (1 tydzień)",
                        "Praca przygotowawcza (1-2 dni)",
                        "Instalacje (1-2 tygodnie)",
                        "Wykończenia (2-4 tygodnie)",
                        "Odbiór i sprzątanie (1-2 dni)"
                    ]
                }
            },
            
            "kontakt": {
                "kanały": ["WhatsApp", "Instagram", "Email", "Formularze", "LinkedIn (wkrótce)"],
                "czas_odpowiedzi": "24 godziny w dni robocze",
                "showroom": "Dostępny do wizyt po umówieniu"
            },
            
            "proces_obsługi": {
                "krok_1": "Pierwsza konsultacja i określenie potrzeb",
                "krok_2": "Przygotowanie wyceny i propozycji",
                "krok_3": "Podpisanie umowy i harmonogram",
                "krok_4": "Realizacja prac zgodnie z harmonogramem",
                "krok_5": "Odbiór i gwarancja"
            }
        }
        
        # Konwersja do chunks
        for category, data in base_knowledge.items():
            chunk_text = f"Kategoria: {category}\n"
            chunk_text += self._dict_to_text(data)
            
            self.knowledge_chunks.append({
                "text": chunk_text,
                "category": category,
                "source": "base_knowledge",
                "timestamp": datetime.now().isoformat()
            })
    
    def _dict_to_text(self, data: Dict, prefix: str = "") -> str:
        """Konwersja słownika do tekstu"""
        text = ""
        for key, value in data.items():
            if isinstance(value, dict):
                text += f"{prefix}{key}:\n"
                text += self._dict_to_text(value, prefix + "  ")
            elif isinstance(value, list):
                text += f"{prefix}{key}: {', '.join(map(str, value))}\n"
            else:
                text += f"{prefix}{key}: {value}\n"
        return text
    
    def add_knowledge_from_file(self, file_path: str, category: str = "external"):
        """Dodawanie wiedzy z pliku"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Podział na chunki
            chunks = self._split_into_chunks(content)
            
            for i, chunk in enumerate(chunks):
                self.knowledge_chunks.append({
                    "text": chunk,
                    "category": category,
                    "source": os.path.basename(file_path),
                    "chunk_id": i,
                    "timestamp": datetime.now().isoformat()
                })
                
            logging.info(f"Dodano {len(chunks)} chunków z pliku {file_path}")
            
        except Exception as e:
            logging.error(f"Błąd podczas ładowania pliku {file_path}: {e}")
    
    def _split_into_chunks(self, text: str) -> List[str]:
        """Podział tekstu na chunki z nakładaniem"""
        chunks = []
        
        # Oczyszczenie tekstu
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Podział na paragrafy
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        current_size = 0
        
        for paragraph in paragraphs:
            paragraph_size = len(self.encoding.encode(paragraph))
            
            if current_size + paragraph_size > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                
                # Nakładanie - zachowaj ostatnie zdania
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + "\n\n" + paragraph
                current_size = len(self.encoding.encode(current_chunk))
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                current_size += paragraph_size
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _get_overlap(self, text: str) -> str:
        """Pobieranie tekstu do nakładania"""
        sentences = text.split('.')
        overlap = ""
        overlap_size = 0
        
        for sentence in reversed(sentences):
            sentence_size = len(self.encoding.encode(sentence))
            if overlap_size + sentence_size > self.overlap_size:
                break
            overlap = sentence + "." + overlap
            overlap_size += sentence_size
        
        return overlap.strip()
    
    async def get_embedding(self, text: str) -> List[float]:
        """Pobieranie embeddingu z OpenAI"""
        try:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logging.error(f"Błąd podczas pobierania embeddingu: {e}")
            return []
    
    def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """Wyszukiwanie w bazie wiedzy"""
        if not self.knowledge_chunks:
            return []
        
        # Dla uproszczenia - wyszukiwanie tekstowe
        # W produkcji użyj embeddings
        query_lower = query.lower()
        results = []
        
        for chunk in self.knowledge_chunks:
            text_lower = chunk["text"].lower()
            
            # Proste scorowanie na podstawie wystąpień słów
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in text_lower:
                    score += text_lower.count(word)
            
            if score > 0:
                results.append({
                    **chunk,
                    "score": score
                })
        
        # Sortowanie według score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """Generowanie odpowiedzi z wykorzystaniem OpenAI"""
        
        # Przygotowanie kontekstu
        context = "\n\n".join([chunk["text"] for chunk in context_chunks])
        
        system_prompt = """Jesteś ekspertem chatbotem NovaHouse - firmy specjalizującej się w wykończeniach wnętrz i domach pasywnych.

Twoim zadaniem jest udzielanie pomocnych, dokładnych i przyjaznych odpowiedzi na pytania klientów.

Zasady:
1. Używaj informacji z podanego kontekstu
2. Jeśli nie masz informacji, powiedz to wprost
3. Bądź konkretny i pomocny
4. Zachęcaj do kontaktu z konsultantem przy złożonych pytaniach
5. Używaj polskiego języka
6. Bądź profesjonalny ale ciepły w tonie

Kontekst z bazy wiedzy:
{context}

Odpowiadaj na pytanie klienta w oparciu o powyższy kontekst."""

        user_prompt = f"Pytanie klienta: {query}"
        
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """Generowanie odpowiedzi - hybrydowe (OpenAI + fallback)"""
        
        # Przygotowanie kontekstu
        context = "\n\n".join([chunk["text"] for chunk in context_chunks])
        
        # Próba użycia OpenAI (jeśli dostępne)
        try:
            client = get_openai_client()
            if client:
                system_prompt = """Jesteś ekspertem chatbotem NovaHouse - firmy specjalizującej się w wykończeniach wnętrz i domach pasywnych.

Twoim zadaniem jest udzielanie pomocnych, dokładnych i przyjaznych odpowiedzi na pytania klientów.

Zasady:
1. Używaj informacji z podanego kontekstu
2. Jeśli nie masz informacji, powiedz to wprost
3. Bądź konkretny i pomocny
4. Zachęcaj do kontaktu z konsultantem przy złożonych pytaniach
5. Używaj polskiego języka
6. Bądź profesjonalny ale ciepły w tonie

Kontekst z bazy wiedzy:
{context}

Odpowiadaj na pytanie klienta w oparciu o powyższy kontekst."""

                user_prompt = f"Pytanie klienta: {query}"
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt.format(context=context)},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            logging.info(f"OpenAI niedostępne, używam lokalnej bazy wiedzy: {e}")
        
        # Fallback - inteligentne odpowiedzi bez OpenAI
        return self._generate_intelligent_fallback(query, context_chunks)
    
    def _generate_intelligent_fallback(self, query: str, context_chunks: List[Dict]) -> str:
        """Inteligentne odpowiedzi bez OpenAI - wykorzystanie bazy wiedzy"""
        
        query_lower = query.lower()
        
        # Analiza intencji na podstawie słów kluczowych
        if any(word in query_lower for word in ['pakiet', 'pakiety', 'wykończenie', 'standard']):
            return self._handle_packages_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['cena', 'koszt', 'ile', 'cennik', 'wycena']):
            return self._handle_price_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['czas', 'długo', 'realizacja', 'harmonogram']):
            return self._handle_time_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['kontakt', 'telefon', 'email', 'adres']):
            return self._handle_contact_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['konsultacja', 'spotkanie', 'umówić', 'wizyta']):
            return self._handle_consultation_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['materiały', 'materiał', 'jakość']):
            return self._handle_materials_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['showroom', 'salon', 'wystawa']):
            return self._handle_showroom_question(query_lower, context_chunks)
        
        elif any(word in query_lower for word in ['pasywny', 'dom', 'budowa']):
            return self._handle_passive_house_question(query_lower, context_chunks)
        
        else:
            # Ogólna odpowiedź z kontekstem
            if context_chunks:
                relevant_info = context_chunks[0]["text"][:300] + "..."
                return f"""Na podstawie naszej bazy wiedzy mogę powiedzieć:

{relevant_info}

Czy chciałbyś dowiedzieć się więcej o konkretnym aspekcie? Mogę pomóc z:
• Pakietami wykończeniowymi
• Cenami i wycenami  
• Harmonogramem realizacji
• Umówieniem konsultacji

Napisz "konsultant" aby porozmawiać z naszym ekspertem!"""
            
            return """Dziękuję za pytanie! Jestem chatbotem NovaHouse i mogę pomóc Ci z:

🏠 **Pakietami wykończeniowymi** - Comfort, Express Plus i inne
💰 **Wycenami i cenami** - indywidualne kalkulacje
⏰ **Harmonogramami realizacji** - planowanie prac
📞 **Kontaktem z zespołem** - umówienie konsultacji
🎨 **Materiałami i standardami** - jakość wykończeń

**Napisz konkretne pytanie lub wybierz temat!**"""
    
    def _handle_packages_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o pakietach wykończeniowych"""
        
        if 'comfort' in query:
            return """🟡 **Pakiet Comfort** to nasz podstawowy standard z wysokiej jakości materiałami:

✅ **Zakres:** Kompleksowe wykończenie mieszkania
✅ **Metraż:** Idealny do 40m²  
✅ **Czas realizacji:** 4-6 tygodni
✅ **Materiały:** Wysokiej jakości wykończenia
✅ **Gwarancja:** Pełna gwarancja na wykonane prace

Pakiet można dostosować do Twoich potrzeb. Chcesz poznać szczegóły lub porównać z innymi pakietami?

**Napisz "wycena" aby otrzymać indywidualną ofertę!**"""
        
        elif 'express' in query:
            return """🟠 **Pakiet Express Plus + Z2** to nasz standard premium:

✅ **Zakres:** Kompleksowe wykończenie z dodatkami
✅ **Metraż:** Do 90m²
✅ **Czas realizacji:** 6-10 tygodni  
✅ **Materiały:** Premium z dodatkowymi opcjami
✅ **Dodatkowe udogodnienia:** Rozszerzone możliwości

Idealny dla większych mieszkań i wymagających klientów.

**Chcesz poznać szczegóły lub umówić prezentację materiałów?**"""
        
        else:
            return """🏠 **Nasze pakiety wykończeniowe NovaHouse:**

🟡 **Pakiet Comfort** - podstawowy standard (do 40m², 4-6 tygodni)
🟠 **Pakiet Express Plus + Z2** - premium (do 90m², 6-10 tygodni)

**Każdy pakiet zawiera:**
• Kompleksowe wykończenie mieszkania
• Wysokiej jakości materiały
• Profesjonalne wykonanie
• Pełną gwarancję
• Możliwość personalizacji

**O którym pakiecie chciałbyś dowiedzieć się więcej?**
Napisz "Comfort" lub "Express Plus" dla szczegółów!"""
    
    def _handle_price_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o cenach"""
        return """💰 **Ceny pakietów NovaHouse:**

Nasze ceny są **indywidualnie kalkulowane** w zależności od:
• Metrażu mieszkania
• Wybranego pakietu (Comfort / Express Plus)
• Zakresu personalizacji
• Lokalizacji obiektu

**🎯 Jak otrzymać wycenę:**
1. **Bezpłatna konsultacja** - omówimy Twoje potrzeby
2. **Pomiar mieszkania** - dokładne wymiary
3. **Prezentacja materiałów** - wybór standardu
4. **Indywidualna wycena** - transparentne koszty

**📞 Umów bezpłatną konsultację:**
Napisz "konsultacja" lub skontaktuj się z nami bezpośrednio!

*Pierwsza konsultacja i wycena są całkowicie bezpłatne!*"""
    
    def _handle_time_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o czasie realizacji"""
        return """⏰ **Czas realizacji NovaHouse:**

**📏 Według metrażu:**
• **Do 40m²:** 4-6 tygodni (Pakiet Comfort)
• **40-90m²:** 6-10 tygodni (Express Plus)
• **Powyżej 90m²:** Indywidualny harmonogram

**🔧 Etapy realizacji:**
1. **Projekt i planowanie** (1 tydzień)
2. **Prace przygotowawcze** (1-2 dni)  
3. **Instalacje** (1-2 tygodnie)
4. **Wykończenia** (2-4 tygodnie)
5. **Odbiór i sprzątanie** (1-2 dni)

**⚡ Przyspieszenie możliwe** przy odpowiedniej organizacji!

Podaj metraż swojego mieszkania, a określimy dokładny harmonogram dla Twojego projektu!"""
    
    def _handle_contact_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o kontakcie"""
        return """📞 **Kontakt z NovaHouse:**

**🌐 Dostępne kanały:**
• **WhatsApp** - szybki kontakt
• **Instagram** - galeria realizacji  
• **Email** - szczegółowe zapytania
• **Formularze** - wygodne zgłoszenia
• **LinkedIn** - kontakt biznesowy (wkrótce)

**⏰ Czas odpowiedzi:** 24 godziny w dni robocze

**🏢 Showroom:** Dostępny po umówieniu wizyty

**💬 Najszybszy kontakt:**
Napisz "konsultant" a przekażę Cię do odpowiedniej osoby, która pomoże Ci z konkretnymi pytaniami!

*Jesteśmy dostępni i chętnie pomożemy!* 😊"""
    
    def _handle_consultation_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o konsultacjach"""
        return """📅 **Konsultacje NovaHouse:**

**🎯 Rodzaje konsultacji:**
• **Konsultacja z projektantem** - planowanie wnętrza
• **Wycena** - kalkulacja kosztów
• **Prezentacja materiałów** - wybór standardu

**📍 Formy spotkań:**
• **Stacjonarne** - w naszym showroomie
• **Online** - wygodnie z domu
• **W showroomie** - z prezentacją materiałów

**📞 Rezerwacja:**
• Przez Booksy (system rezerwacji)
• Bezpośredni kontakt z zespołem
• Formularz na stronie

**💰 Pierwsza konsultacja BEZPŁATNA!**

**Chcesz umówić spotkanie?**
Napisz "umów konsultację" a pomogę Ci w rezerwacji!"""
    
    def _handle_materials_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o materiałach"""
        return """🎨 **Materiały NovaHouse:**

**✨ Standardy jakości:**
• **Wysokiej jakości materiały** we wszystkich pakietach
• **Markowe produkty** od sprawdzonych dostawców
• **Trwałe wykończenia** z długą gwarancją
• **Estetyczne rozwiązania** dopasowane do stylu

**🏆 Pakiet Comfort:**
• Solidne materiały podstawowe
• Sprawdzona jakość
• Optymalna relacja cena-jakość

**💎 Pakiet Express Plus:**
• Materiały premium
• Dodatkowe opcje wykończenia
• Rozszerzone możliwości personalizacji

**🎯 Personalizacja:**
Każdy pakiet można dostosować do Twoich preferencji!

**Chcesz zobaczyć materiały?**
Umów wizytę w showroomie - napisz "showroom"!"""
    
    def _handle_showroom_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o showroomie"""
        return """🏢 **Showroom NovaHouse:**

**✨ Co znajdziesz w showroomie:**
• **Ekspozycja materiałów** - dotknij i zobacz jakość
• **Próbki wykończeń** - wszystkie dostępne standardy  
• **Konsultacje z ekspertami** - profesjonalne doradztwo
• **Prezentacje projektów** - inspiracje i realizacje

**📅 Wizyty po umówieniu:**
• Indywidualne podejście do każdego klienta
• Czas na szczegółowe omówienie projektu
• Możliwość porównania materiałów

**🎯 Korzyści z wizyty:**
• Lepsze zrozumienie jakości materiałów
• Personalne doradztwo projektanta
• Dokładne omówienie możliwości

**Chcesz umówić wizytę w showroomie?**
Napisz "umów wizytę" a pomogę Ci zarezerwować termin!

*Showroom to najlepszy sposób na poznanie naszej oferty!* 🌟"""
    
    def _handle_passive_house_question(self, query: str, context_chunks: List[Dict]) -> str:
        """Odpowiedzi o domach pasywnych"""
        return """🏡 **Domy pasywne NovaHouse:**

**🌱 Specjalizacja w domach pasywnych:**
NovaHouse ma wieloletnie doświadczenie w projektowaniu i budowie domów pasywnych - energooszczędnych budynków przyszłości.

**⚡ Korzyści domów pasywnych:**
• **Niskie koszty ogrzewania** - do 90% oszczędności
• **Komfort przez cały rok** - stała temperatura
• **Zdrowy mikroklimat** - kontrolowana wentylacja
• **Ekologiczne rozwiązania** - ochrona środowiska
• **Wysoka wartość nieruchomości** - inwestycja w przyszłość

**🔧 Nasze usługi:**
• Projektowanie domów pasywnych
• Kompleksowa realizacja
• Doradztwo techniczne
• Certyfikacja energetyczna

**Interesujesz się domem pasywnym?**
Napisz "dom pasywny" aby umówić konsultację z naszym ekspertem!

*Domy pasywne to przyszłość budownictwa!* 🌿"""
    
    def answer_question(self, question: str) -> str:
        """Główna metoda odpowiadania na pytania"""
        
        # Wyszukiwanie w bazie wiedzy
        relevant_chunks = self.search_knowledge(question)
        
        if not relevant_chunks:
            return """Przepraszam, nie znalazłem informacji na ten temat w mojej bazie wiedzy. 

Mogę pomóc Ci w:
• Informacjach o pakietach wykończeniowych
• Procesie realizacji i harmonogramach
• Umówieniu konsultacji
• Kontakcie z naszym zespołem

Napisz "konsultant" a przekażę Cię do odpowiedniej osoby, która pomoże Ci z bardziej szczegółowymi pytaniami."""
        
        # Generowanie odpowiedzi
        response = self.generate_response(question, relevant_chunks)
        
        return response
    
    def load_external_knowledge(self):
        """Ładowanie zewnętrznych plików z wiedzą"""
        knowledge_files = [
            "/home/ubuntu/upload/knowledge_base_update.md",
            "/home/ubuntu/upload/Dokumentacja końcowa chatbota NovaHouse.md",
            "/home/ubuntu/upload/Materiały szkoleniowe dla zespołu NovaHouse.md"
        ]
        
        for file_path in knowledge_files:
            if os.path.exists(file_path):
                category = os.path.basename(file_path).replace('.md', '').replace(' ', '_')
                self.add_knowledge_from_file(file_path, category)
        
        logging.info(f"Załadowano bazę wiedzy: {len(self.knowledge_chunks)} chunków")

# Globalna instancja bazy wiedzy
knowledge_base = None

def get_knowledge_base() -> NovaHouseKnowledgeBase:
    """Pobieranie instancji bazy wiedzy (singleton)"""
    global knowledge_base
    if knowledge_base is None:
        knowledge_base = NovaHouseKnowledgeBase()
        knowledge_base.load_external_knowledge()
    return knowledge_base

def answer_with_knowledge(question: str) -> str:
    """Funkcja pomocnicza do odpowiadania na pytania"""
    kb = get_knowledge_base()
    return kb.answer_question(question)

