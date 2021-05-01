import aiosqlite, discord
from discord.ext import commands
from typing import Union, Coroutine


class Prefixes:
    @staticmethod
    def custom_prefix(db_name: str, default: str) -> Coroutine:
        async def get_prefix(bot, message):
            try:
                async with aiosqlite.connect(db_name) as con:
                    async with con.cursor() as cur:
                        await cur.execute(
                            "CREATE TABLE IF NOT EXISTS prefixes (guild_id BIGINT, prefix TEXT)"
                        )
                        await cur.execute(
                            "SELECT prefix FROM prefixes WHERE guild_id={}".format(
                                message.guild.id
                            ),
                        )
                        prefix = await cur.fetchall()
                        if prefix == []:
                            await cur.execute(
                                f"INSERT INTO prefixes VALUES ({message.guild.id}, '{default}')",
                            )
                            await con.commit()
                            prefix = [default]
                        return prefix[0]
            except AttributeError:
                return default

        return get_prefix

    @staticmethod
    async def reply_with_prefix(
        bot: Union[commands.Bot, discord.Client], message: discord.Message
    ) -> discord.Message:
        prefix = bot.command_prefix
        if callable(prefix):
            prefix = prefix(bot, message)
        return await message.channel.send(f"My prefix is `{prefix}`")

    @staticmethod
    async def change_prefix(db_name: str, guild_id: int, prefix: str):
        async with aiosqlite.connect(db_name) as con:
            async with con.cursor() as cur:
                await cur.execute(
                    f"UPDATE data SET prefix='{prefix}' WHERE guild_id={guild_id}"
                )
                await con.commit()
