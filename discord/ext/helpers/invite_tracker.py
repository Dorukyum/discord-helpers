import asyncio
from typing import Dict, List, Optional, Union
import aiosqlite
import discord


class InviteTracker:
    def __init__(self, bot: discord.Client, database: Optional[str] = None) -> None:
        self.bot = bot
        self.database = database
        asyncio.get_event_loop().create_task(self._init())

    async def _init(self) -> None:
        self.data = {
            g.id: {i.id: i.uses for i in await g.invites()} for g in self.bot.guilds
        }
        async with aiosqlite.connect(self.database) as con:
            async with con.cursor() as cur:
                await cur.execute(
                    "CREATE TABLE IF NOT EXISTS invites (guild_id BIGINT, invite_id TEXT, uses INT, PRIMARY KEY (guild_id, invite_id))"
                )
                await con.commit()
                await cur.execute("SELECT * FROM invites")
                data = await cur.fetchall()
                if data == []:
                    await self._add_to_db(self.data, True)

    async def _add_to_db(
        self, data: Dict[int, Dict[int, int]], init: bool = False, *, guild_id: int = 0
    ) -> None:
        if self.database is not None:
            async with aiosqlite.connect(self.database) as con:
                async with con.cursor() as cur:
                    if init:
                        for guild_id, value in data.items():
                            for invite_id in value.keys():
                                await cur.execute(
                                    "INSERT INTO invites VALUES (?, ?, ?)",
                                    (guild_id, invite_id, data[guild_id][invite_id]),
                                )
                    else:
                        for invite_id, value_ in data.items():
                            await cur.execute(
                                "INSERT INTO invites VALUES (?, ?, ?)",
                                (guild_id, invite_id, value_),
                            )

                    await con.commit()

    async def _remove_from_db(self, what, data) -> None:
        if self.database is not None:
            async with aiosqlite.connect(self.database) as con:
                async with con.cursor() as cur:
                    await cur.execute(
                        f"DELETE FROM invites WHERE {'invite_id' if what == 'invite' else 'guild_id'} = ?",
                        (data,),
                    )
                    await con.commit()

    async def add_guild(self, guild: discord.Guild) -> None:
        self.data[guild.id] = {i.id: i.uses for i in await guild.invites()}
        await self._add_to_db(self.data[guild.id], guild.id)

    async def remove_guild(self, guild: discord.Guild) -> None:
        del self.data[guild.id]
        await self._remove_from_db("guild", guild.id)

    async def add_invite(self, invite: discord.Invite) -> None:
        self.data[invite.guild.id][invite.id] = invite.uses
        await self._add_to_db(self.data[invite.guild.id][invite.id], invite.guild.id)

    async def remove_invite(self, invite: discord.Invite) -> None:
        del self.data[invite.guild.id][invite.id]
        await self._remove_from_db("invite", invite.id)

    async def increment_uses(self, invite: discord.Invite, count: int) -> None:
        self.data[invite.guild.id][invite.id] += count
        async with aiosqlite.connect(self.database) as con:
            async with con.cursor() as cur:
                await cur.execute(
                    "UPDATE invites SET uses = ? WHERE invite_id = ?",
                    (self.data[invite.guild.id][invite.id], invite.id),
                )
                await con.commit()

    async def track(
        self, member: discord.Member
    ) -> List[Union[discord.Member, discord.Invite]]:
        new_data = {i.id: i.uses for i in await member.guild.invites()}
        for inv in self.data[member.guild.id].keys():
            if new_data[inv] == self.data[member.guild.id][inv] + 1:
                for invite in await member.guild.invites():
                    if invite.id == inv:
                        return [member.guild.get_member(invite.inviter.id), invite]
