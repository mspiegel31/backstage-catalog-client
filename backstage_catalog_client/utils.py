import dataclasses
from typing import Any, ClassVar, Dict, Protocol

from pydantic import BaseModel


# thanks https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, Any]]


class EntityRef(BaseModel):
    kind: str
    namespace: str | None = "default"
    name: str

    def __str__(self):
        return f"{self.kind}:{self.namespace}/{self.name}"


def parse_ref_string(ref: str):
    colonI = ref.find(":")
    slashI = ref.find("/")

    # If the / is ahead of the :, treat the rest as the name
    if slashI != -1 and slashI < colonI:
        colonI = -1

    kind = None if colonI == -1 else ref[0:colonI]
    namespace = None if slashI == -1 else ref[colonI + 1 : slashI]
    name = ref[max(colonI + 1, slashI + 1) :]

    if not kind or not namespace or not name:
        raise TypeError(f'Entity reference "{ref}" was not on the form [<kind>:][<namespace>/]<name>')

    return EntityRef(kind=kind, namespace=namespace, name=name)


def to_dict(obj: IsDataclass, exclude_none: bool = True):
    d = dataclasses.asdict(obj)
    if exclude_none:
        return {k: v for k, v in d.items() if v is not None}
    return d
