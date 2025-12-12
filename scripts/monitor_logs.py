#!/usr/bin/env python3
"""
Monitor logów aplikacji w czasie rzeczywistym
Śledzi błędy, ostrzeżenia i kluczowe wydarzenia
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

# Kolory dla terminala
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Projekt GCP
PROJECT_ID = "glass-core-467907-e9"
SERVICE = "default"

def format_timestamp(ts: str) -> str:
    """Formatuj timestamp na czytelny format"""
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts

def format_severity(severity: str) -> str:
    """Formatuj severity z kolorami"""
    if severity == "ERROR":
        return f"{Colors.RED}{Colors.BOLD}ERROR{Colors.RESET}"
    elif severity == "WARNING":
        return f"{Colors.YELLOW}WARN {Colors.RESET}"
    elif severity == "INFO":
        return f"{Colors.GREEN}INFO {Colors.RESET}"
    elif severity == "DEBUG":
        return f"{Colors.CYAN}DEBUG{Colors.RESET}"
    else:
        return severity

def print_log_entry(entry: Dict):
    """Wyświetl pojedynczy wpis logu w czytelny sposób"""
    timestamp = entry.get("timestamp", "")
    severity = entry.get("severity", "INFO")
    text = entry.get("textPayload", entry.get("jsonPayload", {}).get("message", ""))
    
    # Formatuj timestamp
    ts_formatted = format_timestamp(timestamp)
    
    # Formatuj severity
    sev_formatted = format_severity(severity)
    
    # Wyświetl
    print(f"{Colors.CYAN}[{ts_formatted}]{Colors.RESET} {sev_formatted} {text}")
    
    # Jeśli to błąd, wyświetl dodatkowe informacje
    if severity == "ERROR" and "jsonPayload" in entry:
        json_payload = entry["jsonPayload"]
        if "error" in json_payload:
            error = json_payload["error"]
            print(f"  {Colors.RED}→ {error}{Colors.RESET}")

def filter_logs_by_severity(logs: List[Dict], min_severity: str = "INFO") -> List[Dict]:
    """Filtruj logi według severity"""
    severity_levels = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4
    }
    
    min_level = severity_levels.get(min_severity.upper(), 1)
    
    filtered = []
    for log in logs:
        severity = log.get("severity", "INFO")
        level = severity_levels.get(severity, 1)
        if level >= min_level:
            filtered.append(log)
    
    return filtered

def get_recent_logs(limit: int = 50, severity: Optional[str] = None) -> List[Dict]:
    """Pobierz ostatnie logi z GCP"""
    cmd = [
        "gcloud", "logging", "read",
        f"resource.type=gae_app AND resource.labels.module_id={SERVICE}",
        "--limit", str(limit),
        "--format", "json",
        "--project", PROJECT_ID
    ]
    
    if severity:
        cmd.insert(3, f"severity>={severity}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logs = json.loads(result.stdout)
        return logs if isinstance(logs, list) else []
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Błąd pobierania logów: {e}{Colors.RESET}")
        print(f"   {e.stderr}")
        return []
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}❌ Błąd parsowania JSON: {e}{Colors.RESET}")
        return []

def tail_logs(follow: bool = True, severity: Optional[str] = None):
    """Śledź logi w czasie rzeczywistym (tail -f)"""
    print(f"{Colors.BOLD}{Colors.CYAN}🔍 Monitor logów aplikacji{Colors.RESET}")
    print(f"{Colors.CYAN}Projekt: {PROJECT_ID}{Colors.RESET}")
    print(f"{Colors.CYAN}Serwis: {SERVICE}{Colors.RESET}")
    if severity:
        print(f"{Colors.CYAN}Filtr: severity >= {severity}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    
    last_timestamp = None
    
    while True:
        try:
            cmd = [
                "gcloud", "logging", "read",
                f"resource.type=gae_app AND resource.labels.module_id={SERVICE}",
                "--limit", "20",
                "--format", "json",
                "--project", PROJECT_ID,
                "--order", "desc"
            ]
            
            if severity:
                cmd.insert(3, f"severity>={severity}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logs = json.loads(result.stdout)
            
            if not isinstance(logs, list):
                logs = []
            
            # Filtruj tylko nowe logi
            if last_timestamp:
                logs = [log for log in logs if log.get("timestamp", "") > last_timestamp]
            
            # Wyświetl nowe logi
            for log in reversed(logs):  # Odwróć, żeby wyświetlić chronologicznie
                print_log_entry(log)
                if not last_timestamp or log.get("timestamp", "") > last_timestamp:
                    last_timestamp = log.get("timestamp", "")
            
            if follow:
                time.sleep(2)  # Sprawdzaj co 2 sekundy
            else:
                break
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⏹️  Zatrzymano monitorowanie{Colors.RESET}")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Błąd: {e}{Colors.RESET}")
            if follow:
                time.sleep(5)
            else:
                break

def show_error_summary():
    """Pokaż podsumowanie błędów z ostatnich logów"""
    print(f"{Colors.BOLD}{Colors.RED}📊 Podsumowanie błędów{Colors.RESET}\n")
    
    logs = get_recent_logs(limit=100, severity="ERROR")
    
    if not logs:
        print(f"{Colors.GREEN}✅ Brak błędów w ostatnich logach{Colors.RESET}")
        return
    
    # Grupuj błędy według typu
    error_types = {}
    for log in logs:
        text = log.get("textPayload", "")
        if not text:
            text = str(log.get("jsonPayload", {}).get("message", ""))
        
        # Wyciągnij typ błędu (pierwsza linia)
        error_type = text.split("\n")[0][:80]
        if error_type not in error_types:
            error_types[error_type] = []
        error_types[error_type].append(log)
    
    # Wyświetl podsumowanie
    print(f"{Colors.RED}Znaleziono {len(logs)} błędów w {len(error_types)} kategoriach:{Colors.RESET}\n")
    
    for error_type, error_logs in error_types.items():
        count = len(error_logs)
        latest = max(error_logs, key=lambda x: x.get("timestamp", ""))
        ts = format_timestamp(latest.get("timestamp", ""))
        
        print(f"{Colors.RED}  [{count}x]{Colors.RESET} {error_type[:60]}...")
        print(f"      {Colors.CYAN}Ostatni: {ts}{Colors.RESET}\n")

def main():
    """Główna funkcja"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor logów aplikacji GCP")
    parser.add_argument("--tail", "-t", action="store_true", help="Śledź logi w czasie rzeczywistym")
    parser.add_argument("--errors", "-e", action="store_true", help="Pokaż tylko błędy")
    parser.add_argument("--summary", "-s", action="store_true", help="Pokaż podsumowanie błędów")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Liczba logów do wyświetlenia")
    parser.add_argument("--severity", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       help="Minimalna severity")
    
    args = parser.parse_args()
    
    if args.summary:
        show_error_summary()
    elif args.tail:
        severity = "ERROR" if args.errors else args.severity
        tail_logs(follow=True, severity=severity)
    else:
        # Pokaż ostatnie logi
        severity = "ERROR" if args.errors else args.severity
        logs = get_recent_logs(limit=args.limit, severity=severity)
        
        if not logs:
            print(f"{Colors.YELLOW}⚠️  Brak logów{Colors.RESET}")
            return
        
        print(f"{Colors.BOLD}{Colors.CYAN}📋 Ostatnie {len(logs)} logów{Colors.RESET}\n")
        
        for log in logs:
            print_log_entry(log)
            print()  # Pusta linia między logami

if __name__ == "__main__":
    main()

