"""Unit tests for the Redwood Signal Group connector."""

from decimal import Decimal

from src.connector import RedwoodSignalConnector
from src.schema import Record


def test_record_from_api():
    record = Record.from_api({"id": 42, "amount": "10.50"})
    assert record.external_id == "42"
    assert record.amount == Decimal("10.50")


def test_client_requires_key():
    try:
        RedwoodSignalConnector(api_key="")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
