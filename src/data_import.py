#!/usr/bin/env python3
"""
Skrypt do importu danych treningowych dla chatbota NovaHouse
"""

import os
import sys
import json
import re

# Dodanie ścieżki do modułów aplikacji
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.chatbot import db, Intent, Entity


def create_app():
    """Tworzenie aplikacji Flask dla importu danych"""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def parse_intents_file(file_path):
    """Parsowanie pliku z intencjami"""
    intents_data = {}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Podział na sekcje intencji
    intent_sections = re.split(r"^## (.+)$", content, flags=re.MULTILINE)

    for i in range(1, len(intent_sections), 2):
        intent_name = intent_sections[i].strip()
        intent_content = intent_sections[i + 1].strip()

        # Wyciągnięcie przykładowych fraz
        training_phrases = []
        for line in intent_content.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                phrase = line[2:].strip()
                if phrase:
                    training_phrases.append(phrase)

        if training_phrases:
            intents_data[intent_name] = {
                "training_phrases": training_phrases,
                "response_templates": [f"Rozumiem, że pytasz o {intent_name}. Jak mogę Ci pomóc?"],
            }

    return intents_data


def parse_entities_file(file_path):
    """Parsowanie pliku z encjami"""
    entities_data = {}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Podział na sekcje encji
    entity_sections = re.split(r"^## (.+)$", content, flags=re.MULTILINE)

    for i in range(1, len(entity_sections), 2):
        entity_name = entity_sections[i].strip()
        entity_content = entity_sections[i + 1].strip()

        # Wyciągnięcie wartości encji
        values = []
        for line in entity_content.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                value = line[2:].strip()
                if value:
                    values.append(value)

        if values:
            entities_data[entity_name] = values

    return entities_data


