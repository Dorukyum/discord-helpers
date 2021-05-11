# discord-helpers
![Downloads](https://static.pepy.tech/personalized-badge/discord-helpers?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)
![PyPI](https://img.shields.io/pypi/v/discord-helpers.svg) <br>
A helper module for discord.py

## Current Features (v0.0.2)
* Per server custom prefixes using SQLite3 - aiosqlite
* Chatbot coroutine to get a reply from an AI ([The Random Stuff API](https://api-info.pgamerx.com/))
* A cycling status for your bot
* A coroutine to find a webhook from a channel and send a message via it
* Coroutines for using the GET and POST methods easily

## Installation
### Stable Release:
```
pip install -U discord-helpers
```
### Development:
```
pip install -U git+https://github.com/Dorukyum/discord-helpers.git
```

## Some Examples
### Prefixes
```python
from discord.ext import commands, helpers
bot = commands.Bot(command_prefix = helpers.Prefixes.custom_prefix("data.db", "!"))
```
```python
@bot.event
async def on_message(message):
    if message.mentions[0] == client.user:
        await helpers.Prefixes.reply_with_prefix(bot, message)
```
```python
@bot.command()
async def change_prefix(ctx, *, prefix):
    await helpers.Prefixes.change_prefix("data.db", ctx.guild.id, prefix)
```
### Chatbot
```python
@bot.event
async def on_message(message):
    if message.channel.id == my_chatbot_channel_id:
        response = await helpers.chatbot(message.content, api_key=my_api_key)
        await message.reply(response)
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
@tasks.loop(seconds=12)
async def change_status():
    await bot.change_presence(activity=discord.Game(bot.status.next()))
```
