# generated by datamodel-codegen:
#   filename:  Group
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
    Group = "Group"


class Profile(BaseModel):
    displayName: Optional[constr(min_length=1)] = Field(
        None,
        description="A simple display name to present to users.",
        examples=["Infrastructure"],
    )
    email: Optional[constr(min_length=1)] = Field(
        None,
        description="An email where this entity can be reached.",
        examples=["infrastructure@example.com"],
    )
    picture: Optional[constr(min_length=1)] = Field(
        None,
        description="The URL of an image that represents this entity.",
        examples=["https://example.com/groups/bu-infrastructure.jpeg"],
    )


class Spec(BaseModel):
    type: constr(min_length=1) = Field(
        ...,
        description="The type of group. There is currently no enforced set of values for this field, so it is left up to the adopting organization to choose a nomenclature that matches their org hierarchy.",
        examples=["team", "business-unit", "product-area", "root"],
    )
    profile: Optional[Profile] = Field(
        None,
        description="Optional profile information about the group, mainly for display purposes. All fields of this structure are also optional. The email would be a group email of some form, that the group may wish to be used for contacting them. The picture is expected to be a URL pointing to an image that's representative of the group, and that a browser could fetch and render on a group page or similar.",
    )
    parent: Optional[constr(min_length=1)] = Field(
        None,
        description="The immediate parent group in the hierarchy, if any. Not all groups must have a parent; the catalog supports multi-root hierarchies. Groups may however not have more than one parent. This field is an entity reference.",
        examples=["ops"],
    )
    children: list[constr(min_length=1)] = Field(
        ...,
        description="The immediate child groups of this group in the hierarchy (whose parent field points to this group). The list must be present, but may be empty if there are no child groups. The items are not guaranteed to be ordered in any particular way. The entries of this array are entity references.",
    )
    members: Optional[list[constr(min_length=1)]] = Field(
        None,
        description="The users that are members of this group. The entries of this array are entity references.",
    )


class Model(Model_1.Model):
    model_config = ConfigDict(
        extra="allow",
    )
    apiVersion: Optional[ApiVersion] = None
    kind: Optional[Kind] = None
    spec: Spec