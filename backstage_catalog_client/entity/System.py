# generated by datamodel-codegen:
#   filename:  System
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .Entity import Entity as Model_1


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    System = "System"


class Spec(BaseModel):
    owner: str = Field(
        ...,
        description="An entity reference to the owner of the component.",
        examples=["artist-relations-team", "user:john.johnson"],
        min_length=1,
    )
    domain: Optional[str] = Field(
        None,
        description="An entity reference to the domain that the system belongs to.",
        examples=["artists"],
        min_length=1,
    )


class System(Model_1):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind = "System"
    spec: Spec
