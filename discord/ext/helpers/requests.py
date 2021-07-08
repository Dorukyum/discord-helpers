import aiohttp


class Requests:
    @staticmethod
    async def get(url, **kwargs):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, **kwargs) as resp:
                return resp

    @staticmethod
    async def post(url, **kwargs):
        async with aiohttp.ClientSession() as ses:
            async with ses.post(url, **kwargs) as resp:
                return resp
