from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.db import get_requests, init_db, save_request
from app.services.graph_client import fetch_shared_mailbox_messages
from app.services.rfq_parser import parse_messages


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Inside Sales RFQ Tool", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

DEMO_REQUESTS = [
    {
        "id": 1,
        "customer_name": "Global Energy Systems",
        "contact_name": "Megan Collins",
        "items": "Pressure transmitters and valve assemblies",
        "category": "Control Valves",
        "urgency": "Urgent",
        "subject": "RFQ - Control Valve package / urgent",
        "web_link": None,
        "received_at": "2026-11-04T12:02:00+00:00",
    },
    {
        "id": 2,
        "customer_name": "Precision Foods",
        "contact_name": "Luis Ortega",
        "items": "Flow meters and SRV replacement kit",
        "category": "SRV",
        "urgency": "High",
        "subject": "Quote request for service replacement",
        "web_link": None,
        "received_at": "2026-11-04T11:15:00+00:00",
    },
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, status: str | None = None):
    settings = get_settings()
    rows = get_requests()
    demo_mode = not settings.graph_configured and not rows
    if demo_mode:
        rows = DEMO_REQUESTS
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "requests": rows,
            "shared_mailbox": settings.shared_mailbox,
            "demo_mode": demo_mode,
            "status": status,
        },
    )


@app.post("/sync")
async def sync_mailbox():
    settings = get_settings()
    if not settings.graph_configured:
        return RedirectResponse("/?status=Configure+Microsoft+Graph+settings+in+.env+first.", status_code=303)
    try:
        messages = await fetch_shared_mailbox_messages()
        parsed = parse_messages(messages)
        for record in parsed:
            save_request(record)
        status = f"Sync complete: {len(parsed)} RFQ message(s) processed."
    except Exception:
        status = "Sync failed. Check Microsoft Graph permissions, mailbox settings, and server logs."
    return RedirectResponse(f"/?status={status.replace(' ', '+')}", status_code=303)


@app.get("/api/quotes")
async def quotes() -> list[dict[str, Any]]:
    rows = get_requests()
    return rows if rows else DEMO_REQUESTS
