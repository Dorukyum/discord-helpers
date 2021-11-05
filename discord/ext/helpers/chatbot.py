from typing import Optional
from aiohttp import ClientSession


async def chatbot(
    message: str,
    *,
    api_key: str,
    language: str = "en",
    session: Optional[ClientSession] = None
) -> str:
    headers = {"x-api-key": api_key}
    params = {"type": "stable", "message": message, "language": language}
    async with (session or ClientSession()) as ses:
        async with ses.get(
            "https://api.pgamerx.com/v3/ai/response", headers=headers, params=params
        ) as response:
            return await response.json()
