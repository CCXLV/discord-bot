import asyncio
import aiohttp

class HTTPSession(aiohttp.ClientSession):
    def __init__(self):
        super().__init__(
            loop=asyncio.get_event_loop()
        )

session = HTTPSession()
