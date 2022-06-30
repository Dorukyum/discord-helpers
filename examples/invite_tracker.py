import discord
from discord.ext import commands, helpers

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents)

bot.tracker = helpers.InviteTracker(bot)
# InviteTracker(bot, "database.db") if you have a database file


@bot.event
async def on_invite_create(invite):
    await bot.tracker.add_invite(invite)


@bot.event
async def on_invite_delete(invite):
    await bot.tracker.add_invite(invite)


@bot.event
async def on_guild_join(guild):
    await bot.tracker.add_guild(guild)


@bot.event
async def on_guild_remove(guild):
    await bot.tracker.remove_guild(guild)


@bot.event
async def on_member_join(member):
    inviter, invite = await bot.tracker.track(member, update_count=True)
    # inviter is the person who invited the new member
    # and invite.uses will give you their invite count


bot.run("TOKEN")
