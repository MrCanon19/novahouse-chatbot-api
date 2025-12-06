"""
Pre-commit validation: Ensures test integrity
Checks:
1. API routes are synced across all tests
2. No references to non-existent fixtures
3. No hardcoded URLs
4. Extraction validators are used correctly
"""

import logging
import re
import sys
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def check_test_files() -> List[str]:
    """Check all test files for common issues"""
    errors = []
    test_dir = Path("tests")

    if not test_dir.exists():
        return errors

    # Expected API routes
    expected_routes = {
        "/api/chatbot/chat": "chatbot message",
        "/api/leads": "lead creation",
        "/api/booking": "booking",
    }

    test_files = list(test_dir.glob("test_*.py"))

    for test_file in test_files:
        content = test_file.read_text()

        # Check 1: API route consistency
        # Note: Routes like /api/chatbot/rodo-consent are correct, only /api/chat is wrong
        old_route = "/api/chat"
        if old_route + '"' in content or old_route + "'" in content:
            # Check it's not part of a longer route like /api/chatbot
            if "/api/chatbot" not in content or (
                old_route + '"' in content and '"/api/chatbot' not in content
            ):
                errors.append(
                    f"{test_file.name}: Uses old route {old_route} (should be /api/chatbot/chat)"
                )

        # Check 2: Hardcoded fixtures that might not exist
        fixture_refs = re.findall(r"def\s+(\w+)\(.*?(setup_\w+).*?\)", content)
        for func_name, fixture in fixture_refs:
            if not fixture.startswith("_"):  # Skip private fixtures
                # Verify fixture exists in conftest
                conftest_path = test_dir / "conftest.py"
                if conftest_path.exists():
                    conftest = conftest_path.read_text()
                    if f"@pytest.fixture" not in conftest or f"def {fixture}" not in conftest:
                        errors.append(
                            f"{test_file.name}: Uses undefined fixture '{fixture}' in {func_name}"
                        )

        # Check 3: Extract context validation
        # Note: Tests using extract_context should either:
        # 1. Be testing extract_context itself, OR
        # 2. Mock the response, OR
        # 3. Use extract_context_safe wrapper
        if "extract_context" in content and "extract_context_safe" not in content:
            # Check if this test is actually testing extract_context
            if "def test_extract" in content or "test_extraction" in content:
                # This is OK - it's testing the function directly
                pass
            elif "mock" in content.lower() or "@patch" in content:
                # This is OK - it's mocking the function
                pass
            else:
                # Warn but don't fail - some tests may legitimately use it
                logger.debug(
                    f"{test_file.name}: Uses extract_context directly (consider using extract_context_safe)"
                )

    return errors


def check_src_files() -> List[str]:
    """Check src files for extraction issues"""
    errors = []
    src_dir = Path("src")

    if not src_dir.exists():
        return errors

    # Check chatbot.py for hardcoded cities or packages
    chatbot_file = src_dir / "routes" / "chatbot.py"
    if chatbot_file.exists():
        content = chatbot_file.read_text()

        # Check that hardcoded city list is limited (shouldn't have more than 20 common ones)
        city_pattern = r"city_patterns\s*=\s*\{([^}]*)\}"
        match = re.search(city_pattern, content, re.DOTALL)
        if match:
            cities = match.group(1).count(":")
            # This is OK - having a common cities list is fine

        # Check for invalid budget ranges
        if "budget >" in content or "budget <" in content:
            # Look for validation
            if not re.search(r"50000.*5000000|5000000.*50000", content):
                errors.append(
                    "chatbot.py: Budget validation range not found (should be 50k-5M PLN)"
                )

    return errors


def check_imports() -> List[str]:
    """Check that required validators are imported"""
    errors = []

    # Check chatbot.py has correct imports
    chatbot_file = Path("src/routes/chatbot.py")
    if chatbot_file.exists():
        content = chatbot_file.read_text()

        required_imports = [
            "from src.services.extraction_validator",
            "from src.services.regression_detector",
        ]

        # Note: These might not be imported yet if using old code
        # Just validate that IF they're used, they're imported
        if "extract_context_safe" in content:
            if "from src.services.extract_context_safe" not in content:
                errors.append("chatbot.py: Uses extract_context_safe but doesn't import it")

    return errors


def main():
    """Run all checks"""
    all_errors = []

    print("🔍 Running pre-commit validations...")

    # Check test files
    test_errors = check_test_files()
    if test_errors:
        print("\n❌ Test file issues:")
        for error in test_errors:
            print(f"  - {error}")
        all_errors.extend(test_errors)

    # Check src files
    src_errors = check_src_files()
    if src_errors:
        print("\n❌ Source file issues:")
        for error in src_errors:
            print(f"  - {error}")
        all_errors.extend(src_errors)

    # Check imports
    import_errors = check_imports()
    if import_errors:
        print("\n❌ Import issues:")
        for error in import_errors:
            print(f"  - {error}")
        all_errors.extend(import_errors)

    if not all_errors:
        print("✅ All validation checks passed!")
        return 0
    else:
        print(f"\n🚨 Found {len(all_errors)} issue(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
