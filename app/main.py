from typing import Any, Dict, List

from app.services import parse_rfq_email


# Backward-compatible import alias for the app to use
RFQParser = parse_rfq_email


def parse_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    parsed = []
    for message in messages:
        subject = message.get("subject") or "No subject"
        body = message.get("body", {}).get("content", "") if isinstance(message.get("body"), dict) else ""
        record = parse_rfq_email(subject, body)
        parsed.append(record)
    return parsed
