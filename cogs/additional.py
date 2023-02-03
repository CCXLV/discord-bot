import random
import string

import discord
from discord.ext import commands
from discord import app_commands

from utils.http import session
from utils.bot import Brains

from utils.constants import QUOTE_COLORS

class Additional(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot
    
    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(color=0x1983ca)

        embed.add_field(name='About', value=(f'Currently in **{len(self.bot.guilds)}** servers.\n'
                                             f'With a total of **{len(self.bot.users)}** users.'))
        embed.set_footer(text='Made by CCXLV#2179')

        await ctx.send(embed=embed)
    
    @commands.command()
    async def quote(self, ctx):
        main = await session.get("https://api.quotable.io/random")
        data = await main.json()
        quote = data["content"]
        author = data["author"]

        embed = discord.Embed(description=f'**{author}**\n{quote}')
        embed.color = random.choice(QUOTE_COLORS)
        await ctx.send(embed=embed)

   


async def setup(bot: Brains):
    await bot.add_cog(Additional(bot))
