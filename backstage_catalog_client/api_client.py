from typing import Protocol

from backstage_catalog_client.entity.entity import Entity
from backstage_catalog_client.models import (
    AddLocationRequest,
    AddLocationResponse,
    CatalogRequestOptions,
    CompoundEntityRef,
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

# Random UUID to ensure no collisions
CATALOG_FILTER_EXISTS = "CATALOG_FILTER_EXISTS_0e15b590c0b343a2bae3e787e84c2111"
CATALOG_API_BASE_PATH = "/api/catalog"


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
