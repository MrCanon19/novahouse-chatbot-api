#!/usr/bin/env python3
"""
🧪 NovaHouse Chatbot - Smoke Tests
===================================

Szybkie testy sanity check po deploymencie.
Sprawdza czy wszystkie kluczowe endpointy działają.

Usage:
    python smoke_tests.py https://glass-core-467907-e9.ey.r.appspot.com
    python smoke_tests.py http://localhost:8080
"""

import json
import sys
from typing import Dict, Tuple

import requests

# Kolory
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def test_endpoint(
    base_url: str, endpoint: str, method: str = "GET", data: Dict = None, expected_status: int = 200
) -> Tuple[bool, str]:
    """
    Test pojedynczego endpointu

    Returns:
        (success: bool, message: str)
    """
    url = f"{base_url}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return False, f"Unsupported method: {method}"

        if response.status_code != expected_status:
            return False, f"Expected {expected_status}, got {response.status_code}"

        # Sprawdź czy response to JSON
        try:
            response.json()
        except json.JSONDecodeError:
            return False, "Invalid JSON response"

        return True, f"{response.status_code} OK"

    except requests.exceptions.Timeout:
        return False, "Timeout (>10s)"
    except requests.exceptions.ConnectionError:
        return False, "Connection failed"
    except Exception as e:
        return False, str(e)


def run_smoke_tests(base_url: str):
    """Uruchom wszystkie smoke tests"""

    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}🧪 NovaHouse Chatbot - Smoke Tests{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")
    print(f"Target: {base_url}\n")

    tests = [
        # Health & Core
        ("GET", "/api/health", None, 200, "Health check"),
        ("GET", "/", None, 200, "Root endpoint"),
        # Knowledge Base
        ("GET", "/api/packages", None, 200, "Packages endpoint"),
        ("GET", "/api/faq", None, 200, "FAQ endpoint"),
        ("GET", "/api/portfolio", None, 200, "Portfolio endpoint"),
        ("GET", "/api/reviews", None, 200, "Reviews endpoint"),
        ("GET", "/api/partners", None, 200, "Partners endpoint"),
        # Search
        ("GET", "/api/search?q=test", None, 200, "Search endpoint"),
        # Documentation
        ("GET", "/api/docs", None, 200, "API docs (Swagger)"),
        # Analytics (może wymagać API key, więc 401/403 też OK)
        ("GET", "/api/analytics/overview", None, None, "Analytics (auth may be required)"),
    ]

    results = []
    passed = 0
    failed = 0

    for method, endpoint, data, expected_status, description in tests:
        success, message = test_endpoint(base_url, endpoint, method, data, expected_status)
        results.append((description, success, message))

        if success:
            passed += 1
            print(f"{GREEN}✅ PASS{RESET} - {description}")
            print(f"   {message}\n")
        else:
            failed += 1
            print(f"{RED}❌ FAIL{RESET} - {description}")
            print(f"   {message}\n")

    # Summary
    print(f"{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}📊 Summary{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")

    total = passed + failed
    pass_rate = (passed / total * 100) if total > 0 else 0

    print(f"Total tests: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")
    print(f"Pass rate: {pass_rate:.1f}%\n")

    if pass_rate >= 90:
        print(f"{GREEN}🎉 System is healthy!{RESET}\n")
        return 0
    elif pass_rate >= 70:
        print(f"{YELLOW}⚠️  System has issues but core features work{RESET}\n")
        return 1
    else:
        print(f"{RED}🚨 System is unhealthy!{RESET}\n")
        return 2


def main():
    if len(sys.argv) < 2:
        print("Usage: python smoke_tests.py <base_url>")
        print("\nExamples:")
        print("  python smoke_tests.py https://glass-core-467907-e9.ey.r.appspot.com")
        print("  python smoke_tests.py http://localhost:8080")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    exit_code = run_smoke_tests(base_url)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
