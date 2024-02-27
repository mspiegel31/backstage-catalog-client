import asyncio
import base64
from pathlib import Path
from urllib.parse import urljoin

import httpx

ROOT = Path(__file__).parent.parent

api_request_path = "/repos/backstage/backstage/contents/"
schema_path = "packages/catalog-model/src"


schema_request = urljoin(api_request_path, schema_path)


async def get_schema_tree(client: httpx.AsyncClient, schema_request: str):
    resp = await client.get(schema_request)
    schemas = list(filter(lambda x: x["name"] == "schema", resp.json())).pop()
    tree_request = httpx.URL(schemas["git_url"]).copy_add_param("recursive", "true")
    tree_resp = await client.get(tree_request)
    return tree_resp.json()


async def write_schemas(client: httpx.AsyncClient, tree_resp: list[dict]):
    base_path = ROOT / Path("schemas")
    if not base_path.exists():
        base_path.mkdir()

    for leaf in tree_resp["tree"]:
        if leaf["type"] == "tree":
            file_path = base_path / Path(leaf["path"])
            if not file_path.exists():
                file_path.mkdir()
        if leaf["type"] == "blob":
            file_path = base_path / Path(leaf["path"])
            client.headers.update(
                {
                    "Accept": "application/vnd.github.object+json",
                    "User-Agent": "backstage_catalog_client",
                }
            )
            content_resp = await client.get(leaf["url"])
            content = content_resp.json()
            writable_content = base64.b64decode(content["content"]).decode("utf-8")
            file_path.write_text(writable_content)


async def main():
    async with httpx.AsyncClient(base_url="https://api.github.com/") as client:
        client.headers.update(
            {
                "Accept": "application/vnd.github.raw+json",
                "User-Agent": "backstage_catalog_client",
            }
        )
        tree = await get_schema_tree(client, schema_request)
        await write_schemas(client, tree)


if __name__ == "__main__":
    asyncio.run(main())
