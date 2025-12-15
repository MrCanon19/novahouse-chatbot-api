# ERROR LOG (operacyjne)

Format: data | komponent | objaw | przyczyna | fix

- 2025-12-15 | Cloud SQL | 500/502, auth fail `chatbot_user` | złe hasło w `DATABASE_URL` | zaktualizowano hasło, redeploy
- 2025-12-15 | Cloud SQL socket | 502 podczas startu | brak pełnej nazwy instancji w host path | poprawiono `host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db`
- 2025-12-14 | chatbot.py | IndentationError | wcięcia po hotfixach | poprawki wcięć, py_compile/health OK
- 2025-12-14 | Rate limiter | potencjalny SystemExit Redis | brak REDIS_URL na GAE | wymuszony in-memory fallback, DISABLE_REDIS_RATE_LIMITER=true domyślnie

