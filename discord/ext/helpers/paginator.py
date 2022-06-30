from asyncio import TimeoutError
from typing import List, Optional

from discord.ext.commands import Bot, Context

from discord import Embed, Message


class Paginator:
    def __init__(
        self,
        bot: Bot,
        pages: List[Embed] = [],
        remove_user_reaction: bool = True,
        first_page_index: int = 0,
    ) -> None:
        self.bot: Bot = bot
        self.pages: List[Embed] = pages
        self.index: int = first_page_index
        self.message: Optional[Message] = None
        self.remove_user_reaction: bool = remove_user_reaction

    def add_page(self, page: Embed) -> None:
        self.pages.append(page)

    def add_pages(self, pages: List[Embed]) -> None:
        self.pages += pages

    async def start(self, ctx: Context, timeout: float = 30.0) -> None:
        self.message = msg = await ctx.send(embed=self.pages[self.index])
        reaction_list = ["⏮", "◀", "⏹", "▶", "⏭"]
        for reaction in reaction_list:
            await msg.add_reaction(reaction)

        try:
            while True:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda r, u: not u.bot
                    and str(r.emoji) in reaction_list
                    and r.message == msg,
                    timeout=timeout,
                )
                emoji = str(reaction.emoji)
                edit = True
                if emoji == "▶":
                    if self.index + 1 == len(self.pages):
                        edit = False
                    else:
                        self.index += 1
                elif emoji == "◀":
                    if self.index == 0:
                        edit = False
                    else:
                        self.index -= 1
                elif emoji == "⏹":
                    return await msg.clear_reactions()
                elif emoji == "⏭":
                    self.index = len(self.pages) - 1
                elif emoji == "⏮":
                    self.index = 0

                if self.remove_user_reaction:
                    await msg.remove_reaction(emoji, user)

                if edit:
                    await msg.edit(embed=self.pages[self.index])

        except TimeoutError:
            await msg.clear_reactions()

    async def stop(self) -> None:
        if self.message:
            await self.message.clear_reactions()
