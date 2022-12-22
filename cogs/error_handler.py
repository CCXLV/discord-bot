import discord
from discord.ext import commands

from utils.bot import Brains


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed_mp = discord.Embed(description="You don't have permissions to do that.")
        embed_mra = discord.Embed(description="An argument is missing.")
        embed_cnf = discord.Embed(description="This command was not found.")
        embed_bmp = discord.Embed(description="I don't have required permissions to do that.")

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
