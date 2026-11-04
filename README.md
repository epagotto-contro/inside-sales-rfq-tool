# Inside Sales RFQ Tool

A web app for reading a shared Outlook mailbox, identifying RFQ emails, and listing them in a structured dashboard by:

- Customer Name
- Contact Name
- Items to be quoted
- Category (SRV, Control Valves, MSA, E+H)
- Urgency of RFQ

## Overview

This project is a starter implementation for a Microsoft 365-based shared mailbox workflow.

It does the following:

1. Connects to Microsoft Graph using OAuth.
2. Reads messages from the configured shared mailbox.
3. Parses the email text to detect quote-request details.
4. Stores and displays the results in a web dashboard.

## Tech stack

- Python 3.11+
- FastAPI
- Microsoft Graph API
- SQLite (for local persistence)
- Jinja2 templates
- Bootstrap CSS

## Requirements

- A Microsoft 365 tenant
- An app registration in Azure AD / Entra ID
- Shared mailbox access granted to the app
- A user or service account able to consent to the required Graph scopes

## Environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Example values:

```env
TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET=your-client-secret
SHARED_MAILBOX=rfq@contoso.com
GRAPH_SCOPE=https://graph.microsoft.com/.default
APP_SECRET_KEY=change-this-secret
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- http://localhost:8000

## Notes

- The app starts in a safe "demo mode" if Graph is not configured, so the dashboard can still run without live mailbox access.
- A real deployment should use proper secrets management and a production web server.
- You will likely need to grant delegate or application permission depending on whether you use user-based OAuth or app-only access.

## Optional next steps

- Add authentication for internal users
- Add a queue inbox filter by category or urgency
- Add email threading / deduplication
- Add CSV export
- Add webhook-based polling for new shared mailbox messages
