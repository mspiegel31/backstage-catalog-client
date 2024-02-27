from typing import Sequence

from pydantic import BaseModel

from backstage_catalog_client.json_types import JsonObject


class EntityLink(BaseModel):
    url: str
    title: str | None = None
    icon: str | None = None
    type: str | None = None  # noqa: A003


class EntityRelation(BaseModel):
    type: str  # noqa: A003
    targetRef: str


# TODO: inherit/extend from JsonObject
class EntityMeta(BaseModel):
    name: str
    uid: str | None = None
    etag: str | None = None
    namespace: str | None = None
    title: str | None = None
    description: str | None = None
    labels: dict[str, str] | None = {}
    annotations: dict[str, str] = {}
    tags: list[str] = []
    links: list[EntityLink] = []


class Entity(BaseModel):
    apiVersion: str
    kind: str
    metadata: EntityMeta
    spec: JsonObject = {}
    relations: Sequence[EntityRelation] = []
