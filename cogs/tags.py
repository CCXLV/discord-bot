import discord
from discord.ext import commands

from utils.bot import Brains


class Tags(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot


    async def create_tag(self, ctx, name: str, content: str):

        query = """INSERT INTO tags (name, content, guild_id)
                VALUES ($1, $2, $3)"""
        
        await self.bot.pool.execute(query, name, content, ctx.guild.id)

    async def delete_tag(self, ctx, name: str):

        query = """DELETE FROM tags WHERE name = $1 AND guild_id = $2"""

        await self.bot.pool.execute(query, name, ctx.guild.id)
        
    @commands.hybrid_group()
    async def tag(self, ctx, *, name: str):
        tag = await self.bot.pool.fetchrow('SELECT content FROM tags WHERE name = $1 AND guild_id = $2', name, ctx.guild.id)
        
        if not tag:
            await ctx.send("This tag doesn't exist")
        else: 
            await ctx.send(tag['content'])

    @tag.command(name='create')
    async def _create(self, ctx, name: str, *, content: str):
        if len(content) > 2000:
            return await ctx.send('Tag content is a maximum of 2000 characters.')
        else: 
            await self.create_tag(ctx, name, content)
            await ctx.send(f'A new tag has been created named as **{name}**')

    @tag.command(name='delete', aliases=['remove'])
    async def _delete(self, ctx, name: str):
        try:
            await self.delete_tag(ctx, name)
            await ctx.send(f'Tag {name} was deleted.')
        except:
            await ctx.send('Tag was not found.')
    
    
    @tag.command()
    async def all(self, ctx):
        query = """SELECT name FROM tags WHERE guild_id = $1"""

        result = await self.bot.pool.fetch(query, ctx.guild.id)
        names = []

        for name in result:
            raw_name = name['name']
            names.append(raw_name)

        embed = discord.Embed(title='Tags', description='\n'.join(names))
        await ctx.send(embed=embed)

    

async def setup(bot: Brains):
    await bot.add_cog(Tags(bot))
        
