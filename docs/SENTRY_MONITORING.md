# NovaHouse Chatbot – Sentry Monitoring

## What is monitored?
- Application errors (Flask)
- Performance metrics
- Logs and traces
- Profiling

## How it works
- Sentry SDK integrated in `main.py` and `src/main.py`
- DSN set via environment variable `SENTRY_DSN`
- Errors and performance sent to Sentry dashboard

## Setup
1. Install:
   ```sh
   pip install "sentry-sdk[flask]"
   ```
2. Set DSN:
   ```sh
   export SENTRY_DSN="<your-dsn>"
   ```
3. Run app and test endpoint:
   ```sh
   python3 main.py
   # Visit http://localhost:8080/sentry-test
   ```

## Example error
- Division by zero at `/sentry-test` route
- Error visible in Sentry dashboard
