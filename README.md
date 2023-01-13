# vxBot

A Discord bot that replaces messages that contain `https://twitter.com` URLs with `https://vxtwitter.com` (https://github.com/dylanpdx/BetterTwitFix).

Copy the `config-template.json` to a `config.json` and edit as necessary.
The config file is structured as follows:

```json
{
    "DISCORD_TOKEN": "<TOKEN_HERE>",
    "PREAMBLE": "wrote:\n", // message starts with "@mention wrote:\n"
    "MATCH": "https://twitter.com",
    "REPLACE": "https://vxtwitter.com",
    "TAG": false // whether to tag the message author or not
}
```

Necessary bot permissions:
* Read Messages/View Channels
* Send Messages
* Manage Messages
* Embed Links