# Inside Sales RFQ Tool

A small web dashboard that organizes Outlook shared-mailbox quote requests into customer, contact, items, category, and urgency fields. It uses Microsoft Graph (not browser scraping) and stores synced requests in a local SQLite database.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Without Microsoft Graph credentials the dashboard displays sample data. The **Sync mailbox** button will work after configuration below. The JSON endpoint is `/api/quotes`.

## Microsoft 365 / Graph setup

1. Register an application in Microsoft Entra ID.
2. Add the Microsoft Graph **Application** permission `Mail.Read` and obtain tenant admin consent. For a production environment, restrict the app to only the intended shared mailbox using your organization's supported Exchange application access controls.
3. Create a client secret and set `TENANT_ID`, `CLIENT_ID`, and `CLIENT_SECRET` in `.env`.
4. Set `SHARED_MAILBOX` to the shared mailbox email address.
5. Restart the app and click **Sync mailbox**.

Protect the client secret. Do not commit `.env` or use this development server as a production deployment. The Graph app-only permission can grant broad mailbox access if not appropriately restricted; have your Microsoft 365 administrator review the permission and access policy.

## What the app does

- Fetches up to 50 recent messages from the configured mailbox on manual sync.
- Keeps messages that appear to mention an RFQ, quote, quotation, or pricing.
- Extracts simple labeled fields and category/urgency hints. Those guesses should be checked against the email before quoting.
- Stores messages by Graph message ID to avoid adding a duplicate on each sync.
- Shows a link back to each email when Microsoft Graph provides one.

This is an initial working prototype. Extraction rules are intentionally conservative and may need adapting to the formats used by your customers.
