# generated by datamodel-codegen:
#   filename:  API
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .Entity import Component as Model_1


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    API = "API"


class Spec(BaseModel):
    type: str = Field(
        ...,
        description="The type of the API definition.",
        examples=["openapi", "asyncapi", "graphql", "grpc", "trpc"],
        min_length=1,
    )
    lifecycle: str = Field(
        ...,
        description="The lifecycle state of the API.",
        examples=["experimental", "production", "deprecated"],
        min_length=1,
    )
    owner: str = Field(
        ...,
        description="An entity reference to the owner of the API.",
        examples=["artist-relations-team", "user:john.johnson"],
        min_length=1,
    )
    system: Optional[str] = Field(
        None,
        description="An entity reference to the system that the API belongs to.",
        min_length=1,
    )
    definition: str = Field(
        ...,
        description="The definition of the API, based on the format defined by the type.",
        min_length=1,
    )


class API(Model_1):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec
