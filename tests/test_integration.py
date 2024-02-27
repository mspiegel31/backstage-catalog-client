import pytest
import respx

from backstage_catalog_client.api_client import CatalogApi
from backstage_catalog_client.models import GetEntitiesRequest

mock_base_url = "https://foo.bar/api/catalog"


@pytest.mark.respx(base_url=mock_base_url)
@pytest.mark.asyncio(scope="session")
async def test_basic_query(catalog_api: CatalogApi, mocked_entities: respx.Router):
    filter = [
        {"kind": ["component"]},
    ]
    request = GetEntitiesRequest(filter=filter)
    response = await catalog_api.getEntities(request, options=None)
    assert response.items


@pytest.mark.asyncio(scope="session")
async def test_singular_query(catalog_api: CatalogApi, mocked_entities: respx.Router):
    filter = [
        {"kind": "component"},
    ]
    request = GetEntitiesRequest(filter=filter)
    response = await catalog_api.getEntities(request, options=None)

    assert response.items
