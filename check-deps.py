#!/usr/bin/env python3
"""
🔍 Dependency Checker
Sprawdza czy wszystkie dependencies są aktualne i bezpieczne
"""

import subprocess
import json
from typing import List, Dict

def get_installed_packages() -> Dict[str, str]:
    """Pobierz zainstalowane pakiety"""
    result = subprocess.run(
        ["pip", "list", "--format=json"],
        capture_output=True,
        text=True
    )
    packages = json.loads(result.stdout)
    return {pkg["name"]: pkg["version"] for pkg in packages}

def check_outdated() -> List[Dict]:
    """Sprawdź przestarzałe pakiety"""
    result = subprocess.run(
        ["pip", "list", "--outdated", "--format=json"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout:
        return json.loads(result.stdout)
    return []

def check_vulnerabilities() -> bool:
    """Sprawdź podatności (wymaga pip-audit)"""
    try:
        result = subprocess.run(
            ["pip-audit", "--format=json"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            vulns = json.loads(result.stdout)
            return len(vulns.get("dependencies", [])) > 0
    except FileNotFoundError:
        print("⚠️  pip-audit not installed. Install: pip install pip-audit")
        return False
    return False

def main():
    print("🔍 NovaHouse Chatbot - Dependency Check\n")
    
    # Installed packages
    print("📦 Checking installed packages...")
    installed = get_installed_packages()
    print(f"   Found {len(installed)} packages\n")
    
    # Outdated packages
    print("🔄 Checking for updates...")
    outdated = check_outdated()
    
    if outdated:
        print(f"   ⚠️  {len(outdated)} packages can be updated:\n")
        for pkg in outdated[:10]:  # Show first 10
            print(f"   • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        if len(outdated) > 10:
            print(f"   ... and {len(outdated) - 10} more")
        print(f"\n   Run: pip install --upgrade <package>")
    else:
        print("   ✅ All packages are up to date")
    
    print()
    
    # Security vulnerabilities
    print("🔒 Checking for security vulnerabilities...")
    has_vulns = check_vulnerabilities()
    
    if has_vulns:
        print("   ⚠️  Security vulnerabilities found!")
        print("   Run: pip-audit --fix")
    else:
        print("   ✅ No known vulnerabilities")
    
    print("\n" + "="*60)
    print("📊 Summary:")
    print(f"   Total packages: {len(installed)}")
    print(f"   Outdated: {len(outdated)}")
    print(f"   Vulnerabilities: {'Yes' if has_vulns else 'No'}")
    print("="*60)

if __name__ == "__main__":
    main()
