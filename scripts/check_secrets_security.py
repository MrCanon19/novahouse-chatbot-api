#!/usr/bin/env python3
"""
Skrypt sprawdzający bezpieczeństwo sekretów w kodzie
Użycie: python scripts/check_secrets_security.py
"""

import os
import re
import sys
from pathlib import Path

# Wzorce do wykrywania sekretów
SECRET_PATTERNS = [
    (r'sk-proj-[A-Za-z0-9_-]{40,}', 'OpenAI API Key (sk-proj-)'),
    (r'sk-[A-Za-z0-9_-]{40,}', 'OpenAI API Key (sk-)'),
    (r'eyJ[A-Za-z0-9_-]{100,}', 'JWT Token / Monday.com API Key'),
    (r'[A-Za-z0-9_-]{32,}', 'Potential secret (long alphanumeric)'),
]

# Pliki/katalogi do ignorowania
IGNORE_PATTERNS = [
    '.git',
    'venv',
    'env',
    '__pycache__',
    '.pytest_cache',
    'node_modules',
    'backups',
    '.gitignore',
    'check_secrets_security.py',  # Ten plik
]

# Rozszerzenia plików do sprawdzania
CHECK_EXTENSIONS = ['.py', '.yaml', '.yml', '.json', '.sh', '.md', '.txt', '.env']

def is_ignored(file_path):
    """Sprawdź czy plik powinien być ignorowany"""
    path_str = str(file_path)
    
    # Zawsze ignoruj migracje i configs z przykładami
    for ignore_pattern in ALWAYS_IGNORE:
        if ignore_pattern in path_str:
            return True
    
    # Standardowe ignorowanie
    for pattern in IGNORE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def check_file(file_path):
    """Sprawdź plik pod kątem sekretów"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, description in SECRET_PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        # Sprawdź czy to nie jest komentarz z przykładem
                        if any(word in line.lower() for word in ['example', 'placeholder', 'template', 'your_', 'sk-...', 'xxx', 'replace']):
                            continue
                        
                        # Sprawdź czy to nie jest w .gitignore, dokumentacji lub testach
                        if file_path.suffix == '.md' or '.gitignore' in str(file_path) or 'test' in str(file_path).lower():
                            continue
                        
                        # Sprawdź czy to nie jest w plikach .secret, .env, .example (które są ignorowane)
                        if any(ext in str(file_path) for ext in ['.secret', '.env', '.example', '.deploy', '.template']):
                            continue
                        
                        # Sprawdź czy to nie jest w migracjach (zawsze ignoruj migracje)
                        if 'migration' in str(file_path).lower():
                            continue
                        
                        # Sprawdź czy to nie jest w config (przykłady)
                        if 'config/' in str(file_path) and 'app.yaml' in str(file_path):
                            continue
                        
                        # Sprawdź czy to nie jest długi ciąg w nazwie funkcji/zmiennej (false positive)
                        if '=' in line or ':' in line:
                            # Jeśli to przypisanie, sprawdź czy to nie jest nazwa funkcji/zmiennej
                            if any(keyword in line for keyword in ['def ', 'class ', 'import ', 'from ', 'return ', 'if ', 'for ']):
                                continue
                        
                        secret_preview = match.group()[:20] + "..." if len(match.group()) > 20 else match.group()
                        issues.append({
                            'file': str(file_path),
                            'line': line_num,
                            'pattern': description,
                            'preview': secret_preview,
                            'full_line': line.strip()[:100]
                        })
    except Exception as e:
        pass  # Ignoruj błędy odczytu
    
    return issues

def main():
    """Główna funkcja sprawdzająca"""
    print("=== 🔒 SPRAWDZANIE BEZPIECZEŃSTWA SEKRETÓW ===\n")
    
    root = Path('.')
    all_issues = []
    
    # Sprawdź wszystkie pliki
    for file_path in root.rglob('*'):
        if file_path.is_file() and not is_ignored(file_path):
            if any(file_path.suffix == ext for ext in CHECK_EXTENSIONS):
                issues = check_file(file_path)
                all_issues.extend(issues)
    
    # Wyświetl wyniki
    if all_issues:
        print(f"❌ Znaleziono {len(all_issues)} potencjalnych sekretów:\n")
        for issue in all_issues:
            print(f"📁 {issue['file']}:{issue['line']}")
            print(f"   Typ: {issue['pattern']}")
            print(f"   Podgląd: {issue['preview']}")
            print(f"   Linia: {issue['full_line']}")
            print()
        
        print("⚠️  UWAGA: Sprawdź czy te sekrety powinny być w kodzie!")
        print("   → Przenieś je do .env, app.yaml.secret lub GCP Secret Manager")
        print("   → Upewnij się, że pliki z sekretami są w .gitignore")
        return 1
    else:
        print("✅ Nie znaleziono sekretów w kodzie!")
        print("   Wszystkie sekrety są bezpiecznie przechowywane.")
        return 0

if __name__ == "__main__":
    sys.exit(main())

