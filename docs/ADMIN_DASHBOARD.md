# NovaHouse Chatbot – Admin Dashboard

## Features
- User management (add, remove, block)
- Chatbot usage statistics
- Backup status and logs
- Error monitoring (Sentry integration)
- RODO audit panel
- System health (database, integrations)
- Manual backup trigger
- Telegram alert status

## Access
Dashboard is available for admin users at `/admin/dashboard` (Flask route).

## Security
- Access restricted to admin accounts
- All actions logged
- Sensitive data protected (no secrets in UI)

## Example UI (Flask + Bootstrap)
- Table: Users
- Chart: Usage stats
- Panel: Backup status
- Panel: Sentry errors
- Panel: RODO audit
- Button: Manual backup
- Status: Telegram alerts

## Implementation
- Route: `/admin/dashboard`
- Template: `templates/admin_dashboard.html`
- Backend: Flask, SQLAlchemy
- Frontend: Bootstrap 5

## Next steps
- Implement Flask route and template
- Connect to database and Sentry
- Add backup and Telegram status
- Integrate RODO audit panel

## Automation & Monitoring
- Panel admina pobiera dane z bazy w czasie rzeczywistym
- Status backupu, alertów Telegram i błędów Sentry
- Audyt RODO z checklistą zgodności

## Checklist
- [x] Statystyki użytkowników i wiadomości
- [x] Status backupu
- [x] Status alertów Telegram
- [x] Błędy Sentry
- [x] Audyt RODO
