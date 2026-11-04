from typing import Any
from urllib.parse import quote

import httpx
from msal import ConfidentialClientApplication

from app.config import get_settings

GRAPH_ROOT = "https://graph.microsoft.com/v1.0"


def _access_token() -> str:
    settings = get_settings()
    application = ConfidentialClientApplication(
        client_id=settings.client_id,
        authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        client_credential=settings.client_secret,
    )
    result = application.acquire_token_for_client(scopes=[settings.graph_scope])
    if "access_token" not in result:
        # Do not expose token response details or credentials in the UI/log output.
        raise RuntimeError("Microsoft Graph authentication failed. Check app registration and consent.")
    return result["access_token"]


async def fetch_shared_mailbox_messages() -> list[dict[str, Any]]:
    settings = get_settings()
    if not settings.graph_configured:
        raise RuntimeError("Microsoft Graph mailbox settings are incomplete.")

    mailbox = quote(settings.shared_mailbox, safe="")
    url = f"{GRAPH_ROOT}/users/{mailbox}/messages"
    headers = {
        "Authorization": f"Bearer {_access_token()}",
        "Prefer": 'outlook.body-content-type="html"',
    }
    params = {
        "$top": "50",
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,body,from,receivedDateTime,webLink",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("value", [])
