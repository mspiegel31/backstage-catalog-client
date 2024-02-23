from typing import Any

JsonPrimitive = int | float | str | bool | None

JsonObject = dict[str, Any]
JsonArray = list[Any]

JsonValue = JsonObject | JsonArray | JsonPrimitive
