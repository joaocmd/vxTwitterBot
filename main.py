from typing import List, Optional
import discord
import json
import pytwitter
import re

from logger import logger

with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN: str = config['DISCORD_TOKEN']
TWITTER_BEARER_TOKEN: str = config['TWITTER_BEARER_TOKEN']

PREAMBLE: str = config['PREAMBLE']
MATCH: str = config['MATCH']
REPLACE: str = config['REPLACE']

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

twitter_api = pytwitter.Api(bearer_token=TWITTER_BEARER_TOKEN)

def check_video_twitter_api(tweet_ids: List[str], depth: Optional[int] = 0) -> bool:
    """
        Returns whether any tweet specified by `tweet_ids` includes an animated
        GIF or a video. Returns False if the tweet includes any other media,
        even if it is a quote retweet or a video/GIF.

        Arguments:
        tweet_ids --- a list containing the IDs of the tweets in a string format
        depth --- current recursion depth, used to check for quote retweets
    """
    tweets = twitter_api.get_tweets(
            tweet_ids[0],
            expansions=["attachments.media_keys", "referenced_tweets.id"],
            media_fields=["type"]
        )

    if not tweets.includes: # does not include any tweet or media
        return False

    if tweets.includes.media:
        return any(medium.type in ['video', 'animated_gif'] for medium in tweets.includes.media)

    if depth == 0 and tweets.includes.tweets: # only check first quote retweet
        if any(check_video_twitter_api([referenced_tweet.id], depth=1) for referenced_tweet in tweets.includes.tweets):
                return True

    return False

def check_video_discord_embed(message: discord.Message) -> bool:
    """Returns whether a Discord `message` contains an embedded video."""
    return any(embed.video for embed in message.embeds)

@bot.event
async def on_message(message: discord.Message) -> None:
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

    logger.info(f'{message.guild.name}: {message.author} {message.content}')
    if has_video:
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH, REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
                everyone=message.mention_everyone,
                users=message.mentions,
                roles=message.role_mentions
            )
        if message.reference and isinstance(message.reference.resolved, discord.Message):
            allowed_mentions.replied_user = message.author != message.reference.resolved.author
            await message.reference.resolved.reply(new_message, allowed_mentions=allowed_mentions)
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions)

        await message.delete()

if TWITTER_BEARER_TOKEN:
    logger.info('Found twitter API bearer token, using twitter API to check for videos')
else:
    logger.info('Did not find a twitter API bearer token, using Discord embeds videos. This may fail sometimes.')

bot.run(DISCORD_TOKEN, log_handler=None)
