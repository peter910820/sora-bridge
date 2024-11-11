# sora-bridge

chat relay bot instance for Line to Discord for python.

use _aiohttp_

## :notebook_with_decorative_cover: introduction

1. src/detach: This folder provides a example for relay bot detach, _aiohttp_ make discord.py and handle http can do at the same program. Use __discord_side.py__ to run discordbot and catch http request, and use __linebot_side.py__ to handle linebot business and send http request to __discord_side.py__.  
Then can use __linebot_side.py__ to listen line group message and use http request to send message to aiohttp for __discord_side.py__, and display to specify text channel.