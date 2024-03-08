from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict


class EntityTargetRef(TypedDict):
    kind: str
    namespace: str
    name: str


class EntityRelation(TypedDict):
    type: str
    targetRef: str
    target: EntityTargetRef


class EntityLink(TypedDict):
    url: str
    title: NotRequired[str]
    icon: NotRequired[str]
    type: NotRequired[str]


class EntityMeta(TypedDict):
    uid: NotRequired[str]
    etag: NotRequired[str]
    name: str
    namespace: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    labels: NotRequired[Dict[str, str]]
    annotations: NotRequired[Dict[str, str]]
    tags: NotRequired[List[str]]
    links: NotRequired[List[EntityLink]]


class Entity(TypedDict):
    apiVersion: str
    kind: str
    metadata: EntityMeta
    spec: NotRequired[Dict[str, Any]]
    relations: NotRequired[List[EntityRelation]]
