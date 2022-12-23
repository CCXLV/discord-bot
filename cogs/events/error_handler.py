import discord
from discord.ext import commands
from discord import Embed

from utils.bot import Brains


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed_mp = Embed(color=0xb30101)
        embed_mp.description = (
            'You don\'t have permissions to do that.'
        )
        embed_mra = Embed(color=0xb30101)
        embed_mra.description = (
            'An argument is missing.'
        )
        embed_cnf = Embed(color=0xb30101)
        embed_cnf.description = (
            'This command was not found.'
        )
        embed_bmp = Embed(color=0xb30101)
        embed_bmp.description = (
            'I don\'t have required permissions to do that.'
        )
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=embed_mp)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=embed_mra)
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(embed=embed_cnf)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=embed_bmp)     
        else:
            raise error



async def setup(bot: Brains):
    await bot.add_cog(ErrorHandler(bot))
