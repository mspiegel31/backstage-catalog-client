# generated by datamodel-codegen:
#   filename:  EntityEnvelope
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Metadata(BaseModel):
    model_config = ConfigDict(
        extra="allow",
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


class Model(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: str = Field(
        ...,
        description="The version of specification format for this particular entity that this is written against.",
        examples=["backstage.io/v1alpha1", "my-company.net/v1", "1.0"],
        min_length=1,
    )
    kind: str = Field(
        ...,
        description="The high level entity type being described.",
        examples=[
            "API",
            "Component",
            "Domain",
            "Group",
            "Location",
            "Resource",
            "System",
            "Template",
            "User",
        ],
        min_length=1,
    )
    metadata: Metadata
