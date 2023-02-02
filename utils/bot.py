import discord
from discord.ext import commands
import logging

import aiohttp
import asyncpg

log = logging.getLogger(__name__)


extensions = (
    'cogs.events',
    'cogs.additional',
    'cogs.moderation',
    'cogs.information',
    'cogs.tags',
    'cogs.welcoming',
)

class Brains(commands.Bot):
    pool: asyncpg.Pool
    session = aiohttp.ClientSession()
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="?",
            intents=intents,
            status=discord.Status.online,
        )

    async def setup_hook(self) -> None:
        print("Bot is running")

        for extension in extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                log.exception('Failed to load extension %s.', extension)

    async def on_message(self, message):
        if message.author.bot:
            return

        
        await self.process_commands(message)

