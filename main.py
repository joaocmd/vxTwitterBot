import datetime
import discord
import json
import re
import pytwitter

with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN: str = config['DISCORD_TOKEN']
TWITTER_BEARER_TOKEN: str = config['TWITTER_BEARER_TOKEN']

PREAMBLE: str = config['PREAMBLE']
MATCH: str = config['MATCH']
REPLACE: str = config['REPLACE']
TAG: bool = config['TAG']

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

twitter_api = pytwitter.Api(bearer_token=TWITTER_BEARER_TOKEN)

def check_video_twitter_api(tweet_id: str):
    tweet = twitter_api.get_tweet(tweet_id, expansions=["attachments.media_keys"], media_fields=["type"])
    return (tweet.includes and tweet.includes.media and
            any(medium.type == 'video' for medium in tweet.includes.media))

def check_video_no_twitter(message: discord.Message):
    return (MATCH in message.content and
            message.embeds and any(embed.video and embed.video.url for embed in message.embeds))

@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return

    match = re.match('https://twitter.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    if match:
        tweet_id = match.group(1)

    if TWITTER_BEARER_TOKEN:
        has_video = check_video_twitter_api(tweet_id)
    else:
        has_video = check_video_no_twitter(message)

    print(datetime.datetime.now(), message.author, message.content)
    if MATCH in message.content and has_video:
        if TAG:
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'
        else:
            new_message = f'@{message.author.display_name} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'

        await message.channel.send(new_message)
        await message.delete()

bot.run(DISCORD_TOKEN)
