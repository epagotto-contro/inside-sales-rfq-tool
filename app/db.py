from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("RFQ_DB_PATH", Path(__file__).resolve().parent / "rfq.db"))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS rfq_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                customer_name TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                items TEXT NOT NULL,
                category TEXT NOT NULL,
                urgency TEXT NOT NULL,
                subject TEXT NOT NULL,
                web_link TEXT,
                received_at TEXT NOT NULL
            )
            """
        )
        # Allow the app to start when using a database created by the first scaffold.
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(rfq_requests)")}
        if "message_id" not in columns:
            connection.execute("ALTER TABLE rfq_requests ADD COLUMN message_id TEXT")
        if "web_link" not in columns:
            connection.execute("ALTER TABLE rfq_requests ADD COLUMN web_link TEXT")
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_rfq_message_id ON rfq_requests(message_id)"
        )


def save_request(record: dict[str, Any]) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO rfq_requests (
                message_id, customer_name, contact_name, items, category, urgency,
                subject, web_link, received_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(message_id) DO UPDATE SET
                customer_name = excluded.customer_name,
                contact_name = excluded.contact_name,
                items = excluded.items,
                category = excluded.category,
                urgency = excluded.urgency,
                subject = excluded.subject,
                web_link = excluded.web_link,
                received_at = excluded.received_at
            """,
            (
                record.get("message_id"),
                record.get("customer_name", "Unknown"),
                record.get("contact_name", "Unknown"),
                record.get("items", "Not specified"),
                record.get("category", "Unclassified"),
                record.get("urgency", "Not specified"),
                record.get("subject", "No subject"),
                record.get("web_link"),
                record.get("received_at", ""),
            ),
        )


def get_requests() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM rfq_requests ORDER BY received_at DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]
