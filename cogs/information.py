import discord

from discord.ext import commands
from discord import Embed
from discord.utils import format_dt
from datetime import datetime

from utils.bot import Brains

from typing import Optional

class Information(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot

    @commands.command(aliases=['whois', 'ui', 'user'])
    @commands.guild_only()
    async def userinfo(self, ctx, member: Optional[discord.Member]):
        guild_ = self.bot.get_guild(ctx.guild.id)
        role_color = guild_.self_role.color
        if not member:
            member = ctx.author

        roles = []

        for role in member.roles:
            roles.append(str(role.mention))

        roles.reverse()
        roles.pop()
        
        embed = Embed()
        embed.add_field(name='User', value=member.mention, inline=False)
        embed.add_field(name='User ID', value=member.id, inline=False)
        embed.add_field(name='Created', value=format_dt(member.created_at, style="R"), inline=False)
        embed.add_field(name='Joined', value=format_dt(member.joined_at, style="R"), inline=False)
        if len(member.roles) == 1:
            embed.add_field(name='Roles', value='None' , inline=False)
        else:
            embed.add_field(name=f'Roles - {len(roles)}', value=f'{" ".join(roles)}' , inline=False)

        embed.set_thumbnail(url=member.avatar.url)
        if role_color == discord.Color(0x000000):
            embed.color = 0x1983ca
        else:
            embed.color = role_color
            
        await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    @commands.guild_only()
    async def avatar(self, ctx, member: Optional[discord.Member]):
        guild_ = self.bot.get_guild(ctx.guild.id)
        role_color = guild_.self_role.color
        if not member:
            member = ctx.author

        embed = Embed(title=member.name + '#' + member.discriminator + ' Avatar')
        embed.set_image(url=member.avatar.url)
        if role_color == discord.Color(0x000000):
            embed.color = 0x1983ca
        else:
            embed.color = role_color

        await ctx.send(embed=embed)

    @commands.command(aliases=['server'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild_ = self.bot.get_guild(ctx.guild.id)
        role_color = guild_.self_role.color

        online = []
        offline = []

        for member in ctx.guild.members:
            if str(member.status) in ('online', 'dnd'):
                online.append(str(member))
            else:
                offline.append(str(member))

        roles = []

        for role in ctx.guild.roles:
            roles.append(str(role.mention))

        roles.reverse()
        roles.pop()
        
        embed = Embed()
        if ctx.message.guild.icon is not None:
            embed.set_thumbnail(url=ctx.message.guild.icon.url)
        embed.title = ctx.guild.name
        embed.description = (
            f'Created: {format_dt(ctx.guild.created_at, style="R")}'
        )
        embed.add_field(name='Server ID', value=ctx.guild.id, inline=False)
        embed.add_field(name='Server Owner', value=ctx.guild.owner, inline=False)
        embed.add_field(name=f'Roles - {len(ctx.guild.roles)}', value=' '.join(roles), inline=False)
        embed.add_field(name=f'Members - {len(ctx.guild.members)}', value=(
            f'Status: <:green:1039223047607029945> {len(online)}   <:gray:1039223027528892436> {len(offline)}'
        ), inline=False)
        embed.add_field(name=f'Channels - {len(ctx.guild.channels)}', value=(
            f'Category: {len(ctx.guild.categories)}\n'
            f'Text: {len(ctx.guild.text_channels)}\n'
            f'Voice: {len(ctx.guild.voice_channels)}\n'
            f'Stage: {len(ctx.guild.stage_channels)}\n'
            f'Forum: {len(ctx.guild.forums)}\n'
        ), inline=False)
        embed.set_footer(text='Requested by ' + str(ctx.author))
        embed.timestamp = datetime.utcnow()
        
        if role_color == discord.Color(0x000000):
            embed.color = 0x1983ca
        else:
            embed.color = role_color

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, role: discord.Role):
        permissions = [] 

        for name in role.permissions:
            permissions.append(name)

        result = []

        for name in permissions:
            perm_name = name[0]
            value = name[1]
            final_name = perm_name.replace('_', ' ').replace('guild', 'server')

            full = (f"{final_name}: `{str(value)}`")

            cap = full.capitalize()   
            result.append(cap)


        embed = Embed(color=0x1983ca)
        embed.description = (
            f'**Role: ** {role.mention}\n'
            f'**Role ID: ** `{role.id}`'
        )
        embed.add_field(name='Permissions', value='\n'.join(result))
        
        await ctx.send(embed=embed)
 
            
    @commands.command(aliases=['perms'])
    @commands.guild_only()
    async def permissions(self, ctx, member: Optional[discord.Member], channel: Optional[Union[discord.TextChannel, discord.ForumChannel]]):
        if not member:
            member = ctx.author
        
        if not channel:
            channel = ctx.channel

        permissions = channel.permissions_for(member)

        allowed = []
        denied = []

        for name, value in permissions: # This code is licensed MPL v2 from Rapptz/RoboDanny | https://github.com/Rapptz/RoboDanny
            name = name.replace('_', ' ').replace('guild', 'server')
            if value:
                cap_name = name.capitalize()
                allowed.append(cap_name)
            else:
                cap_name = name.capitalize()
                denied.append(cap_name)
            


        embed = Embed(color=0x1983ca)
        embed.add_field(name='Allowed', value='\n'.join(allowed))
        embed.add_field(name='Denied', value='\n'.join(denied))

        embed.set_author(name=member, icon_url=member.avatar.url)

        await ctx.send(embed=embed)
        





async def setup(bot: Brains):
    await bot.add_cog(Information(bot))
