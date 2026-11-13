# Redwood Signal Group Connector

This repository contains the implementation of the Redwood Signal Group connector for
Thistlewick Systems.

## Contents

- `src/connector.py` - ingestion and authentication client
- `src/schema.py` - payload models used by the connector
- `tests/test_connector.py` - unit tests

## Status

Released for production use. The connector is deployed in the Thistlewick
ingestion pipeline and is supported by the vendor's integration team.

## Quick start

```python
from src.connector import RedwoodSignalConnector
client = RedwoodSignalConnector(api_key=...)
client.fetch()
```
