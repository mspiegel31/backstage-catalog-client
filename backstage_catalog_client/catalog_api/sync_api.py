from __future__ import annotations

from typing import Protocol

from backstage_catalog_client.entity import Entity
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    EntityRef,
    GetEntitiesRequest,
    GetEntitiesResponse,
)


class SyncCatalogApi(Protocol):
    def get_entities(
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

    def get_entity_by_ref(
        self,
        request: str | EntityRef,
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
