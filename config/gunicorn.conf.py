# Gunicorn configuration file for production deployment

import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', '2'))
worker_class = "sync"  # Zmiana z gthread na sync - stabilniejsze na App Engine
worker_connections = 1000
timeout = 120  # Zwiększono dla wolnych analytics queries i cold starts
graceful_timeout = 30  # Graceful shutdown time
keepalive = 5

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 500  # Zmniejszono - częstszy restart = mniej memory leaks
max_requests_jitter = 50

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

