from inspect import iscoroutinefunction
from typing import Coroutine

import aiosqlite

import discord
from discord.ext import commands


class Database:
    def __init__(self, bot: commands.Bot, filename: str) -> None:
        self.filename = filename
        self.bot = bot

    def custom_prefix(self, default: str) -> Coroutine:
        async def get_prefix(_, message):
            try:
                async with aiosqlite.connect(self.filename) as con:
                    async with con.cursor() as cur:
                        await cur.execute(
                            "CREATE TABLE IF NOT EXISTS prefixes (guild_id BIGINT PRIMARY KEY, prefix TEXT)"
                        )
                        await cur.execute(
                            "SELECT prefix FROM prefixes WHERE guild_id=?",
                            (message.guild.id,),
                        )
                        prefix = await cur.fetchall()
                        if prefix == []:
                            await cur.execute(
                                "INSERT INTO prefixes VALUES (?, ?)",
                                (message.guild.id, default),
                            )
                            await con.commit()
                            prefix = [default]
                        return prefix[0]
            except AttributeError:
                return default

        return get_prefix

    async def reply_with_prefix(self, message: discord.Message) -> discord.Message:
        prefix = self.bot.command_prefix
        if callable(prefix):
            if iscoroutinefunction(prefix):
                prefix = await prefix(self.bot, message)
            else:
                prefix = prefix(self.bot, message)
        return await message.channel.send(f"My prefix is `{prefix}`")

    async def change_prefix(self, guild_id: int, prefix: str) -> None:
        async with aiosqlite.connect(self.filename) as con:
            async with con.cursor() as cur:
                await cur.execute(
                    "UPDATE prefixes SET prefix=? WHERE guild_id=?", (prefix, guild_id)
                )
                await con.commit()
