#!/usr/bin/env python3
"""
Skrypt testowy do sprawdzania połączenia z OpenAI API
Użycie: python scripts/test_openai_connection.py
"""

import os
import sys

def test_openai_connection():
    """Test połączenia z OpenAI API"""
    print("=== 🧪 TEST POŁĄCZENIA Z OPENAI API ===\n")
    
    # 1. Sprawdź czy klucz jest ustawiony
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY nie jest ustawiony w środowisku")
        print("   Ustaw: export OPENAI_API_KEY='sk-...'")
        print("   Lub sprawdź app.yaml.secret dla produkcji")
        return False
    
    print(f"✅ OPENAI_API_KEY jest ustawiony")
    print(f"   Długość: {len(api_key)} znaków")
    print(f"   Zaczyna się od: {api_key[:15]}...")
    
    # 2. Sprawdź format klucza
    if api_key.lower().startswith("test_"):
        print("⚠️  To jest klucz testowy - GPT będzie wyłączony")
        return False
    elif api_key.startswith("sk-") or api_key.startswith("sk-proj-"):
        print("✅ Format klucza jest poprawny")
    else:
        print("⚠️  Format klucza może być nieprawidłowy")
        print("   Oczekiwany format: sk-... lub sk-proj-...")
    
    # 3. Sprawdź czy pakiet openai jest zainstalowany
    try:
        import openai
        print(f"✅ Pakiet openai zainstalowany (wersja: {openai.__version__ if hasattr(openai, '__version__') else 'nieznana'})")
    except ImportError:
        print("❌ Pakiet openai NIE jest zainstalowany")
        print("   Zainstaluj: pip install openai")
        return False
    
    # 4. Test połączenia z API
    print("\n🔌 Test połączenia z OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Odpowiedz tylko: OK"}],
            max_tokens=10
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"✅ Połączenie działa!")
        print(f"   Odpowiedź: {answer}")
        
        if hasattr(response, 'usage'):
            usage = response.usage
            print(f"   Tokens użyte: {usage.total_tokens} (input: {usage.prompt_tokens}, output: {usage.completion_tokens})")
        
        return True
        
    except openai.AuthenticationError as e:
        print(f"❌ Błąd autoryzacji: {e}")
        print("   → Klucz API jest nieprawidłowy lub wygasł")
        print("   → Sprawdź klucz w https://platform.openai.com/api-keys")
        return False
    except openai.RateLimitError as e:
        print(f"⚠️  Przekroczono limity API: {e}")
        print("   → Sprawdź limity w dashboard OpenAI")
        print("   → Poczekaj na reset limitu")
        return False
    except openai.APIConnectionError as e:
        print(f"❌ Błąd połączenia: {e}")
        print("   → Sprawdź połączenie sieciowe")
        print("   → Sprawdź czy OpenAI API jest dostępne")
        return False
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    print("\n" + "="*50)
    if success:
        print("✅ TEST ZAKOŃCZONY POMYŚLNIE")
        print("   Chatbot powinien działać poprawnie!")
    else:
        print("❌ TEST ZAKOŃCZONY BŁĘDEM")
        print("   Sprawdź konfigurację przed wdrożeniem")
    sys.exit(0 if success else 1)

