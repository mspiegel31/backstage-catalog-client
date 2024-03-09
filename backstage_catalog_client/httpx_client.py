from __future__ import annotations

from typing import Generator, TypedDict, cast

from httpx import URL, AsyncClient, Auth, Request
from httpx._models import Response
from typing_extensions import Unpack
from uritemplate import URITemplate

from backstage_catalog_client.catalog_api.async_api import AsyncCatalogApi
from backstage_catalog_client.catalog_api.util import CATALOG_API_BASE_PATH, encode_order, get_filter_value
from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    EntityRef,
    GetEntitiesByRefsOptions,
    GetEntitiesByRefsResponse,
    GetEntitiesRequest,
    GetEntitiesResponse,
    Location,
    PageInfo,
    QueryEntitiesKwargs,
    QueryEntitiesResponse,
)
from backstage_catalog_client.utils import parse_ref_string


class TokenAuth(Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    @classmethod
    def from_options(cls, opts: CatalogRequestOptions) -> TokenAuth | None:
        token = opts.pop("token", None)
        if token:
            return cls(token)
        return None

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class QueryEntitiesParams(TypedDict, total=False):
    fields: list[str]
    limit: int
    orderField: list[str]
    cursor: str
    filter: list[str]
    fullTextFilterTerm: str
    fullTextFilterFields: list[str]


class HttpxClient(AsyncCatalogApi):
    def __init__(self, base_url: str | None = None, client: AsyncClient | None = None) -> None:
        # TODO: Usage docs on stand-alone instantiation vs using with httpx client
        # Call out that direct instantiation is provided for use in scripts etc.
        # if client is passed, base_url is ignored
        if base_url is None and client is None:
            raise ValueError("Either base_url or client must be provided")

        if client is None:
            self._own_client = True
            self.client = AsyncClient()
            self.base_url = URL(cast(str, base_url))
        else:
            self.client = client
            self.base_url = client.base_url

        self.catalog_api_path = self.base_url.join(CATALOG_API_BASE_PATH)

    async def __aenter__(self):  # type: ignore[no-untyped-def]
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):  # type: ignore[no-untyped-def]
        await self.aclose()

    async def aclose(self) -> None:
        """closes the internally-constructed HTTPX client.  If a client was passed in the constructor, this method does nothing."""
        if self._own_client:
            await self.client.aclose()

    async def get_entities(
        self,
        **opts: Unpack[GetEntitiesRequest],
    ) -> GetEntitiesResponse:
        params, auth = self._prepare_request(opts)

        response = await self.client.get(f"{self.catalog_api_path}/entities", params=params, auth=auth)  # type: ignore[arg-type]
        response.raise_for_status()

        return GetEntitiesResponse(items=response.json())

    async def query_entities(
        self,
        **kwargs: Unpack[QueryEntitiesKwargs],
    ) -> QueryEntitiesResponse:
        auth = TokenAuth.from_options(kwargs)
        params: QueryEntitiesParams = {}
        if "cursor" not in kwargs:
            if "entity_filter" in kwargs:
                params["filter"] = get_filter_value(kwargs["entity_filter"])
            if "search_term" in kwargs:
                params["fullTextFilterTerm"] = kwargs["search_term"].strip()
            if "search_fields" in kwargs:
                params["fullTextFilterFields"] = kwargs["search_fields"]
            if "order_fields" in kwargs:
                params["orderField"] = encode_order(kwargs["order_fields"])
            if "fields" in kwargs:
                params["fields"] = kwargs["fields"]
            if "limit" in kwargs:
                params["limit"] = kwargs["limit"]
        else:
            params["cursor"] = kwargs["cursor"]
            if "limit" in kwargs:
                params["limit"] = kwargs["limit"]
            if "fields" in kwargs:
                params["fields"] = kwargs["fields"]
        template = URITemplate(
            "/entities/by-query{?fields,limit,orderField*,cursor,filter*,fullTextFilterTerm,fullTextFilterFields}"
        )
        uri = template.expand(params)  # type: ignore[arg-type]
        response = await self.client.get(f"{self.catalog_api_path}{uri}", auth=auth)
        response.raise_for_status()
        payload = response.json()
        return QueryEntitiesResponse(
            items=payload["items"],
            total_items=payload["totalItems"],
            page_info=PageInfo(**payload.get("pageInfo", {})),
        )

    async def get_entities_by_refs(
        self,
        refs: list[str | EntityRef],
        **opts: Unpack[GetEntitiesByRefsOptions],
    ) -> GetEntitiesByRefsResponse:
        # avoid network call if there's no refs
        if not refs:
            return GetEntitiesByRefsResponse(items=[])

        parsed_refs = (str(parse_ref_string(ref)) for ref in refs if not isinstance(ref, EntityRef))
        template = URITemplate("/entities/by-refs/{?filter*}")

        if "entity_filter" in opts:
            route = template.expand(filter=get_filter_value(opts["entity_filter"]))
        else:
            route = template.expand()

        data = {"entityRefs": list(parsed_refs)}

        if "fields" in opts:
            data["fields"] = opts["fields"]

        response = await self.client.post(
            f"{self.catalog_api_path}{route}",
            json=data,
            # auth=TokenAuth.from_options(opts),
        )
        response.raise_for_status()

        return GetEntitiesByRefsResponse(items=response.json())

    async def get_entity_by_ref(self, ref: str | EntityRef, **opts: Unpack[CatalogRequestOptions]) -> Entity | None:
        if isinstance(ref, str):
            ref = parse_ref_string(ref)

        route = f"/entities/by-name/{ref.kind}/{ref.namespace}/{ref.name}"
        response = await self.client.get(f"{self.catalog_api_path}{route}", auth=TokenAuth.from_options(opts))
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return cast(Entity, response.json())

    async def get_location_by_entity(
        self, ref: str | EntityRef, **opts: Unpack[CatalogRequestOptions]
    ) -> Location | None:
        if isinstance(ref, str):
            ref = parse_ref_string(ref)
        template = URITemplate("/locations/by-entity/{kind}/{namespace}/{name}")
        route = template.expand(kind=ref.kind, namespace=ref.namespace, name=ref.name)
        response = await self.client.get(f"{self.catalog_api_path}{route}", auth=TokenAuth.from_options(opts))
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return cast(Location, response.json())

    def _prepare_request(self, data: GetEntitiesRequest) -> tuple[dict[str, object], TokenAuth | None]:
        auth = TokenAuth.from_options(data)
        params = self._to_params(data)
        return params, auth

    def _to_params(self, opts: GetEntitiesRequest) -> dict[str, object]:
        transform_keys = {"entity_filter", "order"}
        request = {k: v for k, v in opts.items() if k not in transform_keys}
        if "entity_filter" in opts:
            request["filter"] = get_filter_value(opts["entity_filter"])
        if "order" in opts:
            request["order"] = encode_order(opts["order"])

        return request