def create_response_templates():
    """Tworzenie szablonów odpowiedzi dla różnych intencji"""
    return {
        "zapytanie_o_pakiety": [
            "Oferujemy 4 główne pakiety wykończeniowe: Waniliowy, Pomarańczowy, Cynamonowy i Szafranowy. Każdy pakiet ma różny standard wykończenia. O którym pakiecie chciałbyś dowiedzieć się więcej?",
            "Nasze pakiety wykończeniowe to: Waniliowy (podstawowy), Pomarańczowy (podwyższony), Cynamonowy (wysoki) i Szafranowy (premium). Który Cię interesuje?",
            "Mamy 4 pakiety: od podstawowego Waniliowego po luksusowy Szafranowy. Każdy można dostosować do Twoich potrzeb. Chcesz poznać szczegóły?",
        ],
        "pytanie_o_ceny": [
            "Ceny zależą od wybranego pakietu i metrażu mieszkania. Chętnie przygotujemy dla Ciebie indywidualną wycenę. Podaj proszę metraż i preferowany pakiet.",
            "Koszt wykończenia zależy od wielu czynników. Aby podać dokładną cenę, potrzebuję informacji o metrażu i wybranym pakiecie. Możemy też umówić bezpłatną wycenę.",
            "Przygotujemy dla Ciebie szczegółową wycenę po poznaniu Twoich potrzeb. Jaki metraż ma Twoje mieszkanie i który pakiet Cię interesuje?",
        ],
        "umowienie_spotkania": [
            "Świetnie! Chętnie umówimy spotkanie. Możesz wybrać konsultację telefoniczną, spotkanie w biurze lub wizytę w mieszkaniu. Podaj swój numer telefonu.",
            "Z przyjemnością umówimy spotkanie! Oferujemy konsultacje telefoniczne, w biurze lub u Ciebie. Jak wolisz się spotkać?",
            "Doskonale! Nasze spotkania mogą być telefoniczne, w showroomie lub u Ciebie w domu. Jaka forma będzie dla Ciebie najwygodniejsza?",
        ],
        "pytanie_o_kontakt": [
            "Nasze dane kontaktowe: tel. +48 123 456 789, email: kontakt@novahouse.pl, adres: ul. Przykładowa 123, Gdańsk. Biuro czynne Pon-Pt 8-18, Sob 9-15.",
            "Możesz się z nami skontaktować: telefon +48 123 456 789, email kontakt@novahouse.pl. Zapraszamy też do naszego biura w Gdańsku!",
            "Kontakt: +48 123 456 789, kontakt@novahouse.pl, ul. Przykładowa 123, Gdańsk. Jesteśmy dostępni Pon-Pt 8-18, Sob 9-15.",
        ],
        "powitanie": [
            "Cześć! Witaj w NovaHouse! Jestem Twoim asystentem i pomogę Ci w wyborze pakietu wykończeniowego. Jak mogę Ci pomóc?",
            "Witaj! Miło Cię poznać. Jestem chatbotem NovaHouse i chętnie odpowiem na Twoje pytania o wykończenia wnętrz. O czym chciałbyś porozmawiać?",
            "Hej! Świetnie, że jesteś! Pomogę Ci w sprawach związanych z wykończeniem mieszkania. Jakie masz pytania?",
        ],
        "pozegnanie": [
            "Dziękuję za rozmowę! Jeśli będziesz mieć jakieś pytania, śmiało pisz. Miłego dnia!",
            "Było mi miło z Tobą rozmawiać! Do zobaczenia i powodzenia z wykończeniem!",
            "Dzięki za wizytę! Pamiętaj, że zawsze możesz do nas wrócić z pytaniami. Powodzenia!",
        ],
        "pytanie_o_materialy": [
            "Używamy tylko wysokiej jakości materiałów od sprawdzonych dostawców. W każdym pakiecie znajdziesz szczegółową specyfikację materiałów.",
            "Jakość materiałów to nasza priorytet! Współpracujemy z renomowanymi markami. Chcesz poznać szczegóły dla konkretnego pakietu?",
            "Wszystkie materiały dobieramy z dbałością o jakość i trwałość. Każdy pakiet ma swoją specyfikację materiałową.",
        ],
        "pytanie_o_czas_realizacji": [
            "Czas realizacji zależy od zakresu prac i metrażu. Standardowo wykończenie mieszkania trwa 4-8 tygodni. Podaj szczegóły, a określimy dokładny harmonogram.",
            "Realizacja trwa zwykle 4-8 tygodni, w zależności od pakietu i wielkości mieszkania. Chcesz poznać szczegółowy harmonogram dla Twojego projektu?",
            "Czas wykonania to około 4-8 tygodni. Dokładny harmonogram ustalimy po poznaniu zakresu prac. Jaki masz metraż?",
        ],
        "default": [
            "Przepraszam, nie jestem pewien jak odpowiedzieć na Twoje pytanie. Mogę pomóc w sprawach pakietów wykończeniowych, cen, umówienia spotkania lub kontaktu. O czym chciałbyś porozmawiać?",
            "Nie do końca rozumiem Twoje pytanie. Jestem ekspertem od wykończeń wnętrz NovaHouse. Zapytaj mnie o pakiety, ceny lub umów spotkanie!",
            "Hmm, nie jestem pewien co masz na myśli. Mogę odpowiedzieć na pytania o nasze pakiety wykończeniowe, ceny i umówić spotkanie. Jak mogę pomóc?",
        ],
    }


