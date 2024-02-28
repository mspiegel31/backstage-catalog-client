import pytest

from backstage_catalog_client.api_client import CatalogApi
from backstage_catalog_client.models import GetEntitiesRequest


@pytest.mark.asyncio(scope="class")
class TestGetEntities:
    @staticmethod
    async def test_it_should_fetch_from_the_correct_endpoint(catalog_api: CatalogApi):
        request = GetEntitiesRequest()
        response = await catalog_api.getEntities(request, options=None)
        assert response.items
