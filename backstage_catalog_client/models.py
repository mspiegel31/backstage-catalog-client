from dataclasses import dataclass
from typing import Dict, List, Literal, Mapping, Optional, Sequence, Union

from backstage_catalog_client.entity.entity import Entity
from backstage_catalog_client.raw_entity import RawEntity

# check out key ordering issues in pydantic here:
# https://github.com/tiangolo/fastapi/discussions/7943
EntityFilterItem = Mapping[str, str | Sequence[str]]
EntityFilterQuery = Sequence[EntityFilterItem]


@dataclass
class SerializedError:
    pass


@dataclass
class EntityOrderQuery:
    field: str
    order: Literal["asc", "desc"]


@dataclass
class GetEntitiesRequest:
    filter: Optional[EntityFilterQuery] = None
    fields: Optional[List[str]] = None
    order: Optional[Union[EntityOrderQuery, Sequence[EntityOrderQuery]]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    after: Optional[str] = None


@dataclass
class GetEntitiesResponse:
    items: List[RawEntity]


@dataclass
class GetEntitiesByRefsRequest:
    pass


@dataclass
class GetEntitiesByRefsResponse:
    pass


@dataclass
class GetEntityAncestorsRequest:
    pass


@dataclass
class GetEntityAncestorsResponse:
    pass


@dataclass
class CompoundEntityRef:
    pass


@dataclass
class GetEntityFacetsRequest:
    pass


@dataclass
class GetEntityFacetsResponse:
    pass


@dataclass
class CatalogRequestOptions:
    token: Optional[str] = None


@dataclass
class Location:
    id: str
    type: str
    target: str


@dataclass
class AddLocationRequest:
    type: Optional[str]
    target: str
    dryRun: Optional[bool]


@dataclass
class AddLocationResponse:
    location: Location
    entities: List[Entity]
    exists: Optional[bool]


@dataclass
class ValidateEntityResponse:
    valid: bool
    errors: List[SerializedError]


@dataclass
class QueryEntitiesInitialRequest:
    fields: Optional[List[str]]
    limit: Optional[int]
    filter: Optional[EntityFilterQuery]
    orderFields: Optional[EntityOrderQuery]
    fullTextFilter: Optional[Dict[str, Union[str, List[str]]]]


@dataclass
class QueryEntitiesCursorRequest:
    fields: Optional[List[str]]
    limit: Optional[int]
    cursor: str


@dataclass
class QueryEntitiesRequest:
    filter: Optional[Union[QueryEntitiesInitialRequest, QueryEntitiesCursorRequest]]


@dataclass
class QueryEntitiesResponse:
    items: List[Entity]
    totalItems: int
    pageInfo: Dict[str, Optional[str]]
