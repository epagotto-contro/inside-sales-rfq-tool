import re
from datetime import datetime
from typing import Any, Dict, List, Optional


CATEGORY_MAP = {
    "SRV": "SRV",
    "SERVICE": "SRV",
    "CONTROL VALVES": "Control Valves",
    "VALVES": "Control Valves",
    "MSA": "MSA",
    "E+H": "E+H",
    "EH": "E+H",
}


def normalize_category(raw: str) -> Optional[str]:
    if not raw:
        return None
    cleaned = raw.strip().upper()
    if cleaned.startswith("E+H") or cleaned.startswith("EH"):
        return "E+H"
    if cleaned.startswith("CONTROL VALVE"):
        return "Control Valves"
    return CATEGORY_MAP.get(cleaned)


def detect_category(subject: str, body: str) -> Optional[str]:
    text = f"{subject} {body or ''}".upper()
    patterns = [
        r"\bSRV\b",
        r"\bSERVICE\b",
        r"\bCONTROL VALVE(S)?\b",
        r"\bVALVES?\b",
        r"\bMSA\b",
        r"\bE\+H\b",
        r"\bEH\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return normalize_category(match.group(0))
    return None


def extract_from_patterns(text: str, patterns: List[str]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            candidate = match.group(1).strip()
            if candidate:
                return candidate
    return None


def extract_customer_name(subject: str, body: str) -> Optional[str]:
    text = f"{subject}\n{body or ''}"
    patterns = [
        r"customer\s*(?:name)?\s*[:\-]\s*(.+)",
        r"company\s*(?:name)?\s*[:\-]\s*(.+)",
    ]
    return extract_from_patterns(text, patterns)


def extract_contact_name(subject: str, body: str) -> Optional[str]:
    text = f"{subject}\n{body or ''}"
    patterns = [
        r"contact\s*(?:name)?\s*[:\-]\s*(.+)",
        r"requested\s*by\s*[:\-]\s*(.+)",
        r"from\s*[:\-]\s*(.+)",
    ]
    value = extract_from_patterns(text, patterns)
    if value:
        return re.split(r"\n|<|\(|\b(?:email|phone)\b", value, maxsplit=1)[0].strip()
    return None


def extract_items(subject: str, body: str) -> Optional[str]:
    text = f"{subject}\n{body or ''}"
    patterns = [
        r"items?\s*(?:to\s*be\s*quoted|for\s*quote|to\s*quote)\s*[:\-]\s*(.+)",
        r"description\s*[:\-]\s*(.+)",
        r"part(s)?\s*(?:number|numbers)\s*[:\-]\s*(.+)",
    ]
    value = extract_from_patterns(text, patterns)
    if value:
        return value.strip()
    return None


def extract_urgency(subject: str, body: str) -> Optional[str]:
    text = f"{subject}\n{body or ''}".lower()
    if "urgent" in text or "asap" in text:
        return "Urgent"
    if "today" in text or "tomorrow" in text or "within 2 days" in text or "48h" in text:
        return "High"
    if "this week" in text or "1 week" in text or "deadline" in text:
        return "Medium"
    if "next week" in text or "later" in text:
        return "Low"
    return "Not specified"


def parse_rfq_email(subject: str, body: str) -> Dict[str, Any]:
    cleaned_body = (body or "").replace("\r", "")
    normalized_subject = (subject or "").strip()

    record = {
        "customer_name": extract_customer_name(normalized_subject, cleaned_body) or "Unknown",
        "contact_name": extract_contact_name(normalized_subject, cleaned_body) or "Unknown",
        "items": extract_items(normalized_subject, cleaned_body) or "Not specified",
        "category": detect_category(normalized_subject, cleaned_body) or "Unclassified",
        "urgency": extract_urgency(normalized_subject, cleaned_body),
        "subject": normalized_subject or "No subject",
        "source": "outlook-shared-mailbox",
        "received_at": datetime.utcnow().isoformat(),
    }
    return record


def parse_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    parsed: List[Dict[str, Any]] = []
    for message in messages:
        subject = message.get("subject") or "No subject"
        body = ""
        raw_body = message.get("body")
        if isinstance(raw_body, dict):
            body = raw_body.get("content", "")
        parsed.append(parse_rfq_email(subject, body))
    return parsed
