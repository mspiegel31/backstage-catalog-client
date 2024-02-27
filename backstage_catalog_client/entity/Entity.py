# generated by datamodel-codegen:
#   filename:  Entity
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from . import EntityMeta, common


class Entity(BaseModel):
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
    metadata: EntityMeta.Model
    spec: Optional[dict[str, Any]] = Field(None, description="The specification data describing the entity itself.")
    relations: Optional[list[common.Relation]] = Field(
        None, description="The relations that this entity has with other entities."
    )
    status: Optional[common.Status] = None
