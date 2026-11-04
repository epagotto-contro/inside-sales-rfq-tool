from __future__ import annotations

import re
from datetime import datetime, timezone
from html import unescape
from typing import Any


CATEGORY_PATTERNS = (
    ("Control Valves", re.compile(r"\bcontrol\s+valves?\b", re.I)),
    ("SRV", re.compile(r"\bSRV\b", re.I)),
    ("MSA", re.compile(r"\bMSA\b", re.I)),
    ("E+H", re.compile(r"\bE\s*\+\s*H\b|\bEndress\s*\+\s*Hauser\b", re.I)),
)


def clean_body(value: str) -> str:
    value = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", value or "")
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = unescape(value)
    return re.sub(r"[ \t]+", " ", value).replace("\r", "")


def is_quote_request(subject: str, body: str) -> bool:
    text = f"{subject}\n{body}".lower()
    return bool(re.search(r"\b(rfq|quote|quotation|pricing)\b", text))


def _label_value(text: str, labels: str) -> str | None:
    match = re.search(rf"(?im)^\s*(?:{labels})\s*[:\-]\s*([^\n]+)", text)
    return match.group(1).strip(" \t;,.\r") if match else None


def parse_rfq_email(subject: str, body: str) -> dict[str, Any]:
    subject = (subject or "No subject").strip()
    body = clean_body(body)
    text = f"{subject}\n{body}"

    customer = _label_value(text, r"customer(?:\s+name)?|company(?:\s+name)?")
    contact = _label_value(text, r"contact(?:\s+name)?|requested\s+by")
    items = _label_value(
        text,
        r"items?(?:\s+to\s+be\s+quoted|\s+for\s+quote|\s+to\s+quote)?|description|part\s+numbers?",
    )

    category = "Unclassified"
    for label, pattern in CATEGORY_PATTERNS:
        if pattern.search(text):
            category = label
            break

    lowered = text.lower()
    if re.search(r"\b(urgent|asap|immediately)\b", lowered):
        urgency = "Urgent"
    elif re.search(r"\b(today|tomorrow|within\s+2\s+days?|48\s*hours?)\b", lowered):
        urgency = "High"
    elif re.search(r"\b(this week|within\s+a week|1 week|deadline)\b", lowered):
        urgency = "Medium"
    elif re.search(r"\b(next week|no rush|when convenient)\b", lowered):
        urgency = "Low"
    else:
        urgency = "Not specified"

    return {
        "customer_name": customer or "Unknown",
        "contact_name": contact or "Unknown",
        "items": items or "Not specified",
        "category": category,
        "urgency": urgency,
        "subject": subject,
    }


def parse_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parsed = []
    for message in messages:
        subject = message.get("subject") or "No subject"
        body_part = message.get("body") or {}
        body = body_part.get("content", "") if isinstance(body_part, dict) else ""
        if not is_quote_request(subject, clean_body(body)):
            continue
        record = parse_rfq_email(subject, body)
        record.update(
            {
                "message_id": message.get("id"),
                "web_link": message.get("webLink"),
                "received_at": message.get("receivedDateTime")
                or datetime.now(timezone.utc).isoformat(),
            }
        )
        parsed.append(record)
    return parsed
