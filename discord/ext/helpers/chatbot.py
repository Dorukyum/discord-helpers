from prsaw import RandomStuff


async def chatbot(message: str, *, api_key: str, language: str = "en") -> str:
    wrapper = RandomStuff(async_mode=True, api_key=api_key)
    return await wrapper.get_ai_response(message, lang=language)
