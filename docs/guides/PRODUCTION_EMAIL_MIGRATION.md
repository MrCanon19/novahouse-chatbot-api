# Production migration for `chat_conversations.email`

This guide walks through running the idempotent email-column migration against the production Cloud SQL database. Follow the steps in order to avoid connection and shell pitfalls (notably the `!` character in the password).

## 1) Collect the production connection string

Read `app.yaml` (or `app.yaml.deploy`) for the credentials and database name. The format you will need later is:

```
postgresql+psycopg2://<user>:<password>@127.0.0.1:5432/<database>
```

Example from production:

```
postgresql+psycopg2://chatbot_user:NovaH0use2025!DB@127.0.0.1:5432/chatbot
```

## 2) Open a Cloud SQL tunnel

Set the project and start the Cloud SQL Auth Proxy on port 5432. Install it first via Homebrew if it is not available.

```bash
gcloud config set project glass-core-467907-e9
cloud-sql-proxy glass-core-467907-e9:europe-west1:novahouse-chatbot-db --port=5432
```

Keep the proxy running in its own terminal window.

## 3) Export `DATABASE_URL` safely and activate the venv

In a separate terminal, switch to the project, activate the virtual environment, and export the URL using **single quotes** (so zsh does not treat `!` as history expansion).

```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
source novahouse/bin/activate
export DATABASE_URL='postgresql+psycopg2://chatbot_user:NovaH0use2025!DB@127.0.0.1:5432/chatbot'
```

If your runner checks `SQLALCHEMY_DATABASE_URI`, export it to the same value as well.

## 4) Run the production migration runner

Execute the migration script while the proxy is active:

```bash
python migrations/run_production_migration.py
```

You should see logs indicating either that the `email` column and `ix_chat_conversations_email` index were added or that they already exist.

## 5) Verify directly in the database

Connect to the instance via `gcloud sql connect` and inspect the table:

```bash
gcloud sql connect novahouse-chatbot-db --user=chatbot_user --database=chatbot
```

Within `psql`:

```sql
\d chat_conversations
```

Confirm that:

- The `email` column is present.
- The `ix_chat_conversations_email` index exists.

Exit with `\q`.

## 6) Smoke-test the app and logs

After the migration, check application health and confirm the `UndefinedColumn` error is gone:

```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health
gcloud app logs read -s default --limit=50 | grep -E "chat_conversations\.email|UndefinedColumn"
```

If the grep produces no output and the health endpoint responds, the email column issue is resolved. If errors persist, verify that the database and instance you connected to match the values used by App Engine.
