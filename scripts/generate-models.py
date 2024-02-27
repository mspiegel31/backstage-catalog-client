import asyncio
import os
from base64 import b64decode
from pathlib import Path
from urllib.parse import urljoin

import httpx
from dotenv import load_dotenv

load_dotenv()


token = os.getenv("GITHUB_TOKEN")

ROOT = Path(__file__).parent.parent

api_request_path = "/repos/backstage/backstage/contents/"
schema_path = "packages/catalog-model/src"
schema_request = urljoin(api_request_path, schema_path)

client = httpx.AsyncClient(base_url="https://api.github.com/")
if token:
    client.headers.update({"Authorization": f"Bearer {token}"})
client.headers.update({"User-Agent": "backstage_catalog_client"})


async def get_schema_tree(schema_request: str):
    client.headers.update(
        {
            "Accept": "application/vnd.github.raw+json",
        }
    )
    resp = await client.get(schema_request)
    schemas = list(filter(lambda x: x["name"] == "schema", resp.json())).pop()
    tree_request = httpx.URL(schemas["git_url"]).copy_add_param("recursive", "true")
    tree_resp = await client.get(tree_request)
    return tree_resp.json()


async def write_schemas(tree_resp: list[dict]):
    base_path = ROOT / Path("schemas")
    base_path.mkdir(exist_ok=True)

    for entry in tree_resp["tree"]:
        print(f"Processing {entry['path']}")
        if entry["type"] == "tree":
            directory = base_path / Path(entry["path"])
            directory.mkdir(exist_ok=True)

        if entry["type"] == "blob":
            file = base_path / Path(entry["path"])
            client.headers.update(
                {
                    "Accept": "application/vnd.github.object+json",
                }
            )
            content_resp = await client.get(entry["url"])
            content = content_resp.json()["content"]
            file.write_text(b64decode(content).decode("utf-8"))


async def main():
    tree = await get_schema_tree(schema_request)
    await write_schemas(tree)
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
