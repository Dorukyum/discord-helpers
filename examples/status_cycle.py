import discord
from discord.ext import commands, helpers, tasks

bot = commands.Bot()

status = helpers.StatusCycle("status 1", "status 2")


@tasks.loop(minutes=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(status.next()))


bot.run()
