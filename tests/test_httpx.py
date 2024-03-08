from typing import Callable, List

import httpx
import pytest
import respx
from conftest import mock_base_url

from backstage_catalog_client.catalog_api.async_api import AsyncCatalogApi
from backstage_catalog_client.catalog_api.util import CATALOG_FILTER_EXISTS
from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import CompoundEntityRef, GetEntitiesRequest

entities: List[Entity] = [
    {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {"name": "wayback-search"},
        "spec": {"type": "service"},
    },
    {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {"name": "www-artist"},
        "spec": {"type": "service"},
    },
]

ResponseClosure = Callable[[List[Entity]], respx.Router]


@pytest.fixture()
def with_reponse_data(respx_mock: respx.Router) -> ResponseClosure:
    def inner(data: List[Entity]):
        response = httpx.Response(200, json=data)
        respx_mock.get(f"{mock_base_url}/entities").mock(return_value=response)
        return respx_mock

    return inner


@pytest.fixture()
def default_router(respx_mock: respx.Router):
    response = httpx.Response(200, json=entities)
    yield respx_mock.get(f"{mock_base_url}/entities").mock(return_value=response)


@pytest.mark.asyncio(scope="class")
class TestGetEntities:
    @staticmethod
    @pytest.fixture(autouse=True)
    def _setup(default_router: respx.Router):
        yield

    @staticmethod
    async def test_it_should_fetch_from_the_correct_endpoint(
        httpx_catalog_client: AsyncCatalogApi,
    ):
        response = await httpx_catalog_client.get_entities()
        assert response.items == entities

    @staticmethod
    async def test_it_should_build_multiple_entity_search_params_properly(
        httpx_catalog_client: AsyncCatalogApi,
        default_router: respx.Router,
    ):
        query_filter = [
            {"a": "1"},
            {"b": ["2", "3"]},
            {"c": "="},
            {"d": CATALOG_FILTER_EXISTS},
        ]
        request = GetEntitiesRequest(entity_filter=query_filter)
        await httpx_catalog_client.get_entities(request)
        actual = default_router.calls.last.request.url.params.get_list("filter")
        assert actual == ["a=1", "b=2,b=3", "c==", "d"]

    @staticmethod
    async def test_it_builds_search_filters_properly_even_with_URL_unsafe_values(
        httpx_catalog_client: AsyncCatalogApi, default_router: respx.Router
    ):
        query_filter = [
            {
                "!@#$%": "t?i=1&a:2",
                "^&*(){}[]": ["t%^url*encoded2", "url"],
            }
        ]
        await httpx_catalog_client.get_entities(GetEntitiesRequest(entity_filter=query_filter))
        actual = default_router.calls.last.request.url.params.get_list("filter")
        assert actual == ["!@#$%=t?i=1&a:2,^&*(){}[]=t%^url*encoded2,^&*(){}[]=url"]

    @staticmethod
    async def test_it_builds_entity_field_selector_properly(
        httpx_catalog_client: AsyncCatalogApi, default_router: respx.Router
    ):
        request = GetEntitiesRequest(fields=["metadata.name", "spec.type"])
        await httpx_catalog_client.get_entities(request)
        actual = default_router.calls.last.request.url.params.get_list("fields")
        assert actual == request.fields

    @staticmethod
    async def test_it_handles_field_filterd_entities(
        httpx_catalog_client: AsyncCatalogApi, with_reponse_data: ResponseClosure
    ):
        with_reponse_data([{"apiVersion": "1"}, {"apiVersion": "2"}])
        request = GetEntitiesRequest(fields=["apiVersion"])
        response = await httpx_catalog_client.get_entities(request)
        assert response.items == [{"apiVersion": "1"}, {"apiVersion": "2"}]


@pytest.mark.asyncio(scope="class")
class TestGetEntityByRef:
    @staticmethod
    @pytest.fixture(autouse=True)
    def _setup(respx_mock: respx.Router):
        respx_mock.get(f"{mock_base_url}/entities/by-name/component/default/www-artist").mock(
            return_value=httpx.Response(200, json=entities[1])
        )
        respx_mock.get(f"{mock_base_url}/entities/by-name/component/default/non-existent").mock(
            return_value=httpx.Response(404)
        )

    @staticmethod
    async def test_it_should_fetch_from_the_correct_endpoint(
        httpx_catalog_client: AsyncCatalogApi,
    ):
        response = await httpx_catalog_client.get_entity_by_ref("component:www-artist")
        assert response == entities[1]

    @staticmethod
    async def test_it_should_fetch_from_the_correct_endpoint_with_compound_entity_ref(
        httpx_catalog_client: AsyncCatalogApi,
    ):
        response = await httpx_catalog_client.get_entity_by_ref(
            CompoundEntityRef(kind="component", namespace="default", name="www-artist")
        )
        assert response == entities[1]

    @staticmethod
    async def test_it_should_return_none_if_entity_not_found(
        httpx_catalog_client: AsyncCatalogApi,
    ):
        response = await httpx_catalog_client.get_entity_by_ref("component:default/non-existent")
        assert response is None

    @staticmethod
    async def test_it_should_return_none_if_entity_not_found_with_compound_entity_ref(
        httpx_catalog_client: AsyncCatalogApi,
    ):
        response = await httpx_catalog_client.get_entity_by_ref(
            CompoundEntityRef(kind="component", name="non-existent")
        )
        assert response is None
