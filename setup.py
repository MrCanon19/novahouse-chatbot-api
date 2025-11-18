"""
📦 NovaHouse Chatbot API - Setup Script
========================================

Ten skrypt automatycznie konfiguruje środowisko developerskie.

Wykonuje:
- ✅ Sprawdzenie Python 3.11+
- ✅ Utworzenie virtual environment
- ✅ Instalacja dependencies
- ✅ Konfiguracja .env
- ✅ Inicjalizacja bazy danych
- ✅ Setup pre-commit hooks
- ✅ Weryfikacja instalacji

Użycie:
    python setup.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Kolory dla terminala
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text):
    """Pretty print header"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}🚀 {text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")


def check_python_version():
    """Sprawdź wersję Pythona"""
    print_header("Sprawdzanie wersji Pythona")
    
    if sys.version_info < (3, 11):
        print_error(f"Wymagany Python 3.11+, znaleziono {sys.version}")
        print("Zainstaluj nowszą wersję: https://www.python.org/downloads/")
        sys.exit(1)
    
    print_success(f"Python {sys.version.split()[0]} ✓")


def create_venv():
    """Utwórz virtual environment"""
    print_header("Tworzenie Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print_warning("Virtual environment już istnieje, pomijam...")
        return
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment utworzony")
    except subprocess.CalledProcessError as e:
        print_error(f"Błąd podczas tworzenia venv: {e}")
        sys.exit(1)


def get_pip_path():
    """Zwróć ścieżkę do pip w venv"""
    if sys.platform == "win32":
        return Path("venv/Scripts/pip.exe")
    return Path("venv/bin/pip")


def get_python_path():
    """Zwróć ścieżkę do python w venv"""
    if sys.platform == "win32":
        return Path("venv/Scripts/python.exe")
    return Path("venv/bin/python")


def install_dependencies():
    """Zainstaluj dependencies z requirements.txt"""
    print_header("Instalacja Dependencies")
    
    pip_path = get_pip_path()
    
    if not pip_path.exists():
        print_error("Nie znaleziono pip w venv!")
        sys.exit(1)
    
    try:
        # Upgrade pip
        print("Aktualizacja pip...")
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        print("Instalacja pakietów z requirements.txt...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        
        print_success("Dependencies zainstalowane")
    except subprocess.CalledProcessError as e:
        print_error(f"Błąd podczas instalacji: {e}")
        sys.exit(1)


def setup_env_file():
    """Utwórz plik .env z template"""
    print_header("Konfiguracja .env")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print_warning(".env już istnieje, pomijam...")
        return
    
    if not env_example.exists():
        print_error(".env.example nie znaleziony!")
        return
    
    try:
        shutil.copy(env_example, env_file)
        print_success(".env utworzony z .env.example")
        print(f"{YELLOW}⚠️  Uzupełnij .env własnymi wartościami przed uruchomieniem!{RESET}")
    except Exception as e:
        print_error(f"Błąd podczas kopiowania .env: {e}")


def setup_pre_commit():
    """Zainstaluj pre-commit hooks"""
    print_header("Setup Pre-commit Hooks")
    
    pip_path = get_pip_path()
    
    try:
        # Install pre-commit
        subprocess.run([str(pip_path), "install", "pre-commit"], check=True)
        
        # Install hooks
        if sys.platform == "win32":
            pre_commit = Path("venv/Scripts/pre-commit.exe")
        else:
            pre_commit = Path("venv/bin/pre-commit")
        
        subprocess.run([str(pre_commit), "install"], check=True)
        print_success("Pre-commit hooks zainstalowane")
    except subprocess.CalledProcessError as e:
        print_warning(f"Pre-commit setup failed (opcjonalne): {e}")


def verify_installation():
    """Zweryfikuj instalację"""
    print_header("Weryfikacja Instalacji")
    
    python_path = get_python_path()
    
    try:
        # Test import głównych pakietów
        test_script = """
import flask
import sqlalchemy
import google.generativeai
import redis
print('✅ Wszystkie główne pakiety zaimportowane')
"""
        
        result = subprocess.run(
            [str(python_path), "-c", test_script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("Weryfikacja przeszła pomyślnie")
            print(result.stdout.strip())
        else:
            print_warning("Niektóre pakiety mogą nie działać:")
            print(result.stderr)
    except Exception as e:
        print_warning(f"Weryfikacja nie powiodła się: {e}")


def print_next_steps():
    """Wyświetl następne kroki"""
    print_header("🎉 Setup Complete!")
    
    print("Następne kroki:\n")
    print("1️⃣  Aktywuj virtual environment:")
    if sys.platform == "win32":
        print(f"    {BLUE}venv\\Scripts\\activate{RESET}")
    else:
        print(f"    {BLUE}source venv/bin/activate{RESET}")
    
    print("\n2️⃣  Uzupełnij .env własnymi wartościami:")
    print(f"    {BLUE}nano .env{RESET}")
    
    print("\n3️⃣  Uruchom development server:")
    print(f"    {BLUE}python main.py{RESET}")
    
    print("\n4️⃣  Sprawdź health check:")
    print(f"    {BLUE}curl http://localhost:8080/api/health{RESET}")
    
    print("\n5️⃣  Uruchom testy:")
    print(f"    {BLUE}pytest tests/{RESET}")
    
    print("\n📚 Dokumentacja:")
    print("    - README.md - Główna dokumentacja")
    print("    - CONTRIBUTING.md - Jak kontrybuować")
    print("    - SETUP_MONITORING.md - Setup Sentry & Redis")
    
    print(f"\n{GREEN}Happy coding! 🚀{RESET}\n")


def main():
    """Główna funkcja setup"""
    print(f"\n{BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🏠 NovaHouse Chatbot API - Development Setup            ║")
    print("║  Version 2.3.0 'Production Ready'                        ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")
    
    try:
        check_python_version()
        create_venv()
        install_dependencies()
        setup_env_file()
        setup_pre_commit()
        verify_installation()
        print_next_steps()
        
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Setup przerwany przez użytkownika{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Nieoczekiwany błąd: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
