# generated by datamodel-codegen:
#   filename:  Domain
#   timestamp: 2024-02-27T19:34:26+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, constr

from .Entity import Entity


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    Domain = "Domain"


class Spec(BaseModel):
    owner: constr(min_length=1) = Field(
        ...,
        description="An entity reference to the owner of the component.",
        examples=["artist-relations-team", "user:john.johnson"],
    )


class Model(Entity.Model):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec
