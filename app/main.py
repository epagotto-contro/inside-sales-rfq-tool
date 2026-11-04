from typing import Any, Dict, List

import httpx
from msal import ConfidentialClientApplication

from app.config import get_settings


async def get_access_token() -> str:
    settings = get_settings()
    if not settings.tenant_id or not settings.client_id or not settings.client_secret:
        raise ValueError("Microsoft Graph credentials are not configured.")

    app = ConfidentialClientApplication(
        client_id=settings.client_id,
        authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        client_credential=settings.client_secret,
    )

    token = app.acquire_token_for_client(scopes=[settings.graph_scope])
    if not token or "access_token" not in token:
        raise RuntimeError(f"Unable to fetch Graph token: {token}")
    return token["access_token"]


async def fetch_shared_mailbox_messages() -> List[Dict[str, Any]]:
    settings = get_settings()
    if not settings.shared_mailbox:
        return []

    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Prefer": "outlook.body-content=\"true\""}
    url = (
        f"https://graph.microsoft.com/v1.0/users/{settings.shared_mailbox}/messages"
        f"?$top=25&$select=subject,body,from,receivedDateTime"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return payload.get("value", [])
