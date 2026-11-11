"""Fake backend for the Brightcart store. You do not need to change this file.

Everything is in memory. Restarting the program resets the data.
"""

import json
import uuid
from datetime import date
from pathlib import Path

# Fixed "today" so refund-window math gives the same answer whatever day you run this.
TODAY = date(2026, 11, 11)

REFUND_WINDOW_DAYS = 30
MAX_AUTO_REFUND = 500.00

_DATA = json.loads((Path(__file__).parent / "data" / "store.json").read_text())
_TICKETS: list[dict] = []


class NotFoundError(Exception):
    pass


def _find_order(order_id: str) -> tuple[str, dict]:
    """Return (normalised id, stored order). Raises NotFoundError."""
    key = order_id.strip().upper()
    order = _DATA["orders"].get(key)
    if order is None:
        raise NotFoundError(f"No order with id {order_id!r}")
    return key, order


def get_order(order_id: str) -> dict:
    """Return the order plus the customer's name. Raises NotFoundError."""
    key, order = _find_order(order_id)
    customer = _DATA["customers"][order["customer_id"]]
    return {"order_id": key, **order, "customer_name": customer["name"]}


def search_faq(query: str) -> list[dict]:
    """Naive keyword search over the FAQ. Returns matching entries (may be empty)."""
    words = {w.lower().strip("?.,!") for w in query.split() if len(w) > 2}
    hits = []
    for entry in _DATA["faq"]:
        text = f"{entry['topic']} {entry['question']} {entry['answer']}".lower()
        if any(w in text for w in words):
            hits.append(entry)
    return hits


def issue_refund(order_id: str, reason: str) -> dict:
    """Mark the order as refunded. Does NOT check any policy. That is the caller's job."""
    key, order = _find_order(order_id)
    order["status"] = "refunded"
    return {"order_id": key, "refunded_amount": order["total"], "reason": reason}


def create_ticket(summary: str, order_id: str | None = None) -> dict:
    """Open a ticket for a human agent."""
    ticket = {"ticket_id": f"T-{uuid.uuid4().hex[:6].upper()}", "summary": summary, "order_id": order_id}
    _TICKETS.append(ticket)
    return ticket


def list_tickets() -> list[dict]:
    return list(_TICKETS)
