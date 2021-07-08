import asyncio
from inspect import iscoroutinefunction
from typing import Coroutine, Union

import aiosqlite

import discord
from discord.ext import commands


class Database:
    def __init__(self, bot: Union[commands.Bot, discord.Client], filename: str):
        self.filename = filename
        self.bot = bot
        self.invite_tracker = self.InviteTracker(bot, filename)

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
                                f"INSERT INTO prefixes VALUES (?, ?)",
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

    async def change_prefix(self, guild_id: int, prefix: str):
        async with aiosqlite.connect(self.filename) as con:
            async with con.cursor() as cur:
                await cur.execute(
                    f"UPDATE prefixes SET prefix=? WHERE guild_id=?", (prefix, guild_id)
                )
                await con.commit()

    class InviteTracker:
        def __init__(self, bot, filename):
            self.bot = bot
            self.filename = filename
            asyncio.get_event_loop().create_task(self._init())

        async def _init(self):
            self.data = {
                g.id: {i.id: i.uses for i in await g.invites()} for g in self.bot.guilds
            }
            async with aiosqlite.connect(self.filename) as con:
                async with con.cursor() as cur:
                    await cur.execute(
                        "CREATE TABLE IF NOT EXISTS invites (guild_id BIGINT, invite_id TEXT, uses INT, PRIMARY KEY (guild_id, invite_id))"
                    )
                    await con.commit()
                    await cur.execute("SELECT * FROM invites")
                    data = await cur.fetchall()
                    if data == []:
                        await self._add_to_db(self.data, True)

        async def _add_to_db(self, data, init=False, *, guild_id=0):
            async with aiosqlite.connect(self.filename) as con:
                async with con.cursor() as cur:
                    if init:
                        for guild_id in data.keys():
                            for invite_id in data[guild_id].keys():
                                await cur.execute(
                                    "INSERT INTO invites VALUES (?, ?, ?)",
                                    (guild_id, invite_id, data[guild_id][invite_id]),
                                )
                    else:
                        for invite_id in data.keys():
                            await cur.execute(
                                "INSERT INTO invites VALUES (?, ?, ?)",
                                (guild_id, invite_id, data[invite_id]),
                            )
                    await con.commit()

        async def _remove_from_db(self, what, data):
            async with aiosqlite.connect(self.filename) as con:
                async with con.cursor() as cur:
                    await cur.execute(
                        f"DELETE FROM invites WHERE {'invite_id' if what == 'invite' else 'guild_id'} = ?",
                        (data,),
                    )
                    await con.commit()

        async def add_guild(self, guild):
            self.data[guild.id] = {i.id: i.uses for i in await guild.invites()}
            await self._add_to_db(self.data[guild.id], guild.id)

        async def remove_guild(self, guild):
            del self.data[guild.id]
            await self._remove_from_db("guild", guild.id)

        async def add_invite(self, invite):
            self.data[invite.guild.id][invite.id] = invite.uses
            await self._add_to_db(
                self.data[invite.guild.id][invite.id], invite.guild.id
            )

        async def remove_invite(self, invite):
            del self.data[invite.guild.id][invite.id]
            await self._remove_from_db("invite", invite.id)

        async def increment_uses(self, invite, count):
            self.data[invite.guild.id][invite.id] += count
            async with aiosqlite.connect(self.filename) as con:
                async with con.cursor() as cur:
                    await cur.execute(
                        "UPDATE invites SET uses = ? WHERE invite_id = ?",
                        (self.data[invite.guild.id][invite.id], invite.id),
                    )
                    await con.commit()

        async def track(self, member):
            new_data = {i.id: i.uses for i in await member.guild.invites()}
            for inv in self.data[member.guild.id].keys():
                if new_data[inv] == self.data[member.guild.id][inv] + 1:
                    for invite in await member.guild.invites():
                        if invite.id == inv:
                            return [member.guild.get_member(invite.inviter.id), invite]
