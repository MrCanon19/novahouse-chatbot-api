#!/usr/bin/env python3
"""
Run migration via gcloud app execute command
This runs the migration endpoint directly on GAE instance
"""

import subprocess
import sys
import json

API_KEY = "V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
PRODUCTION_URL = "https://glass-core-467907-e9.ey.r.appspot.com"

def run_migration_gcloud():
    """Run migration using gcloud app execute"""
    print("=" * 70)
    print("🚀 MIGRACJA PRZEZ GCLOUD APP EXECUTE")
    print("=" * 70)
    print()
    
    # Try direct API call first
    print("1. Próba przez API endpoint...")
    try:
        import requests
        response = requests.post(
            f"{PRODUCTION_URL}/api/migration/create-dead-letter-queue",
            headers={
                "X-API-KEY": API_KEY,
                "Content-Type": "application/json"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Migracja zakończona pomyślnie przez API!")
            print(f"   Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"⚠️  API zwróciło {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"⚠️  Błąd API: {e}")
    
    print()
    print("2. Alternatywa: Uruchomienie przez gcloud...")
    print("   (Wymaga zainstalowanego gcloud CLI)")
    print()
    print("   Polecenie do uruchomienia ręcznie:")
    print(f"   curl -X POST {PRODUCTION_URL}/api/migration/create-dead-letter-queue \\")
    print(f"     -H 'X-API-KEY: {API_KEY}' \\")
    print(f"     -H 'Content-Type: application/json'")
    print()
    
    return False


if __name__ == "__main__":
    success = run_migration_gcloud()
    sys.exit(0 if success else 1)

