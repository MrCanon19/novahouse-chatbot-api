"""
Tests for knowledge base
"""

import pytest

# Try to import PACKAGES (optional module)
try:
    from src.knowledge.novahouse_info import PACKAGES
    KNOWLEDGE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_AVAILABLE = False
    PACKAGES = {}


@pytest.mark.skipif(not KNOWLEDGE_AVAILABLE, reason="Knowledge module not available")
class TestPackagesData:
    """Tests for packages data structure"""

    def test_all_packages_exist(self):
        """Test that all expected packages are defined"""
        expected_packages = ["express", "express_plus", "comfort", "premium", "individual"]
        for package_name in expected_packages:
            assert package_name in PACKAGES

    def test_package_has_required_fields(self):
        """Test that each package has required fields"""
        required_fields = ["name", "price_per_sqm", "standard", "ideal_for"]

        for package_key, package_data in PACKAGES.items():
            for field in required_fields:
                assert field in package_data, f"Package '{package_key}' missing field '{field}'"
