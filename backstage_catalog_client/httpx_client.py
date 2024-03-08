from __future__ import annotations

import typing
from urllib.parse import urljoin

from httpx import AsyncClient

from backstage_catalog_client.catalog_api.async_api import AsyncCatalogApi
from backstage_catalog_client.catalog_api.util import CATALOG_API_BASE_PATH, get_filter_value
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    CompoundEntityRef,
    GetEntitiesRequest,
    GetEntitiesResponse,
)
from backstage_catalog_client.raw_entity import RawEntity
from backstage_catalog_client.utils import parse_ref_string, to_dict


class HttpxClient(AsyncCatalogApi):
    def __init__(self, base_url: str, client: AsyncClient | None = None) -> None:
        self.catalog_api_path = urljoin(base_url, CATALOG_API_BASE_PATH)
        self.base_url = base_url
        if client is None:
            self.client = AsyncClient()
        else:
            self.client = client

    async def get_entities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        if request is None:
            request = GetEntitiesRequest()
        if options is None:
            options = CatalogRequestOptions()

        dict_request = to_dict(request)
        if request.entity_filter:
            del dict_request["entity_filter"]
            dict_request["filter"] = get_filter_value(request.entity_filter)

        response = await self.client.get(f"{self.catalog_api_path}/entities", params=dict_request)
        response.raise_for_status()

        return GetEntitiesResponse(items=response.json())

    async def get_entity_by_ref(
        self, request: str | CompoundEntityRef, options: CatalogRequestOptions | None = None
    ) -> RawEntity | None:
        if isinstance(request, str):
            request = parse_ref_string(request)

        uri = f"{self.catalog_api_path}/entities/by-name/{request.kind}/{request.namespace}/{request.name}"
        response = await self.client.get(uri)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return typing.cast(RawEntity, response.json())
