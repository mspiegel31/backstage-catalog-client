import httpx
import pytest
import pytest_asyncio

from backstage_catalog_client.api_client import CatalogApi, DefaultCatalogApi
from backstage_catalog_client.models import GetEntitiesRequest


@pytest_asyncio.fixture(scope="session")
async def httpx_client():
    async with httpx.AsyncClient(base_url="https://demo.backstage.io/api/catalog") as client:
        yield client


@pytest.fixture()
def catalog_api(httpx_client: httpx.AsyncClient):
    yield DefaultCatalogApi(httpx_client)


@pytest.mark.asyncio(scope="session")
async def test_basic_query(catalog_api: CatalogApi):
    filter = [
        {"kind": ["component"]},
    ]
    request = GetEntitiesRequest(filter=filter)
    response = await catalog_api.getEntities(request, options=None)
    assert response.items


@pytest.mark.asyncio(scope="session")
async def test_singular_query(catalog_api: CatalogApi):
    filter = [
        {"kind": "component"},
    ]
    request = GetEntitiesRequest(filter=filter)
    response = await catalog_api.getEntities(request, options=None)
    assert response.items
