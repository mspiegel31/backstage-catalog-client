import json
from pathlib import Path

import httpx
import pytest
import pytest_asyncio

from backstage_catalog_client.api_client import DefaultCatalogApi

DATA_DIR = Path(__file__).parent / "data"

# https://demo.backstage.io/api/catalog/entities
mock_base_url = "https://foo.bar/api/catalog"


@pytest.fixture(scope="session")
def all_entities():
    with open(DATA_DIR / "entities.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def components(all_entities) -> list[dict]:
    return [entity for entity in all_entities if entity["kind"].lower() == "component"]


@pytest_asyncio.fixture(scope="session")
async def httpx_client():
    async with httpx.AsyncClient(base_url=mock_base_url) as client:
        yield client


@pytest.fixture()
def catalog_api(httpx_client: httpx.AsyncClient):
    yield DefaultCatalogApi(mock_base_url)
