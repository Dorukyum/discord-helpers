# discord-helpers
![Downloads](https://static.pepy.tech/personalized-badge/discord-helpers?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)
![PyPI](https://img.shields.io/pypi/v/discord-helpers.svg) <br>
A helper module for discord.py

## Current Features (v0.0.5)
* Per server custom prefixes using SQLite3 - aiosqlite
* Invite tracker
* Paginator
* Chatbot coroutine to get a reply from an AI ([The Random Stuff API](https://api-info.pgamerx.com/))
* A cycling status for your bot
* A function to create a rich embed with every feature in a simple line of code
* A coroutine to find a webhook from a channel and send a message via it
* Coroutines for using the GET and POST methods easily

## Installation
### Stable Release:
```
pip install -U discord-helpers
pip install -U discord-helpers[sqlite]
```
### Development:
```
pip install -U git+https://github.com/Dorukyum/discord-helpers.git
```

## Some Examples
### Prefixes
```python
import discord
from discord.ext import commands, helpers

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    bot.db = helpers.Database(bot, "data.db") # also used in the examples below
    bot.command_prefix = bot.db.custom_prefix("!")
```
```python
@bot.event
async def on_message(message):
	if message.mentions[0] == client.user:
		await bot.db.reply_with_prefix(message)
```
```python
@bot.command()
async def change_prefix(ctx, *, prefix):
	await bot.db.change_prefix(ctx.guild.id, prefix)
    await ctx.send(f"Successfuly changed the prefix to `{prefix}`.")
```
### Chatbot
```python
@bot.event
async def on_message(message):
	if message.channel.id == my_chatbot_channel_id:
		response = await helpers.chatbot(message.content, api_key=my_api_key)
		await message.reply(response)
```
### Paginator
```python
@bot.command()
async def send_pages(ctx):
    paginator = helpers.Paginator(bot, pages=[
        discord.Embed(title="Page 1"),
        discord.Embed(title="Page 2"),
    ])
    paginator.add_page(discord.Embed(title="Page 3"))
    await paginator.start(ctx)
```
### Invite Tracker
```python
tracker = helpers.InviteTracker(bot, "data.db")  # with a database
tracker = helpers.InviteTracker(bot)             # without a database, cached

@bot.event
async def on_invite_create(inv):
    await bot.tracker.add_invite(inv)
# and so on for the guild_join, guild_remove and invite_delete events

@bot.event
async def on_member_join(member):
    inviter, invite = await tracker.track(member)
    await bot.get_channel(my_channel_id).send(inviter.name)
    await tracker.increment_uses(invite, 1)
```
### Webhooks
```python
@bot.command()
async def send_webhook(ctx, *, text):
	await helpers.Webhooks.find_and_send(text, channel=ctx.channel, webhook_name="Test")
```
### Status
```python
bot.status = helpers.StatusCycle("status 1", "status 2")

@tasks.loop(minutes=3)
async def change_status():
	await bot.change_presence(activity=discord.Game(bot.status.next()))
```
