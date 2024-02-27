# generated by datamodel-codegen:
#   filename:  Resource
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel

from .Entity import Component as Model_1


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    Resource = "Resource"


class DependsOnItem(RootModel[str]):
    root: str = Field(..., min_length=1)


class Spec(BaseModel):
    type: str = Field(
        ...,
        description="The type of resource.",
        examples=["database", "s3-bucket", "cluster"],
        min_length=1,
    )
    owner: str = Field(
        ...,
        description="An entity reference to the owner of the resource.",
        examples=["artist-relations-team", "user:john.johnson"],
        min_length=1,
    )
    dependsOn: Optional[list[DependsOnItem]] = Field(
        None,
        description="An array of references to other entities that the resource depends on to function.",
    )
    system: Optional[str] = Field(
        None,
        description="An entity reference to the system that the resource belongs to.",
        min_length=1,
    )


class Resource(Model_1):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec
