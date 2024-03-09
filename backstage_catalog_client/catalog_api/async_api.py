from __future__ import annotations

from typing import Protocol

from typing_extensions import Unpack

from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import (
    AddLocationRequest,
    AddLocationResponse,
    CatalogRequestOptions,
    EntityRef,
    GetEntitiesByRefsOptions,
    GetEntitiesByRefsResponse,
    GetEntitiesRequest,
    GetEntitiesResponse,
    GetEntityAncestorsRequest,
    GetEntityAncestorsResponse,
    GetEntityFacetsRequest,
    GetEntityFacetsResponse,
    Location,
    QueryEntitiesKwargs,
    QueryEntitiesResponse,
    ValidateEntityResponse,
)


class AsyncCatalogApi(Protocol):
    async def get_entities(
        self,
        **kwargs: Unpack[GetEntitiesRequest],
    ) -> GetEntitiesResponse:
        """
        Gets entities from your backstage instance.

        Args:
            kwargs: The request object for getting entities. Defaults to None.
            options: The options for the catalog request. Defaults to None.

        Returns:
            The response object containing the entities.
        """
        ...

    async def get_entities_by_refs(
        self,
        refs: list[str | EntityRef],
        **opts: Unpack[GetEntitiesByRefsOptions],
    ) -> GetEntitiesByRefsResponse:
        """
        Gets a batch of entities, by their entity refs.
        The output list of entities is of the same size and in the same order as
        the requested list of entity refs. Entries that are not found are returned
        as null.
        """
        ...

    async def get_entity_by_ref(
        self,
        ref: str | EntityRef,
        **options: Unpack[CatalogRequestOptions],
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

    async def get_location_by_entity(
        self,
        ref: str | EntityRef,
        **opts: Unpack[CatalogRequestOptions],
    ) -> Location | None: ...

    async def query_entities(
        self,
        **kwargs: Unpack[QueryEntitiesKwargs],
    ) -> QueryEntitiesResponse: ...


class todo_catalog_api(Protocol):
    async def get_entity_ancestors(
        self,
        request: GetEntityAncestorsRequest,
        **options: Unpack[CatalogRequestOptions],
    ) -> GetEntityAncestorsResponse: ...

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

    async def validate_entity(
        self, entity: Entity, locationRef: str, options: CatalogRequestOptions | None
    ) -> ValidateEntityResponse: ...
