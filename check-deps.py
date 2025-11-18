#!/usr/bin/env python3
"""
🔍 Dependency & Application Update Checker
Sprawdza czy wszystkie dependencies są aktualne i bezpieczne
Sprawdza dostępność nowych wersji aplikacji (GitHub releases)
"""

import subprocess
import json
import requests
import os
from typing import List, Dict, Optional
from datetime import datetime

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

def get_current_version() -> str:
    """Pobierz aktualną wersję aplikacji z pyproject.toml"""
    try:
        with open("pyproject.toml", "r") as f:
            for line in f:
                if line.startswith("version ="):
                    return line.split('"')[1]
    except FileNotFoundError:
        pass
    return "unknown"

def check_github_releases() -> Optional[Dict]:
    """
    Sprawdź najnowszą wersję aplikacji na GitHub
    Zwraca informacje o najnowszym release jeśli dostępny
    """
    repo_owner = "MrCanon19"
    repo_name = "novahouse-chatbot-api"
    
    try:
        # GitHub API - pobierz latest release
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NovaHouse-Chatbot-Update-Checker"
        }
        
        # Dodaj token jeśli dostępny (opcjonalnie)
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            release_data = response.json()
            return {
                "version": release_data["tag_name"].lstrip("v"),
                "name": release_data["name"],
                "published_at": release_data["published_at"],
                "url": release_data["html_url"],
                "body": release_data["body"][:200] + "..." if len(release_data["body"]) > 200 else release_data["body"]
            }
        elif response.status_code == 404:
            return None  # Brak releases
        else:
            print(f"   ⚠️  GitHub API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Network error: {str(e)[:50]}")
        return None
    except Exception as e:
        print(f"   ⚠️  Error checking GitHub: {str(e)[:50]}")
        return None

def compare_versions(current: str, latest: str) -> int:
    """
    Porównaj wersje (semantic versioning)
    Zwraca: -1 (current < latest), 0 (equal), 1 (current > latest)
    """
    def parse_version(v: str) -> tuple:
        """Parse version string to tuple of integers"""
        try:
            parts = v.replace("v", "").split(".")
            return tuple(int(p.split("-")[0]) for p in parts[:3])
        except:
            return (0, 0, 0)
    
    current_parts = parse_version(current)
    latest_parts = parse_version(latest)
    
    if current_parts < latest_parts:
        return -1
    elif current_parts > latest_parts:
        return 1
    else:
        return 0

def check_python_version() -> Optional[str]:
    """Sprawdź czy dostępna jest nowsza wersja Pythona"""
    try:
        import sys
        current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # Sprawdź najnowszą stabilną wersję Python na python.org
        response = requests.get("https://www.python.org/downloads/", timeout=5)
        if response.status_code == 200:
            # Prosta parsowanie - szuka "Download Python X.Y.Z"
            import re
            match = re.search(r'Download Python (\d+\.\d+\.\d+)', response.text)
            if match:
                latest = match.group(1)
                if compare_versions(current, latest) == -1:
                    return latest
        return None
    except:
        return None

def main():
    print("🔍 NovaHouse Chatbot - Update Checker\n")
    print("="*60)
    
    # Application version check
    print("\n📱 APPLICATION VERSION CHECK")
    print("-" * 60)
    current_version = get_current_version()
    print(f"   Current version: {current_version}")
    
    print("   Checking GitHub for new releases...")
    latest_release = check_github_releases()
    
    if latest_release:
        latest_version = latest_release["version"]
        comparison = compare_versions(current_version, latest_version)
        
        if comparison == -1:
            print(f"   🎉 NEW VERSION AVAILABLE: {latest_version}")
            print(f"   📅 Released: {latest_release['published_at'][:10]}")
            print(f"   📝 {latest_release['name']}")
            print(f"   🔗 {latest_release['url']}")
            print(f"\n   Update command: git pull origin main")
        elif comparison == 0:
            print(f"   ✅ You're on the latest version ({current_version})")
        else:
            print(f"   ℹ️  You're ahead of latest release ({latest_version})")
    else:
        print("   ℹ️  No releases found on GitHub")
    
    # Python version check
    print("\n🐍 PYTHON VERSION CHECK")
    print("-" * 60)
    import sys
    current_python = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"   Current Python: {current_python}")
    
    latest_python = check_python_version()
    if latest_python:
        print(f"   🆕 Newer Python available: {latest_python}")
        print(f"   Download: https://www.python.org/downloads/")
    else:
        print("   ✅ Python version is recent")
    
    # Installed packages
    print("\n📦 PYTHON PACKAGES")
    print("-" * 60)
    print("   Checking installed packages...")
    installed = get_installed_packages()
    print(f"   Found {len(installed)} packages")
    
    # Outdated packages
    print("   Checking for updates...")
    outdated = check_outdated()
    
    if outdated:
        print(f"   ⚠️  {len(outdated)} packages can be updated:\n")
        for pkg in outdated[:10]:  # Show first 10
            print(f"   • {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        if len(outdated) > 10:
            print(f"   ... and {len(outdated) - 10} more")
        print(f"\n   Update command: pip install --upgrade <package>")
        print(f"   Update all: pip install --upgrade -r requirements.txt")
    else:
        print("   ✅ All packages are up to date")
    
    # Security vulnerabilities
    print("\n🔒 SECURITY CHECK")
    print("-" * 60)
    print("   Checking for vulnerabilities...")
    has_vulns = check_vulnerabilities()
    
    if has_vulns:
        print("   ⚠️  Security vulnerabilities found!")
        print("   Fix command: pip-audit --fix")
    else:
        print("   ✅ No known vulnerabilities")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"   Application: {current_version} {'⚠️ UPDATE AVAILABLE' if latest_release and compare_versions(current_version, latest_release['version']) == -1 else '✅'}")
    print(f"   Python: {current_python} {'🆕' if latest_python else '✅'}")
    print(f"   Packages: {len(installed)} total, {len(outdated)} outdated")
    print(f"   Security: {'⚠️ VULNERABILITIES' if has_vulns else '✅ SECURE'}")
    print("="*60)
    
    # Exit code
    if latest_release and compare_versions(current_version, latest_release['version']) == -1:
        print("\n💡 Tip: Run 'git pull' to update to the latest version")
        return 1  # Exit with warning code
    return 0

if __name__ == "__main__":
    main()
