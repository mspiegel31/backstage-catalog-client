import json
from pathlib import Path

import httpx
import pytest
import pytest_asyncio
import respx

from backstage_catalog_client.api_client import DefaultCatalogApi

DATA_DIR = Path(__file__).parent / "data"
# https://demo.backstage.io/api/catalog/entities
mock_base_url = "https://foo.bar/api/catalog"


@pytest.fixture(scope="session")
def entities():
    with open(DATA_DIR / "entities.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def entities_response(entities) -> httpx.Response:
    return httpx.Response(200, json=entities)


@pytest.fixture()
def mocked_entities(entities_response: httpx.Response):
    with respx.mock(base_url=mock_base_url) as respx_mock:
        respx_mock.get(f"{mock_base_url}/entities").mock(return_value=entities_response)
        yield respx_mock


@pytest_asyncio.fixture(scope="session")
async def httpx_client():
    async with httpx.AsyncClient(base_url=mock_base_url) as client:
        yield client


@pytest.fixture()
def catalog_api(httpx_client: httpx.AsyncClient):
    yield DefaultCatalogApi(httpx_client)
