# generated by datamodel-codegen:
#   filename:  Resource
#   timestamp: 2024-02-27T19:34:26+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, constr

from .Entity import Model as Model_1


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    Resource = "Resource"


class Spec(BaseModel):
    type: constr(min_length=1) = Field(
        ...,
        description="The type of resource.",
        examples=["database", "s3-bucket", "cluster"],
    )
    owner: constr(min_length=1) = Field(
        ...,
        description="An entity reference to the owner of the resource.",
        examples=["artist-relations-team", "user:john.johnson"],
    )
    dependsOn: Optional[list[constr(min_length=1)]] = Field(
        None,
        description="An array of references to other entities that the resource depends on to function.",
    )
    system: Optional[constr(min_length=1)] = Field(
        None,
        description="An entity reference to the system that the resource belongs to.",
    )


class Model(Model_1.Model):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec