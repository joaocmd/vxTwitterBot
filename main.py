import datetime
import discord
import json

with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN = config['DISCORD_TOKEN']
PREAMBLE = config['PREAMBLE']
MATCH = config['MATCH']
REPLACE = config['REPLACE']
TAG = config['TAG']

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if MATCH in message.content:
        if TAG:
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'
        else:
            new_message = f'@{message.author.display_name} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'

        if message.embeds and any(embed.video and embed.video.url for embed in message.embeds):
            await message.channel.send(new_message)
            await message.delete()

bot.run(DISCORD_TOKEN)
