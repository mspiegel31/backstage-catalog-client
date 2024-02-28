from typing import Any, Optional

from typing_extensions import TypedDict


class RawEntityRelation(TypedDict, total=False):
    type: str
    targetRef: str


class RawEntityLink(TypedDict, total=False):
    url: str
    title: Optional[str]
    icon: Optional[str]
    type: Optional[str]


class RawEntityMeta(TypedDict, total=False):
    name: str
    uid: Optional[str]
    etag: Optional[str]
    namespace: Optional[str]
    title: Optional[str]
    description: Optional[str]
    labels: Optional[dict[str, str]]
    annotations: Optional[dict[str, str]]
    tags: Optional[list[str]]
    links: Optional[list[RawEntityLink]]


class RawEntity(TypedDict, total=False):
    apiVersion: str
    kind: str
    metadata: RawEntityMeta
    spec: Optional[dict[str, Any]]
    relations: Optional[list[RawEntityRelation]]
