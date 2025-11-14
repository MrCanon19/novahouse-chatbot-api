# RODO / Chatbot — Quick runbook

This file contains quick instructions to run the local API, test RODO endpoints and export user data for GDPR requests.

Prerequisites
- Python 3.10+ (this project uses a virtualenv named `venv`)
- Project dependencies installed: `pip install -r requirements.txt`

Start server (development, foreground — recommended for debugging)

```bash
cd ~/Projects/manus/novahouse-chatbot-api
source venv/bin/activate
python src/main.py
```

Start server (background, production-like — disables reloader)

```bash
cd ~/Projects/manus/novahouse-chatbot-api
source venv/bin/activate
FLASK_ENV=production nohup python src/main.py > server.log 2>&1 &
```

Save RODO consent (example)

```bash
curl -X POST http://127.0.0.1:8080/api/chatbot/rodo-consent \
  -H "Content-Type: application/json" \
  -d '{"session_id":"session-123","consent_given":true}'
```

Export all data for a session (admin endpoint)

- If you have set `ADMIN_API_KEY` in the environment, include header `X-ADMIN-API-KEY: <key>`.

```bash
# without admin key (if ADMIN_API_KEY not set)
curl -s http://127.0.0.1:8080/api/chatbot/export-data/session-123 | jq .

# with admin key
curl -s http://127.0.0.1:8080/api/chatbot/export-data/session-123 \
  -H "X-ADMIN-API-KEY: ${ADMIN_API_KEY}" | jq .
```

Delete user data (GDPR right to be forgotten)

```bash
curl -X DELETE http://127.0.0.1:8080/api/chatbot/delete-my-data \
  -H "Content-Type: application/json" \
  -d '{"session_id":"session-123"}'
```

Tests

A small pytest is included under `tests/` — run it with:

```bash
source venv/bin/activate
pytest -q
```

Notes
- The admin key is optional. If you want to protect export endpoints, set `ADMIN_API_KEY` in the environment before starting the app.
- For production use a WSGI server (gunicorn) and secure the admin endpoints behind authentication and transport TLS.

Run scripts

Use the provided scripts to start/stop the server locally (background, production-like):

```bash
# Start
./start.sh

# Stop
./stop.sh
```

Systemd / gunicorn example

An example systemd unit file for running the app with gunicorn is provided in `deploy/gunicorn.service`.
Edit `WorkingDirectory`, `PATH` and `ExecStart` to match your installation path and set a secure `ADMIN_API_KEY` in the Environment.

Security reminder

Always protect admin endpoints in production. Set `ADMIN_API_KEY` and place the app behind TLS. Consider adding OAuth or reverse-proxy authentication for management endpoints.
