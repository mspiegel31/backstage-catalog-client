import asyncio
from urllib.parse import urljoin

import httpx

api_request_path = "/repos/backstage/backstage/contents/"
schema_path = "packages/catalog-model/src"


schema_request = urljoin(api_request_path, schema_path)


async def get_schema_tree(client: httpx.AsyncClient, schema_request: str):
    resp = await client.get(schema_request)
    schemas = list(filter(lambda x: x["name"] == "schema", resp.json())).pop()
    tree_request = httpx.URL(schemas["git_url"]).copy_add_param("recursive", "true")
    tree_resp = await client.get(tree_request)
    return tree_resp.json()


async def main():
    async with httpx.AsyncClient(base_url="https://api.github.com/") as client:
        client.headers.update(
            {
                "Accept": "application/vnd.github.raw+json",
                "User-Agent": "backstage_catalog_client",
            }
        )
        tree = await get_schema_tree(client, schema_request)


if __name__ == "__main__":
    asyncio.run(main())
