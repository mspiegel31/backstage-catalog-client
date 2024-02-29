from httpx import AsyncClient

from backstage_catalog_client.api_client import CATALOG_FILTER_EXISTS, CatalogApi
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    EntityFilterQuery,
    GetEntitiesRequest,
    GetEntitiesResponse,
)
from backstage_catalog_client.utils import to_dict


class DefaultCatalogApi(CatalogApi):
    def __init__(self, base_url: str, client: AsyncClient | None = None) -> None:
        # catalog_api_path = urljoin(base_url, CATALOG_API_BASE_PATH)
        if client is None:
            self.client = AsyncClient()
        else:
            self.client = client

        if str(self.client.base_url):
            self.base_url = str(self.client.base_url)
        else:
            self.base_url = base_url

    async def getEntities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ):
        if request is None:
            request = GetEntitiesRequest()
        if options is None:
            options = CatalogRequestOptions()

        dict_request = to_dict(request)
        if request.filter:
            dict_request["filter"] = self._get_filter_value(request.filter)

        response = await self.client.get(f"{self.base_url}/entities", params=dict_request)
        if response.status_code != 200:
            raise Exception(response.text)

        return GetEntitiesResponse(items=response.json())

    def _get_filter_value(self, filter: EntityFilterQuery = []):
        prepared_filters: list[str] = []
        # filter param can occur multiple times, for example
        # /api/catalog/entities?filter=metadata.name=wayback-search,kind=component&filter=metadata.name=www-artist,kind=component'
        # the "outer array" defined by `filter` occurrences corresponds to "anyOf" filters
        # the "inner array" defined within a `filter` param corresponds to "allOf" filters

        for filter_item in filter:
            filter_parts: list[str] = []
            for key, value in filter_item.items():
                v_iter = value if isinstance(value, list) else [value]
                for v in v_iter:
                    if v == CATALOG_FILTER_EXISTS:
                        filter_parts.append(key)
                    elif isinstance(v, str):
                        filter_parts.append(f"{key}={v}")
            if filter_parts:
                prepared_filters.append(",".join(filter_parts))
        return prepared_filters
