from __future__ import annotations

from typing import Protocol

from backstage_catalog_client.entity import Entity
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


class AsyncCatalogApi(Protocol):
    async def get_entities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        """
        Gets entities from your backstage instance.

        Args:
            request: The request object for getting entities. Defaults to None.
            options: The options for the catalog request. Defaults to None.

        Returns:
            The response object containing the entities.
        """
        ...

    async def get_entity_by_ref(
        self,
        request: str | CompoundEntityRef,
        options: CatalogRequestOptions | None = None,
    ) -> Entity | None:
        """
        Gets a single entity from your backstage instance by reference (kind, namespace, name).

        Args:
            request: The reference to the entity to fetch.
            options: The options for the catalog request. Defaults to None.

        Returns:
            The entity if found, otherwise None.
        """

        ...


class todo_catalog_api(Protocol):
    async def query_entities(
        self,
        request: QueryEntitiesRequest | None,
        options: CatalogRequestOptions | None,
    ) -> QueryEntitiesResponse: ...

    async def get_entities_by_refs(
        self,
        request: GetEntitiesByRefsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntitiesByRefsResponse: ...

    async def get_entity_ancestors(
        self,
        request: GetEntityAncestorsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntityAncestorsResponse: ...

    async def get_entity_by_ref(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> Entity | None: ...

    async def remove_entity_by_uid(self, uid: str, options: CatalogRequestOptions | None) -> None: ...

    async def refresh_entity(self, entityRef: str, options: CatalogRequestOptions | None) -> None: ...

    async def get_entity_facets(
        self, request: GetEntityFacetsRequest, options: CatalogRequestOptions | None
    ) -> GetEntityFacetsResponse: ...

    async def get_location_by_id(self, location_id: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def get_location_by_ref(self, locationRef: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def add_location(
        self, location: AddLocationRequest, options: CatalogRequestOptions | None
    ) -> AddLocationResponse: ...

    async def remove_location_by_id(self, location_id: str, options: CatalogRequestOptions | None) -> None: ...

    async def get_location_by_entity(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> Location | None: ...

    async def validate_entity(
        self, entity: Entity, locationRef: str, options: CatalogRequestOptions | None
    ) -> ValidateEntityResponse: ...
