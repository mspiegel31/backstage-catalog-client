from pydantic import BaseModel


class EntityRef(BaseModel):
    kind: str
    namespace: str | None = "default"
    name: str

    def __str__(self):
        return f"{self.kind}:{self.namespace}/{self.name}"


def parse_ref_string(ref):
    colonI = ref.find(":")
    slashI = ref.find("/")

    # If the / is ahead of the :, treat the rest as the name
    if slashI != -1 and slashI < colonI:
        colonI = -1

    kind = None if colonI == -1 else ref[0:colonI]
    namespace = None if slashI == -1 else ref[colonI + 1 : slashI]
    name = ref[max(colonI + 1, slashI + 1) :]

    if kind == "" or namespace == "" or name == "":
        raise TypeError(f'Entity reference "{ref}" was not on the form [<kind>:][<namespace>/]<name>')  # noqa: TRY003

    return EntityRef(kind=kind, namespace=namespace, name=name)
