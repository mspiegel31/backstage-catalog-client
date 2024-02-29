# generated by datamodel-codegen:
#   filename:  EntityMeta
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Tag(RootModel[str]):
    root: str = Field(..., min_length=1)


class Link(BaseModel):
    title: Optional[str] = Field(
        None,
        description="A user friendly display name for the link.",
        examples=["Admin Dashboard"],
        min_length=1,
    )

    url: str = Field(
        ...,
        description="A url in a standard uri format.",
        examples=["https://admin.example-org.com"],
        min_length=1,
    )
    icon: Optional[str] = Field(
        None,
        description="A key representing a visual icon to be displayed in the UI.",
        examples=["dashboard"],
        min_length=1,
    )
    type: Optional[str] = Field(
        None,
        description="An optional value to categorize links into specific groups.",
        examples=["runbook", "documentation", "logs", "dashboard"],
        min_length=1,
    )


class Model(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    uid: Optional[str] = Field(
        None,
        description="A globally unique ID for the entity. This field can not be set by the user at creation time, and the server will reject an attempt to do so. The field will be populated in read operations. The field can (optionally) be specified when performing update or delete operations, but the server is free to reject requests that do so in such a way that it breaks semantics.",
        examples=["e01199ab-08cc-44c2-8e19-5c29ded82521"],
        min_length=1,
    )
    etag: Optional[str] = Field(
        None,
        description="An opaque string that changes for each update operation to any part of the entity, including metadata. This field can not be set by the user at creation time, and the server will reject an attempt to do so. The field will be populated in read operations. The field can (optionally) be specified when performing update or delete operations, and the server will then reject the operation if it does not match the current stored value.",
        examples=["lsndfkjsndfkjnsdfkjnsd=="],
        min_length=1,
    )
    name: str = Field(
        ...,
        description="The name of the entity. Must be unique within the catalog at any given point in time, for any given namespace + kind pair.",
        examples=["metadata-proxy"],
        min_length=1,
    )
    namespace: Optional[str] = Field(
        "default",
        description="The namespace that the entity belongs to.",
        examples=["default", "admin"],
        min_length=1,
    )
    title: Optional[str] = Field(
        None,
        description="A display name of the entity, to be presented in user interfaces instead of the name property, when available.",
        examples=["React SSR Template"],
        min_length=1,
    )
    description: Optional[str] = Field(
        None,
        description="A short (typically relatively few words, on one line) description of the entity.",
    )
    labels: dict[str, str] = Field(
        {},
        description="Key/value pairs of identifying information attached to the entity.",
    )
    annotations: dict[str, str] = Field(
        {},
        description="Key/value pairs of non-identifying auxiliary information attached to the entity.",
    )
    tags: list[Tag] = Field(
        [],
        description="A list of single-valued strings, to for example classify catalog entities in various ways.",
    )
    links: list[Link] = Field(
        [],
        description="A list of external hyperlinks related to the entity. Links can provide additional contextual information that may be located outside of Backstage itself. For example, an admin dashboard or external CMS page.",
    )