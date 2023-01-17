from typing import List
import datetime
import discord
import json
import pytwitter
import re

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

def check_video_twitter_api(tweet_ids: List[str], depth=0):
    tweets = twitter_api.get_tweets(
            tweet_ids[0],
            expansions=["attachments.media_keys", "referenced_tweets.id"],
            media_fields=["type"]
        )

    if not tweets.includes: # does not include any tweet or media
        return False

    if (tweets.includes and tweets.includes.media and
        any(medium.type in ['video', 'animated_gif'] for medium in tweets.includes.media)):
            return True

    if depth == 0 and tweets.includes.tweets: # only check first quote retweet
        if any(check_video_twitter_api([referenced_tweet.id], depth=1) for referenced_tweet in tweets.includes.tweets):
                return True

    return False

def check_video_discord_embed(message: discord.Message):
    return (MATCH in message.content and
            message.embeds and any(embed.video and embed.video.url for embed in message.embeds))

@bot.event
async def on_message(message: discord.Message):
    logging.info('TEST')
    if message.author.id == bot.user.id:
        return

    # Only need to match once, message.content.replace replaces all
    tweet_ids = re.findall('https://twitter.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    if not tweet_ids:
        return

    if TWITTER_BEARER_TOKEN:
        has_video = check_video_twitter_api(tweet_ids)
    else:
        has_video = check_video_discord_embed(message)

    print(datetime.datetime.now(), message.author, message.content)
    if has_video:
        if TAG:
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'
        else:
            new_message = f'@{message.author.display_name} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'

        await message.channel.send(new_message)
        await message.delete()

if TWITTER_BEARER_TOKEN:
    print(datetime.datetime.now(), 'Found twitter API bearer token, using twitter API to check for videos')
else:
    print(datetime.datetime.now(), 'Did not find a twitter API bearer token, using Discord embeds videos. This may fail sometimes.')

bot.run(DISCORD_TOKEN)
