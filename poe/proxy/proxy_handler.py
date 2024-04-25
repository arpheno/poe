from aiohttp import ClientSession, web


class ProxyHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    async def forward_request(self, request):
        """High-level function to handle request forwarding."""
        target_url = self._construct_url(request)
        headers, data = await self._extract_request_details(request)
        response = await self._process_request(request.method, target_url, headers, data)
        return self._build_client_response(response)

    def _construct_url(self, request):
        """Constructs the full URL to which the request will be forwarded."""
        path = request.match_info.get('path', '/')
        query_string = request.query_string
        target_url = f"{self.base_url}/{path}"
        if query_string:
            target_url += f'?{query_string}'
        return target_url

    async def _extract_request_details(self, request):
        """Extracts necessary details from the request to be forwarded."""
        headers = self._filter_headers(request.headers)
        data = await request.read()
        return headers, data

    def _filter_headers(self, headers):
        """Filters and returns headers to forward, excluding specific headers."""
        return {k: v for k, v in headers.items() if k.lower() != 'host'}

    async def _process_request(self, method, url, headers, data):
        """Processes the request by making an HTTP call to the target API."""
        async with ClientSession() as session:
            async with session.request(method, url, headers=headers, data=data) as resp:
                return await resp.read(), resp

    def _build_client_response(self, response):
        """Builds the response to be sent back to the client."""
        data, resp = response
        headers_for_client = {
            'content-type': resp.headers.get('content-type', 'text/plain'),
            'content-length': str(len(data)),
            **{k: v for k, v in resp.headers.items() if k.lower().startswith('x-rate-limit')}
        }
        return web.Response(body=data, status=resp.status, headers=headers_for_client)
