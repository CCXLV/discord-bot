import random
import string

import discord
from discord.ext import commands
from discord import Embed
from discord import app_commands

from utils.http import session
from utils.bot import Brains

from utils.constants import QUOTE_COLORS

class Additional(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot
    
    @commands.command()
    async def about(self, ctx):
        embed = Embed(color=0x1983ca)

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

        embed = Embed(description=f'**{author}**\n{quote}')
        embed.color = random.choice(QUOTE_COLORS)
        await ctx.send(embed=embed)

    @app_commands.command(name='password', description='Generates random strong password')
    @app_commands.describe(
        length='The length of the password(less than 100)'
        )
    async def _password(self, interaction: discord.Interaction, length: int):
        password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits,
                k=length
            ))

        if length > 100:
            await interaction.response.send_message('Passoword length can\'t be longer than 100')
        else:
            try:
                await interaction.user.send(f'Your password is `{password}`')
                await interaction.response.send_message('Your password was sent in DMs')
            except:
                await interaction.response.send_message(f'Your password is `{password}`', ephemeral=True)
        
    


async def setup(bot: Brains):
    await bot.add_cog(Additional(bot))
