# discord-helpers
![Downloads](https://static.pepy.tech/personalized-badge/discord-helpers?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)
![PyPI](https://img.shields.io/pypi/v/discord-helpers.svg) <br>
A helper module for discord.py and its forks

## Current Features (v0.2.0)
* Invite tracker
* Per server custom prefixes using SQLite3 - aiosqlite
* Paginator
* A chatbot coroutine function to get a reply from an AI ([The Random Stuff API](https://api-info.pgamerx.com/))
* A cycling status for your bot
* A function to create a rich embed with every feature in a simple line of code
* A coroutine function to find a webhook from a channel and send a message via it
* Coroutine functions for making GET and POST requests easily

## Installation
```sh
$ pip install -U discord-helpers
$ pip install -U discord-helpers[sqlite]

# development
$ pip install -U git+https://github.com/Dorukyum/discord-helpers.git
```

## Examples
More bot examples can be found in the [examples](https://github.com/Dorukyum/discord-helpers/tree/main/examples) directory.

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
### Webhooks
```python
@bot.command()
async def send_webhook(ctx, *, text):
	await helpers.Webhooks.find_and_send(text, channel=ctx.channel, webhook_name="Test")
```