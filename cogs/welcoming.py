import discord
from discord.ext import commands

from utils.bot import Brains


class Welcoming(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot

        
    @commands.command()
    async def setwelcome(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            channel = ctx.channel
        query = """
            INSERT INTO welcoming (server_id, channel_id) VALUES ($1, $2)
        """
        await self.bot.pool.execute(query, ctx.guild.id, channel.id)
        await ctx.send(f'Welcoming channel was set up to {channel.mention}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        query = """
            SELECT server_id FROM welcoming
        """
        result = await self.bot.pool.fetch(query)
        guild_ids = []
        
        for i in result:
            raw_id = i['server_id']
            guild_ids.append(raw_id)


        if member.guild.id in guild_ids:
            query = """SELECT channel_id FROM welcoming WHERE server_id = $1"""
            result = await self.bot.pool.fetchrow(query, member.guild.id)
            
            channel_id: discord.TextChannel.id = result['channel_id']
            channel = self.bot.get_channel(channel_id)

            await channel.send(f'Welcome {member.mention} to the server')
        else:
            return
            


async def setup(bot: Brains):
    await bot.add_cog(Welcoming(bot))
