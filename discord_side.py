import asyncio
import discord
import os

from aiohttp import web
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


class SoraBridge(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=intents,
        )
        self.http_app = web.Application()
        self.http_app.router.add_post('/webhook', self.handle_message)

    async def on_ready(self):
        delay_time = str(round(self.latency*1000, 2))
        logger.success(f'{self.user} is starting......')
        logger.success(f'{self.user} is online. delay time: {delay_time}ms.')
        status = discord.Activity(
            type=discord.ActivityType.streaming, name='chat-realy')
        await self.change_presence(status=discord.Status.online, activity=status)
        asyncio.create_task(self.start_http_server())

    async def handle_message(self, message):
        try:
            data = await message.json()
            logger.debug(str(data))
            await self.get_channel(int(os.getenv('TARGET_CHANNEL'))).send(str(data))
        except Exception as e:
            logger.error(str(e))
            return web.json_response({'error': str(e)}, status=400)
        return web.json_response({'ok': 'sucess'}, status=200)

    async def start_http_server(self):
        runner = web.AppRunner(self.http_app)
        await runner.setup()
        await web.TCPSite(runner, '127.0.0.1', os.getenv('PORT')).start()
        logger.debug('HTTP server is running on http://127.0.0.1:7000')

    @app_commands.command(name='ping', description='return bot delay')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'delay time: {str(round(self.bot.latency*1000, 2))}ms.')


if __name__ == '__main__':
    bot = SoraBridge()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
