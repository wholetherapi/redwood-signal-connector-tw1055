"""Production connector for Redwood Signal Group.

The module implements the read/transform client used by the Thistlewick
ingestion pipeline. It is released and supported by the vendor integration
team.
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Any, Dict, Iterable, List

DEFAULT_TIMEOUT = 30


class RedwoodSignalConnector:
    """Client for the Redwood Signal Group data-exchange API."""

    def __init__(self, api_key: str, endpoint: str = "https://api.redwoodsignal.com") -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "thistlewick-connector/1.0",
        }

    def fetch(self, since: str | None = None, limit: int = 500) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if since:
            params["since"] = since
        response = self._request("GET", "/v1/records", params=params)
        return list(self._normalise(response.get("records", [])))

    def _normalise(self, records: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
        for record in records:
            yield {
                "external_id": str(record.get("id")),
                "amount": Decimal(str(record.get("amount", 0))),
                "captured_at": record.get("timestamp"),
                "payload": record,
            }

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        import urllib.request

        url = self.endpoint + path
        request = urllib.request.Request(url, method=method, headers=self._headers())
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as handle:
            return json.loads(handle.read().decode("utf-8"))
