"""Schema helpers for the Redwood Signal Group connector."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict


@dataclass
class Record:
    external_id: str
    amount: Decimal
    captured_at: str | None = None
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Record":
        return cls(
            external_id=str(data["id"]),
            amount=Decimal(str(data.get("amount", 0))),
            captured_at=data.get("timestamp"),
            payload=data,
        )
