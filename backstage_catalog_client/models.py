from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, Sequence, Union

from typing_extensions import TypedDict

from backstage_catalog_client.entity import Entity

EntityFilterItem = Mapping[str, Union[str, Sequence[str]]]

EntityFilterQuery = Sequence[EntityFilterItem]
"""
A key-value based filter expression for entities.

Each key of a record is a dot-separated path into the entity structure, e.g.
`metadata.name`.
The values are literal values to match against. As a value you can also pass
in the symbol `CATALOG_FILTER_EXISTS` (exported from this package), which
means that you assert on the existence of that key, no matter what its value
is.
All matching of keys and values is case insensitive.
If multiple filter sets are given as an array, then there is effectively an
OR between each filter set.
Within one filter set, there is effectively an AND between the various keys.
Within one key, if there are more than one value, then there is effectively
an OR between them.
Example: For an input of
```
[
  { kind: ['API', 'Component'] },
  { 'metadata.name': 'a', 'metadata.namespace': 'b' }
]
```

This effectively means
```
(kind = EITHER 'API' OR 'Component')
OR
(metadata.name = 'a' AND metadata.namespace = 'b' )
```
"""


class CatalogRequestOptions(TypedDict, total=False):
    """Options you can pass into a catalog request for additional information."""

    token: str
    """an Authentication token for authenticated requests"""


class SerializedError(TypedDict):
    pass


class EntityOrderQuery(TypedDict):
    field: str
    order: Literal["asc", "desc"]


class GetEntitiesRequest(CatalogRequestOptions, TypedDict, total=False):
    entity_filter: EntityFilterQuery
    """If given, only entities matching this filter will be returned."""
    fields: Sequence[str]
    """If given, return only the parts of each entity that match the field declarations."""
    order: EntityOrderQuery | Sequence[EntityOrderQuery]
    """If given, order the result set by those directives."""
    offset: int
    """If given, skips over the first N items in the result set."""
    limit: int
    """If given, returns at most N items from the result set."""
    after: str
    """If given, skips over all items before that cursor as returned by a previous request."""


@dataclass
class GetEntitiesResponse:
    """the repsonse type for getEntities"""

    items: list[Entity]


class GetEntitiesByRefsOptions(CatalogRequestOptions, TypedDict, total=False):
    fields: list[str]
    entity_filter: EntityFilterQuery


@dataclass
class GetEntitiesByRefsResponse:
    items: list[Entity | None]


@dataclass
class GetEntityAncestorsRequest:
    pass


@dataclass
class GetEntityAncestorsResponse:
    pass


@dataclass
class EntityRef:
    """all parts of a compound entity reference."""

    kind: str
    name: str
    namespace: str = "default"

    def __str__(self) -> str:
        return f"{self.kind}:{self.namespace}/{self.name}"


@dataclass
class GetEntityFacetsRequest:
    pass


@dataclass
class GetEntityFacetsResponse:
    pass


@dataclass
class Location:
    location_id: str
    location_type: str
    target: str


@dataclass
class AddLocationRequest:
    location_type: str | None
    target: str
    dryRun: bool | None


@dataclass
class AddLocationResponse:
    location: Location
    entities: list[Entity]
    exists: bool | None


@dataclass
class ValidateEntityResponse:
    valid: bool
    errors: list[SerializedError]


class FullTextFilter(TypedDict, total=False):
    search_term: str
    """search term"""
    search_fields: list[str]


class QueryEntitiesKwargs(FullTextFilter, CatalogRequestOptions, TypedDict, total=False):
    cursor: str
    """cursor for the next batch of entities"""
    entity_filter: EntityFilterQuery
    """If given, only entities matching this filter will be returned."""
    fields: list[str]
    """If given, return only the parts of each entity that match the field declarations."""
    limit: int
    """controls the number of items per page;  default is 20"""
    order_fields: list[EntityOrderQuery] | EntityOrderQuery
    """If given, order the result set by those directives."""


@dataclass
class PageInfo:
    nextCursor: str | None = None
    """The cursor for the next batch of entities"""
    prevCursor: str | None = None
    """The cursor for the previous batch of entities"""


@dataclass
class QueryEntitiesResponse:
    items: list[Entity]
    """The list of entities for the current request"""
    total_items: int
    """"The number of entities among all the requests"""
    page_info: PageInfo
