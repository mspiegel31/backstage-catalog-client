import asyncio
from urllib.parse import urljoin

import httpx

api_request_path = "/repos/backstage/backstage/contents/"
schema_path = "packages/catalog-model/src/schema"

schema_request = urljoin(api_request_path, schema_path)


async def main():
    async with httpx.AsyncClient(base_url="https://api.github.com/") as client:
        resp = await client.get(schema_request)
        print(resp.json())


if __name__ == "__main__":
    asyncio.run(main())
