from __future__ import annotations

from typing import Protocol

from typing_extensions import Unpack

from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    EntityRef,
    GetEntitiesByRefsOptions,
    GetEntitiesByRefsResponse,
    GetEntitiesRequest,
    GetEntitiesResponse,
    Location,
    QueryEntitiesKwargs,
    QueryEntitiesResponse,
)


class SyncCatalogApi(Protocol):
    async def get_entities(
        self,
        **kwargs: Unpack[GetEntitiesRequest],
    ) -> GetEntitiesResponse:
        """
        Gets entities from your backstage instance.

        Args:
            kwargs: The request object for getting entities. Defaults to None.

        Returns:
            The response object containing the entities.
        """
        ...

    async def query_entities(
        self,
        **kwargs: Unpack[QueryEntitiesKwargs],
    ) -> QueryEntitiesResponse:
        """
        Gets paginated entities from the catalog.'

        Args:
            **kwargs: keyword arguments, represented as a dict.

        Returns:
            The response object containing the entities.

        Examples:
            ```python
            response = await catalog_client.query_entities(
                search_term='A',
                entity_filter=[{"kind": "User"}],
                order_fields={'field': 'metadata.name', 'order': 'asc'},
                limit=20,
            )
            ```
            this will match all entities of type group having a name starting
            with 'A', ordered by name ascending.
            The response will contain a maximum of 20 entities. In case
            more than 20 entities exist, the response will contain a nextCursor
            property that can be used to fetch the next batch of entities.

            ```python
            second_batch_response = await catalog_client
                .query_entities(cursor=response.page_info.nextCursor)
            ```
            second_batch_response will contain the next batch of (maximum) 20 entities,
            together with a prevCursor property, useful to fetch the previous batch.

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
            ref: The reference to the entity to fetch.
            options: The options for the catalog request. Defaults to None.

        Returns:
            The entity if found, otherwise None.
        """

        ...

    async def get_location_by_entity(
        self,
        ref: str | EntityRef,
        **opts: Unpack[CatalogRequestOptions],
    ) -> Location | None:
        """
        Gets a location associated with an entity.

        Args:
            ref: The reference to the entity to fetch.
            **opts: The options for the catalog request.

        Returns:
            the location if found, otherwise None.
        """
        ...
