import asyncio
from typing import Callable

from aiohttp import web


class ProxyServer:
    def __init__(self, handler: Callable, port=8080):
        self.handler = handler
        self.port = port
        self.app = web.Application()
        self.app.router.add_route('*', '/{path:.*}', handler)
        self.runner = web.AppRunner(self.app)

    async def setup_server(self):
        self.app.router.add_route('*', '/{path:.*}', self.handler)
        self.runner = web.AppRunner(self.app)

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, 'localhost', self.port)
        await site.start()
        print(f"Server started at http://localhost:{self.port}")
        while True:
            await asyncio.sleep(3600)
