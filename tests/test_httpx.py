import json
from typing import Callable, List

import httpx
import pytest
import respx
from conftest import mock_base_url

from backstage_catalog_client.catalog_api.async_api import AsyncCatalogApi
from backstage_catalog_client.catalog_api.util import CATALOG_FILTER_EXISTS
from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import EntityRef, PageInfo, QueryEntitiesKwargs, QueryEntitiesResponse

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
    async def test_it_should_send_a_token(
        httpx_catalog_client: AsyncCatalogApi,
        default_router: respx.Router,
    ):
        await httpx_catalog_client.get_entities(token="my-token")  # noqa: S106
        assert default_router.calls.last.request.headers.get("Authorization") == "Bearer my-token"

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
        await httpx_catalog_client.get_entities(entity_filter=query_filter)
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
        await httpx_catalog_client.get_entities(entity_filter=query_filter)
        actual = default_router.calls.last.request.url.params.get_list("filter")
        assert actual == ["!@#$%=t?i=1&a:2,^&*(){}[]=t%^url*encoded2,^&*(){}[]=url"]

    @staticmethod
    async def test_it_builds_entity_field_selector_properly(
        httpx_catalog_client: AsyncCatalogApi, default_router: respx.Router
    ):
        await httpx_catalog_client.get_entities(fields=["metadata.name", "spec.type"])
        actual = default_router.calls.last.request.url.params.get_list("fields")
        assert actual == ["metadata.name", "spec.type"]

    @staticmethod
    async def test_it_handles_field_filterd_entities(
        httpx_catalog_client: AsyncCatalogApi, with_reponse_data: ResponseClosure
    ):
        with_reponse_data([{"apiVersion": "1"}, {"apiVersion": "2"}])
        response = await httpx_catalog_client.get_entities(fields=["apiVersion"])
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
            EntityRef(kind="component", namespace="default", name="www-artist")
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
        response = await httpx_catalog_client.get_entity_by_ref(EntityRef(kind="component", name="non-existent"))
        assert response is None


@pytest.mark.asyncio(scope="class")
class TestGetEntitiesByRefs:
    @staticmethod
    @pytest.fixture(autouse=True)
    def _setup(respx_mock: respx.Router):
        respx_mock.post(f"{mock_base_url}/entities/by-refs/").mock(
            return_value=httpx.Response(200, json=[entities[1], None])
        )

    @staticmethod
    async def test_mixed_response(httpx_catalog_client: AsyncCatalogApi, respx_mock: respx.Router):
        resp = await httpx_catalog_client.get_entities_by_refs(
            ["component:www-artist", "component:wayback-search"],
            fields=["metadata.name"],
            entity_filter=[{"kind": ["component", "group"]}],
        )

        assert resp.items == [entities[1], None]
        expected_body = {
            "entityRefs": ["component:default/www-artist", "component:default/wayback-search"],
            "fields": ["metadata.name"],
        }
        assert json.loads(respx_mock.calls.last.request.content) == expected_body
        assert respx.calls.last.request.url.params.get_list("filter") == ["kind=component,kind=group"]


@pytest.mark.asyncio(scope="class")
class TestQueryEntities:
    @pytest.fixture(autouse=True)
    def setup(self, respx_mock: respx.Router, httpx_catalog_client: AsyncCatalogApi):
        self.respx_mock = respx_mock
        self.client = httpx_catalog_client
        self.default_response = {
            "items": entities,
            "totalItems": 10,
            "pageInfo": {
                "prevCursor": "prev",
                "nextCursor": "next",
            },
        }

        self.respx_mock.get(f"{mock_base_url}/entities/by-query").mock(
            return_value=httpx.Response(200, json=self.default_response)
        )

    def _to_response(self, payload: dict):
        return QueryEntitiesResponse(
            items=payload["items"],
            total_items=payload["totalItems"],
            page_info=PageInfo(**payload.get("pageInfo", {})),
        )

    async def test_it_should_fetch_from_the_correct_endpoint(self):
        response = await self.client.query_entities()
        assert response == self._to_response(self.default_response)

    async def test_it_handles_paginated_requests(self):
        kwargs: QueryEntitiesKwargs = {
            "fields": ["a", "b"],
            "limit": 100,
            "search_term": "search",
            "order_fields": [{"field": "metadata.name", "order": "asc"}],
            "cursor": "cursor",
        }
        await self.client.query_entities(**kwargs)
        assert (
            self.respx_mock.calls.last.request.url.params.items()
            == {"fields": "a,b", "limit": "100", "cursor": "cursor"}.items()
        )


@pytest.mark.asyncio(scope="class")
class TestGetLocationByEntity:
    pass
