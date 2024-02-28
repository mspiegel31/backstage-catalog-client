import httpx
import pytest
import respx
from conftest import mock_base_url

from backstage_catalog_client.api_client import CATALOG_FILTER_EXISTS, CatalogApi
from backstage_catalog_client.models import GetEntitiesRequest


@pytest.fixture(scope="session")
def entities_subset(all_entities) -> list[dict]:
    return all_entities[:2]


@pytest.fixture(scope="session")
def entities_response(entities_subset) -> httpx.Response:
    return httpx.Response(200, json=entities_subset)


@pytest.fixture()
def mocked_entities(entities_response: httpx.Response):
    with respx.mock(base_url=mock_base_url) as respx_mock:
        respx_mock.get(f"{mock_base_url}/entities").mock(return_value=entities_response)
        yield respx_mock


@pytest.mark.asyncio(scope="class")
class TestGetEntities:
    @staticmethod
    @pytest.fixture(autouse=True)
    def _setup(mocked_entities):
        pass

    @staticmethod
    async def test_it_should_fetch_from_the_correct_endpoint(catalog_api: CatalogApi, entities_subset):
        request = GetEntitiesRequest()
        response = await catalog_api.getEntities(request, options=None)
        final_entities = [item.model_dump(exclude_unset=True) for item in response.items]
        assert final_entities == entities_subset

    @staticmethod
    async def test_it_should_build_multiple_entity_search_params_properly(
        catalog_api: CatalogApi, mocked_entities: respx.Router
    ):
        query_filter = [
            {"a": "1"},
            {"b": ["2", "3"]},
            {"c": "="},
            {"d": CATALOG_FILTER_EXISTS},
        ]
        request = GetEntitiesRequest(filter=query_filter)
        await catalog_api.getEntities(request)
        actual = mocked_entities.calls.last.request.url.params.get_list("filter")
        assert actual == ["a=1", "b=2,b=3", "c==", "d"]

    @staticmethod
    async def test_it_builds_search_filters_properly_even_with_URL_unsafe_values(
        catalog_api: CatalogApi, mocked_entities: respx.Router
    ):
        query_filter = [
            {
                "!@#$%": "t?i=1&a:2",
                "^&*(){}[]": ["t%^url*encoded2", "url"],
            }
        ]
        await catalog_api.getEntities(GetEntitiesRequest(filter=query_filter))
        actual = mocked_entities.calls.last.request.url.params.get_list("filter")
        assert actual == ["!@#$%=t?i=1&a:2,^&*(){}[]=t%^url*encoded2,^&*(){}[]=url"]

    @staticmethod
    async def test_it_builds_entity_field_selector_properly(catalog_api: CatalogApi, mocked_entities: respx.Router):
        request = GetEntitiesRequest(fields=["metadata.name", "spec.type"])
        await catalog_api.getEntities(request)
        actual = mocked_entities.calls.last.request.url.params.get_list("fields")
        assert actual == ["metadata.name", "spec.type"]

    @staticmethod
    async def test_it_handles_field_filterd_entities(catalog_api: CatalogApi, mocked_entities: respx.Router):
        mocked_entities.get(f"{mock_base_url}/entities").mock(
            return_value=httpx.Response(200, json=[{"apiVersion": "1"}, {"apiVersion": "2"}])
        )
        request = GetEntitiesRequest(fields=["apiVersion"])
        response = await catalog_api.getEntities(request)
        actual = [item.model_dump(exclude_unset=True) for item in response.items]
        assert actual == [{"apiVersion": "1"}, {"apiVersion": "2"}]
