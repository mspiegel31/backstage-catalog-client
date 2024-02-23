from json_types import JsonObject
from pydantic import BaseModel


class EntityLink(BaseModel):
    url: str
    title: str | None = None
    icon: str | None = None
    type: str | None = None


class EntityRelation(BaseModel):
    type: str
    targetRef: str


# TODO: inherit/extend from JsonObject
class EntityMeta(BaseModel):
    name: str
    uid: str | None = None
    etag: str | None = None
    namespace: str | None = None
    title: str | None = None
    description: str | None = None
    labels: dict[str, str] | None = None
    annotations: dict[str, str] | None = None
    tags: list[str] | None = None
    links: list[EntityLink] | None = None


class Entity(BaseModel):
    apiVersion: str
    kind: str
    metadata: EntityMeta
    spec: JsonObject | None = None
    relations: list[EntityRelation] | None = None
