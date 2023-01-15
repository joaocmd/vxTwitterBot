# vxTwitterBot

A Discord bot that replaces messages that contain `https://twitter.com` URLs with `https://vxtwitter.com` (https://github.com/dylanpdx/BetterTwitFix).

## Usage

Copy the `config-template.json` to a `config.json` and edit as necessary.
The config file is structured as follows:

```json
{
    "DISCORD_TOKEN": "<TOKEN_HERE>",
    "TWITTER_BEARER_TOKEN": "<TWITTER_BEARER_TOKEN_HERE>",
    "PREAMBLE": "wrote:\n", // message starts with "@mention wrote:\n"
    "MATCH": "https://twitter.com",
    "REPLACE": "https://vxtwitter.com",
    "TAG": false // whether to tag the message author or not
}
```

The `TWITTER_BEARER_TOKEN` field can be left with an empty string.
In that case, the bot uses the message embed to check if it contains a video.
This method does not always work because the embed might not load or might be loaded only after `on_message` is called.

## Necessary bot permissions

The following permissions are necessary to run the bot:
* Read Messages/View Channels (Requires message content intent)
* Send Messages
* Manage Messages
* Embed Links