def import_training_data():
    """Główna funkcja importu danych treningowych"""
    app = create_app()

    with app.app_context():
        # Tworzenie tabel
        db.create_all()

        # Przygotowanie szablonów odpowiedzi
        response_templates = create_response_templates()

        # Ścieżki do plików z danymi - sprawdzamy wszystkie dostępne lokalizacje
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )  # /home/ubuntu/novahouse_project

        base_paths = [
            os.path.join(project_root, "chatbot_data_package"),
            project_root,  # główny katalog projektu
        ]

        intents_files = []
        entities_files = []

        for base_path in base_paths:
            # Sprawdzanie w podkatalogu nlu
            nlu_intents = os.path.join(base_path, "nlu", "intencje.md")
            nlu_entities = os.path.join(base_path, "nlu", "encje.md")

            # Sprawdzanie w głównym katalogu
            main_intents = os.path.join(base_path, "intencje.md")
            main_entities = os.path.join(base_path, "encje.md")

            if os.path.exists(nlu_intents):
                intents_files.append(nlu_intents)
            if os.path.exists(nlu_entities):
                entities_files.append(nlu_entities)
            if os.path.exists(main_intents):
                intents_files.append(main_intents)
            if os.path.exists(main_entities):
                entities_files.append(main_entities)

        print("🔄 Rozpoczynam import danych treningowych...")
        print(f"📁 Znalezione pliki intencji: {len(intents_files)}")
        print(f"📁 Znalezione pliki encji: {len(entities_files)}")

        # Import intencji ze wszystkich znalezionych plików
        all_intents_data = {}
        for intents_file in intents_files:
            print(f"📖 Czytam intencje z: {intents_file}")
            file_intents = parse_intents_file(intents_file)
            all_intents_data.update(file_intents)

        for intent_name, intent_info in all_intents_data.items():
            # Sprawdzenie czy intencja już istnieje
            existing_intent = Intent.query.filter_by(name=intent_name).first()
            if existing_intent:
                print(f"⚠️  Intencja '{intent_name}' już istnieje - pomijam")
                continue

            # Użycie przygotowanych szablonów odpowiedzi lub domyślnych
            templates = response_templates.get(intent_name, intent_info["response_templates"])

            intent = Intent(
                name=intent_name,
                training_phrases=json.dumps(intent_info["training_phrases"], ensure_ascii=False),
                response_templates=json.dumps(templates, ensure_ascii=False),
            )
            db.session.add(intent)
            print(
                f"✅ Dodano intencję: {intent_name} ({len(intent_info['training_phrases'])} fraz)"
            )

        # Import encji ze wszystkich znalezionych plików
        all_entities_data = {}
        for entities_file in entities_files:
            print(f"📖 Czytam encje z: {entities_file}")
            file_entities = parse_entities_file(entities_file)
            all_entities_data.update(file_entities)

        for entity_name, entity_values in all_entities_data.items():
            # Sprawdzenie czy encja już istnieje
            existing_entity = Entity.query.filter_by(name=entity_name).first()
            if existing_entity:
                print(f"⚠️  Encja '{entity_name}' już istnieje - pomijam")
                continue

            entity = Entity(name=entity_name, values=json.dumps(entity_values, ensure_ascii=False))
            db.session.add(entity)
            print(f"✅ Dodano encję: {entity_name} ({len(entity_values)} wartości)")

        # Dodanie dodatkowych intencji, które mogą nie być w pliku
        additional_intents = {
            "pytanie_o_materialy": {
                "training_phrases": [
                    "Jakie materiały używacie?",
                    "Czy materiały są dobrej jakości?",
                    "Skąd pochodzą materiały?",
                    "Czy mogę zobaczyć próbki materiałów?",
                    "Jakie marki materiałów stosujecie?",
                ],
                "response_templates": response_templates["pytanie_o_materialy"],
            },
            "pytanie_o_czas_realizacji": {
                "training_phrases": [
                    "Ile trwa wykończenie?",
                    "Jak długo będzie trwała realizacja?",
                    "Kiedy będzie gotowe?",
                    "Jaki jest czas wykonania?",
                    "W jakim czasie zrobicie wykończenie?",
                ],
                "response_templates": response_templates["pytanie_o_czas_realizacji"],
            },
        }

        for intent_name, intent_info in additional_intents.items():
            existing_intent = Intent.query.filter_by(name=intent_name).first()
            if not existing_intent:
                intent = Intent(
                    name=intent_name,
                    training_phrases=json.dumps(
                        intent_info["training_phrases"], ensure_ascii=False
                    ),
                    response_templates=json.dumps(
                        intent_info["response_templates"], ensure_ascii=False
                    ),
                )
                db.session.add(intent)
                print(f"✅ Dodano dodatkową intencję: {intent_name}")

        # Zapisanie zmian
        try:
            db.session.commit()
            print("🎉 Import danych zakończony pomyślnie!")

            # Statystyki
            intents_count = Intent.query.count()
            entities_count = Entity.query.count()
            print(f"📊 Statystyki: {intents_count} intencji, {entities_count} encji")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Błąd podczas zapisywania: {e}")
            return False

    return True


if __name__ == "__main__":
    success = import_training_data()
    if success:
        print("✨ Dane treningowe zostały pomyślnie zaimportowane!")
    else:
        print("💥 Wystąpił błąd podczas importu danych!")
        sys.exit(1)
