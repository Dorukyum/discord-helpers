import aiohttp


async def chatbot(message: str, *, api_key: str, language: str = "en") -> str:
    headers = {"x-api-key": api_key}
    params = {"type": "stable", "message": message}
    async with aiohttp.ClientSession() as ses:
        async with ses.get(
            "https://api.pgamerx.com/v3/ai/response", headers=headers, params=params
        ) as response:
            return await response.json()
