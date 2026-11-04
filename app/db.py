import os
import sqlite3
from typing import Any, Dict, List

DB_PATH = os.path.join(os.path.dirname(__file__), "rfq.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS rfq_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            contact_name TEXT,
            items TEXT,
            category TEXT,
            urgency TEXT,
            subject TEXT,
            source TEXT,
            received_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_request(record: Dict[str, Any]) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO rfq_requests (
            customer_name, contact_name, items, category, urgency, subject, source, received_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.get("customer_name"),
            record.get("contact_name"),
            record.get("items"),
            record.get("category"),
            record.get("urgency"),
            record.get("subject"),
            record.get("source"),
            record.get("received_at"),
        ),
    )
    conn.commit()
    conn.close()


def get_requests() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM rfq_requests ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_requests() -> None:
    conn = get_connection()
    conn.execute("DELETE FROM rfq_requests")
    conn.commit()
    conn.close()
