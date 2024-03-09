from __future__ import annotations

import dataclasses
from typing import Any, ClassVar, Protocol

from backstage_catalog_client.models import EntityRef


# thanks https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


def to_dict(obj: IsDataclass, exclude_none: bool = True) -> dict[str, Any]:
    d = dataclasses.asdict(obj)
    if exclude_none:
        return {k: v for k, v in d.items() if v is not None}
    return d


def parse_ref_string(ref: str, default_kind: str | None = None, default_namespace: str | None = None) -> EntityRef:
    colonI = ref.find(":")
    slashI = ref.find("/")

    # If the / is ahead of the :, treat the rest as the name
    if slashI != -1 and slashI < colonI:
        colonI = -1

    kind = None if colonI == -1 else ref[0:colonI]
    namespace = None if slashI == -1 else ref[colonI + 1 : slashI]
    name = ref[max(colonI + 1, slashI + 1) :]

    final_kind = kind or default_kind
    final_namespace = namespace or default_namespace or "default"

    if final_kind is None:
        raise ValueError(
            f'Entity reference {ref} had missing or empty kind (e.g. did not start with "component:" or similar)'
        )

    if final_namespace is None:
        raise ValueError(f"Entity reference {ref} had missing or empty namespace")

    if not name:
        raise ValueError(f"Entity reference {ref} had missing or empty name")

    return EntityRef(kind=final_kind, namespace=final_namespace, name=name)
