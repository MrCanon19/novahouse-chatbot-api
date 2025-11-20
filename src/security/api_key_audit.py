import os
from datetime import datetime

AUDIT_LOG = os.getenv("API_KEY_AUDIT_LOG", "logs/api_key_audit.log")


def log_api_key_usage(service: str, key_id: str, user: str = "system"):
    with open(AUDIT_LOG, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {service} | {key_id} | {user}\n")


def report_api_key_usage():
    if not os.path.exists(AUDIT_LOG):
        return []
    with open(AUDIT_LOG) as f:
        return f.readlines()


def rotate_api_key(env_var: str, new_value: str):
    os.environ[env_var] = new_value
    log_api_key_usage(env_var, "ROTATED", user="admin")
    # Można dodać alert do Sentry lub email
