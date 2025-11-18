# Gunicorn configuration file for production deployment

import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
backlog = 2048

# Worker processes - OPTIMIZED
workers = int(os.environ.get('GUNICORN_WORKERS', '4'))  # Zwiększono z 2 do 4
worker_class = "gthread"  # Zmieniono z sync na gthread dla lepszej wydajności
threads = 2  # 2 wątki na worker = 8 równoczesnych requestów
worker_connections = 1000
timeout = 60  # Zwiększono z 30 do 60 dla wolniejszych requestów
keepalive = 5  # Zwiększono z 2 do 5

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 2000  # Zwiększono z 1000
max_requests_jitter = 100  # Zwiększono z 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'novahouse-chatbot'

# Server mechanics
preload_app = True
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

