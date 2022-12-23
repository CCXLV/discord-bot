import discord
from discord.ext import commands
import logging
import aiohttp

log = logging.getLogger(__name__)


extensions = (
    'cogs.events',
    'cogs.additional',
    'cogs.moderation',
    'cogs.youtube_search',
    'cogs.information',
)

class Brains(commands.Bot):
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

        if message.guild is None:
            return await message.author.send("Bot can't be used in DMs(for now).")
        
        await self.process_commands(message)

