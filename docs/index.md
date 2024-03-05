# backstage-catalog-client

[![Release](https://img.shields.io/github/v/release/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/v/release/mspiegel31/backstage-catalog-client)
[![Build status](https://img.shields.io/github/actions/workflow/status/mspiegel31/backstage-catalog-client/main.yml?branch=main)](https://github.com/mspiegel31/backstage-catalog-client/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/commit-activity/m/mspiegel31/backstage-catalog-client)
[![License](https://img.shields.io/github/license/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/license/mspiegel31/backstage-catalog-client)

A python client for the Backstage catalog API. Only uses native python datatypes.

# Usage

To use a ready-made client, import it and make requests

```python
import asyncio
import json
from backstage_catalog_client.httpx_client import HttpxClient


async def main():
    catalog = HttpxClient("https://demo.backstage.io/")
    data = await catalog.get_entities()
    for entity in data.items[:1]:
        print(json.dumps(entity, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

# Building your own client

This package exports both an `AsyncCatalogApi` and a `SyncCatalogApi` as python [protocols](https://typing.readthedocs.io/en/latest/spec/protocol.html#protocols). You can use these to implement your own clients for the Catalog API.

For example, if you'd like to implement your own synchronous Catalog API client:

```python
from typing import List
from backstage_catalog_client.raw_entity import RawEntity
from backstage_catalog_client.catalog_api.sync_api import SyncCatalogApi
from backstage_catalog_client.models import GetEntitiesResponse

class HighPerformanceCatalogApi(SyncCatalogApi):
    """
    A high-performance client that never makes a network request.
    Stable, speedy, and (relatively) useless
    """
    def getEntities(self, request=None, options=None) -> GetEntitiesResponse:
        items: List[RawEntity] = [
            {
                "apiVersion": "backstage.io/v1alpha1",
                "kind": "Component",
                "metadata": {
                    "name": "wayback-search",
                    "namespace": "default"
                },
                "spec": {
                    "type": "service",
                    "owner": "team-a",
                    "lifecycle": "experimental"
                }
            }
        ]
        return GetEntitiesResponse(items=items)
    # ... other methods ...


def main():
    client: SyncCatalogApi = HighPerformanceCatalogApi()
    data = client.get_entities()
    for item in data.items:
        print(item)

if __name__ == "__main__":
    main()

```
