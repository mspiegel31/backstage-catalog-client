from typing import Literal

from pydantic import BaseModel

from backstage_catalog_client.entities import Entity


class ComponentSpec(BaseModel):
    type: str
    lifecycle: str
    owner: str
    subcomponentOf: str | None
    providesApis: list[str] | None
    consumesApis: list[str] | None
    dependsOn: list[str] | None
    system: str | None


class ComponentEntity(Entity):
    apiVersion: Literal["backstage.io/v1alpha1"] | Literal["backstage.io/v1beta1"]
    kind: Literal["Component"]
    spec: ComponentSpec
