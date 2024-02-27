# generated by datamodel-codegen:
#   filename:  Component
#   timestamp: 2024-02-27T19:48:38+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel

from .Entity import Component


class ApiVersion(Enum):
    backstage_io_v1alpha1 = "backstage.io/v1alpha1"
    backstage_io_v1beta1 = "backstage.io/v1beta1"


class Kind(Enum):
    Component = "Component"


class ProvidesApi(RootModel[str]):
    root: str = Field(..., min_length=1)


class ConsumesApi(RootModel[str]):
    root: str = Field(..., min_length=1)


class DependsOnItem(RootModel[str]):
    root: str = Field(..., min_length=1)


class Spec(BaseModel):
    type: str = Field(
        ...,
        description="The type of component.",
        examples=["service", "website", "library"],
        min_length=1,
    )
    lifecycle: str = Field(
        ...,
        description="The lifecycle state of the component.",
        examples=["experimental", "production", "deprecated"],
        min_length=1,
    )
    owner: str = Field(
        ...,
        description="An entity reference to the owner of the component.",
        examples=["artist-relations-team", "user:john.johnson"],
        min_length=1,
    )
    system: Optional[str] = Field(
        None,
        description="An entity reference to the system that the component belongs to.",
        min_length=1,
    )
    subcomponentOf: Optional[str] = Field(
        None,
        description="An entity reference to another component of which the component is a part.",
        min_length=1,
    )
    providesApis: Optional[list[ProvidesApi]] = Field(
        None,
        description="An array of entity references to the APIs that are provided by the component.",
    )
    consumesApis: Optional[list[ConsumesApi]] = Field(
        None,
        description="An array of entity references to the APIs that are consumed by the component.",
    )
    dependsOn: Optional[list[DependsOnItem]] = Field(
        None,
        description="An array of references to other entities that the component depends on to function.",
    )


class Component(Model_1):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec
