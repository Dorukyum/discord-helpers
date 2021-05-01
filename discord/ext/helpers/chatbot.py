import aiohttp


async def chatbot(message: str, *, api_key: str = None, language: str = "en") -> str:
    message = "+".join(message.split())
    url = (
        f"https://api.pgamerx.com/ai/response?api_key={api_key}&"
        if api_key
        else "https://api.pgamerx.com/demo/ai/response?"
    )
    url += f"message={message}&language={language}"
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as res:
            return (await res.json())[0]
