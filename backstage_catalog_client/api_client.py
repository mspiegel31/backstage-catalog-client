from typing import Protocol

from httpx import AsyncClient

from backstage_catalog_client.entity.entity import Entity
from backstage_catalog_client.models import (
    AddLocationRequest,
    AddLocationResponse,
    CatalogRequestOptions,
    CompoundEntityRef,
    EntityFilterQuery,
    GetEntitiesByRefsRequest,
    GetEntitiesByRefsResponse,
    GetEntitiesRequest,
    GetEntitiesResponse,
    GetEntityAncestorsRequest,
    GetEntityAncestorsResponse,
    GetEntityFacetsRequest,
    GetEntityFacetsResponse,
    Location,
    QueryEntitiesRequest,
    QueryEntitiesResponse,
    ValidateEntityResponse,
)
from backstage_catalog_client.utils import to_dict


class CatalogApi(Protocol):
    async def getEntities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        """
        docs go here
        """
        ...


class TODOCatalogApi(Protocol):
    async def getEntitiesByRefs(
        self,
        request: GetEntitiesByRefsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntitiesByRefsResponse: ...

    async def queryEntities(
        self,
        request: QueryEntitiesRequest | None,
        options: CatalogRequestOptions | None,
    ) -> QueryEntitiesResponse: ...

    async def getEntityAncestors(
        self,
        request: GetEntityAncestorsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntityAncestorsResponse: ...

    async def getEntityByRef(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> Entity | None: ...

    async def removeEntityByUid(self, uid: str, options: CatalogRequestOptions | None) -> None: ...

    async def refreshEntity(self, entityRef: str, options: CatalogRequestOptions | None) -> None: ...

    async def getEntityFacets(
        self, request: GetEntityFacetsRequest, options: CatalogRequestOptions | None
    ) -> GetEntityFacetsResponse: ...

    async def getLocationById(self, id: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def getLocationByRef(self, locationRef: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def addLocation(
        self, location: AddLocationRequest, options: CatalogRequestOptions | None
    ) -> AddLocationResponse: ...

    async def removeLocationById(self, id: str, options: CatalogRequestOptions | None) -> None: ...

    async def getLocationByEntity(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> Location | None: ...

    async def validateEntity(
        self, entity: Entity, locationRef: str, options: CatalogRequestOptions | None
    ) -> ValidateEntityResponse: ...


# Random UUID to ensure no collisions
CATALOG_FILTER_EXISTS = "CATALOG_FILTER_EXISTS_0e15b590c0b343a2bae3e787e84c2111"


class DefaultCatalogApi(CatalogApi):
    client: AsyncClient

    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    async def getEntities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ):
        if request is None:
            request = GetEntitiesRequest()
        if options is None:
            options = CatalogRequestOptions()

        dict_request = to_dict(request)
        if request.filter:
            dict_request["filter"] = self.get_filter_value(request.filter)

        response = await self.client.get("/entities", params=dict_request)
        if response.status_code != 200:
            raise Exception(response.text)

        return GetEntitiesResponse(items=response.json())

    def get_filter_value(self, filter: EntityFilterQuery = []):
        prepared_filters: list[str] = []
        # filter param can occur multiple times, for example
        # /api/catalog/entities?filter=metadata.name=wayback-search,kind=component&filter=metadata.name=www-artist,kind=component'
        # the "outer array" defined by `filter` occurrences corresponds to "anyOf" filters
        # the "inner array" defined within a `filter` param corresponds to "allOf" filters

        for filter_item in filter:
            filter_parts: list[str] = []
            for key, value in filter_item.items():
                v_iter = value if isinstance(value, list) else [value]
                for v in v_iter:
                    if v == CATALOG_FILTER_EXISTS:
                        filter_parts.append(key)
                    elif isinstance(v, str):
                        filter_parts.append(f"{key}={v}")
            if filter_parts:
                prepared_filters.append(",".join(filter_parts))
        return prepared_filters
