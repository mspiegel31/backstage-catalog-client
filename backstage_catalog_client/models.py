from typing import Dict, List, Mapping, Sequence

from pydantic import BaseModel

from backstage_catalog_client.entities import Entity

# check out key ordering issues in pydantic here:
# https://github.com/tiangolo/fastapi/discussions/7943

EntityFilterQuery = Mapping[str, str | Sequence[str]] | Sequence[Mapping[str, str | Sequence[str]]]


class EntityOrderQuery(BaseModel):
    # Implementation details of EntityOrderQuery
    pass


class SerializedError(BaseModel):
    # Implementation details of SerializedError
    pass


class GetEntitiesRequest(BaseModel):
    # Implementation details of GetEntitiesRequest
    filter: EntityFilterQuery | None = None
    fields: bool | None = None
    order: bool | None = None
    offset: int | None = None
    limit: int | None = None
    after: str | None = None


class GetEntitiesResponse(BaseModel):
    # Implementation details of GetEntitiesResponse
    items: list[Entity]


class GetEntitiesByRefsRequest(BaseModel):
    # Implementation details of GetEntitiesByRefsRequest
    pass


class GetEntitiesByRefsResponse(BaseModel):
    # Implementation details of GetEntitiesByRefsResponse
    pass


class GetEntityAncestorsRequest(BaseModel):
    # Implementation details of GetEntityAncestorsRequest
    pass


class GetEntityAncestorsResponse(BaseModel):
    # Implementation details of GetEntityAncestorsResponse
    pass


class CompoundEntityRef(BaseModel):
    # Implementation details of CompoundEntityRef
    pass


class GetEntityFacetsRequest(BaseModel):
    # Implementation details of GetEntityFacetsRequest
    pass


class GetEntityFacetsResponse(BaseModel):
    # Implementation details of GetEntityFacetsResponse
    pass


class CatalogRequestOptions(BaseModel):
    token: str | None


class Location(BaseModel):
    id: str
    type: str
    target: str


class AddLocationRequest(BaseModel):
    type: str | None
    target: str
    dryRun: bool | None


class AddLocationResponse(BaseModel):
    location: Location
    entities: List[Entity]
    exists: bool | None


class ValidateEntityResponse(BaseModel):
    valid: bool
    errors: List[SerializedError]


class QueryEntitiesInitialRequest(BaseModel):
    fields: List[str] | None
    limit: int | None
    filter: EntityFilterQuery | None
    orderFields: EntityOrderQuery | None
    fullTextFilter: Dict[str, str | List[str]] | None


class QueryEntitiesCursorRequest(BaseModel):
    fields: List[str] | None
    limit: int | None
    cursor: str


class QueryEntitiesRequest(BaseModel):
    filter: QueryEntitiesInitialRequest | QueryEntitiesCursorRequest | None


class QueryEntitiesResponse(BaseModel):
    items: List[Entity]
    totalItems: int
    pageInfo: Dict[str, str | None]
