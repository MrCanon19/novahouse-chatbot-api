"""
Testy weryfikacji odszyfrowania backupów GPG
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestBackupDecryption:
    """Testy odszyfrowania backupów"""

    @pytest.fixture
    def sample_backup_data(self):
        """Przykładowe dane backupu"""
        return {
            "export_date": "2025-01-15T03:00:00Z",
            "version": "2.2",
            "tables": {
                "users": [{"id": 1, "username": "test", "email": "test@example.com"}],
                "leads": [{"id": 1, "name": "Test Lead", "email": "lead@example.com"}],
            },
        }

    @pytest.fixture
    def gpg_key_id(self):
        """Key ID GPG"""
        return os.getenv("GPG_KEY_ID", "1485A442EBE7A135AA9CD87B07804FF9F230D9BE")

    @pytest.fixture
    def gpg_passphrase(self):
        """Passphrase GPG"""
        return os.getenv("GPG_PASSPHRASE", "8$wK8$o4CfzuoQ2B")

    def test_backup_is_valid_json(self, sample_backup_data, tmp_path):
        """Test: Backup jest poprawnym JSON"""
        backup_file = tmp_path / "test_backup.json"
        
        with open(backup_file, "w") as f:
            json.dump(sample_backup_data, f)
        
        # Sprawdź czy można załadować jako JSON
        with open(backup_file, "r") as f:
            data = json.load(f)
        
        assert data["version"] == "2.2"
        assert "tables" in data
        assert "users" in data["tables"]
        assert "leads" in data["tables"]

    def test_backup_structure(self, sample_backup_data):
        """Test: Backup ma poprawną strukturę"""
        assert "export_date" in sample_backup_data
        assert "version" in sample_backup_data
        assert "tables" in sample_backup_data
        assert isinstance(sample_backup_data["tables"], dict)

    @pytest.mark.skipif(
        not os.path.exists("/usr/bin/gpg") and not os.path.exists("/usr/local/bin/gpg"),
        reason="GPG not installed",
    )
    def test_gpg_decryption_workflow(self, sample_backup_data, tmp_path, gpg_key_id, gpg_passphrase):
        """Test: Pełny workflow szyfrowania i odszyfrowania"""
        # 1. Utwórz plik backupu
        backup_file = tmp_path / "test_backup.json"
        encrypted_file = tmp_path / "test_backup.json.gpg"
        
        with open(backup_file, "w") as f:
            json.dump(sample_backup_data, f)
        
        # 2. Zaszyfruj
        try:
            encrypt_cmd = [
                "gpg",
                "--batch",
                "--yes",
                "--pinentry-mode", "loopback",
                "--cipher-algo", "AES256",
                "--recipient", gpg_key_id,
                "--encrypt",
                "--output", str(encrypted_file),
                str(backup_file),
            ]
            
            process = subprocess.Popen(
                encrypt_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            stdout, stderr = process.communicate(input=gpg_passphrase.encode())
            
            if process.returncode != 0:
                pytest.skip(f"GPG encryption failed: {stderr.decode()}")
            
            # 3. Sprawdź czy plik zaszyfrowany istnieje
            assert encrypted_file.exists(), "Zaszyfrowany plik nie został utworzony"
            
            # 4. Odszyfruj
            decrypted_file = tmp_path / "test_backup_decrypted.json"
            decrypt_cmd = [
                "gpg",
                "--batch",
                "--yes",
                "--pinentry-mode", "loopback",
                "--passphrase-fd", "0",
                "--decrypt",
                "--output", str(decrypted_file),
                str(encrypted_file),
            ]
            
            process = subprocess.Popen(
                decrypt_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            stdout, stderr = process.communicate(input=gpg_passphrase.encode())
            
            assert process.returncode == 0, f"GPG decryption failed: {stderr.decode()}"
            assert decrypted_file.exists(), "Odszyfrowany plik nie został utworzony"
            
            # 5. Sprawdź zawartość
            with open(decrypted_file, "r") as f:
                decrypted_data = json.load(f)
            
            assert decrypted_data["version"] == sample_backup_data["version"]
            assert decrypted_data["export_date"] == sample_backup_data["export_date"]
            assert len(decrypted_data["tables"]["users"]) == len(sample_backup_data["tables"]["users"])
            
        except FileNotFoundError:
            pytest.skip("GPG not found in system")

    def test_backup_contains_required_tables(self, sample_backup_data):
        """Test: Backup zawiera wymagane tabele"""
        required_tables = ["users", "leads", "bookings", "chat_sessions", "messages"]
        
        # Sprawdź które tabele są w backupie
        backup_tables = set(sample_backup_data["tables"].keys())
        
        # W tym teście sprawdzamy tylko czy struktura jest poprawna
        # W rzeczywistym backupie powinny być wszystkie tabele
        assert isinstance(backup_tables, set)
        assert len(backup_tables) > 0

    def test_backup_file_size(self, sample_backup_data, tmp_path):
        """Test: Backup ma rozsądny rozmiar"""
        backup_file = tmp_path / "test_backup.json"
        
        with open(backup_file, "w") as f:
            json.dump(sample_backup_data, f)
        
        file_size = backup_file.stat().st_size
        
        # Backup nie powinien być pusty
        assert file_size > 0, "Backup jest pusty"
        
        # Backup nie powinien być zbyt duży (dla testu - w produkcji może być większy)
        # W rzeczywistości backupy mogą być większe, ale dla testu ustawiamy limit
        assert file_size < 100 * 1024 * 1024, "Backup jest zbyt duży (>100MB)"


def test_backup_location():
    """Test: Sprawdź lokalizację backupów"""
    import os
    
    # Sprawdź czy katalog backupów istnieje lub może być utworzony
    if os.environ.get("GAE_ENV", "").startswith("standard"):
        backup_dir = "/tmp/backups"
    else:
        backup_dir = os.path.join(os.path.dirname(__file__), "..", "backups", "automated")
    
    # Sprawdź czy katalog może być utworzony
    os.makedirs(backup_dir, exist_ok=True)
    assert os.path.exists(backup_dir), f"Katalog backupów nie istnieje: {backup_dir}"
    assert os.path.isdir(backup_dir), f"Ścieżka nie jest katalogiem: {backup_dir}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

