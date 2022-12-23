import typing

import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed

from utils.bot import Brains

from typing import Optional

class Moderation(Cog):
    def __init__(self, bot: Brains):
        self.bot = bot
    

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        if reason == None:
            reason = 'Wasn\'t mentioned'

        if member == ctx.author:
            embed = Embed(color=0xb30101)
            embed.description = (
                'I can\'t kick you.'     
            )
            await ctx.send(embed=embed)
        elif member == ctx.bot.user:
            embed = Embed(color=0xb30101)
            embed.description = (
                'You can\'t kick me. I am the one who **knocks!**'
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0x5e7bdd)
            embed.description = (
                f'**Reason:** {reason}'
            )
            embed.set_author(icon_url=member.avatar, name=f'{member.name}' + '#' + f'{member.discriminator} has been kicked.')

            await member.kick(reason=reason)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        if reason == None:
            reason = 'Wasn\'t mentioned.'

        if member == ctx.author:
            embed = Embed(color=0xb30101)
            embed.description = (
                'I can\'t ban you.'
            )
            await ctx.send(embed=embed)
        elif member == ctx.bot.user:
            embed = Embed(color=0xb30101)
            embed.description = (
                'You can\'t ban me. I am the one who **knocks!**'
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0x5e7bdd)
            embed.description = (
                f'**Reason:** {reason}'
            )
            embed.set_author(icon_url=member.avatar, name=f'{member.name}' + '#' + f'{member.discriminator} has been banned.')

            await member.ban(reason=reason)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member):
        
        guild: discord.Guild = ctx.guild

        #embed = Embed(description='Hello', color=0x5e7bdd)
        #embed.set_author(icon_url=member.avatar, name=f"{member.name}" + '#' + f"{member.discriminator} has been unbanned.")

        #await ctx.send(embed=embed)
        await guild.unban(member)
        
    @commands.command(aliases=['delay', 'setdelay'])
    @commands.has_guild_permissions(manage_channels=True)
    async def slowmode(self, ctx, channel: Optional[discord.TextChannel], seconds: int):
        if channel is None:
            channel = ctx.message.channel

        await channel.edit(slowmode_delay=seconds)
        await channel.send("Slowmode added", delete_after=2)
    
    @commands.command(aliases=['reset'])
    @commands.has_guild_permissions(manage_channels=True)
    async def resetlowmode(self, ctx, channel: Optional[discord.TextChannel]):
        if channel is None:
            channel = ctx.message.channel

        await channel.edit(slowmode_delay=0)
        await channel.send("Slowmode removed", delete_after=2)
    
    @commands.command()
    @commands.has_guild_permissions(moderate_members=True)
    async def silent(self, ctx, channel: Optional[discord.TextChannel], role: Optional[discord.Role]):

        if role == int:
            role = role.id

        if not channel:
            channel = ctx.message.channel    

        if not role:
            role = ctx.guild.default_role
        
        
        await channel.set_permissions(role, send_messages=False, read_messages=True)

        if role == ctx.guild.default_role:
            await ctx.send(f"This channel has been silented for **everyone**")
        else:
            await ctx.send(f"This channel has been silented for **{role.name}**")

    @commands.command(aliases=['resetsilent', 'uns'])
    @commands.has_guild_permissions(moderate_members=True)
    async def unsilent(self, ctx, channel: Optional[discord.TextChannel], role: Optional[discord.Role]):

        if role == int:
            role = role.id

        if not channel:
            channel = ctx.message.channel

        if not role:
            role = ctx.guild.default_role

        if role == ctx.guild.default_role:
            await channel.set_permissions(role, send_messages=True)
            await ctx.send(f"This channel has been unsilented for **everyone**")
        else:
            await channel.set_permissions(role, send_messages=True)
            await ctx.send(f"This channel has been unsilented for **{role.name}**")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        amount < 100
        if amount > 100:
            await ctx.send("Can't delete more than 100 messages")
        else:  
            await ctx.channel.purge(limit=amount + 1)
        
        await ctx.send(f'Deleted {amount} messages.', delete_after=2)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):

        if role in member.roles:
            embed = Embed(color=0xb30101)
            embed.description = (
                f'{member.mention} already has the role {role.mention}'
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0x1983ca)
            embed.description = (
                f'Added {role.mention} role to {member.mention}'
            )
            await member.add_roles(role)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):

        if role not in member.roles:
            embed = Embed(color=0xb30101)
            embed.description = (
                f'{member.mention} doesn't have the role {role.mention}'
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0x1983ca)
            embed.description = (
                f'Removed {role.mention} role from {member.mention}'
            )
            await member.remove_roles(role)
            await ctx.send(embed=embed)


    @commands.command(aliases=['chadd'])
    @commands.has_guild_permissions(moderate_members=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def channeladd(self, ctx, channel: Optional[discord.TextChannel], member: Optional[discord.Member]):
        embed = Embed(color=0x1983ca)

        if not channel:
            channel = ctx.channel

        if member == int:
            member = member.id

        if member in channel.members:
            embed.description = (
                f'User {member.mention} is already in this channel {channel.mention}'
            )
        else:
            await channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            embed.description = (
                f'User {member.mention} has been added to this channel {channel.mention}'
            )

        await ctx.send(embed=embed)

    @commands.command(aliases=['chre', 'channelre'])
    @commands.has_guild_permissions(moderate_members=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def channelremove(self, ctx, channel: Optional[discord.TextChannel], member: Optional[discord.Member]):
        embed = Embed(color=0x1983ca)

        if not channel:
            channel = ctx.channel

        if member == int:
            member = member.id

        if member in channel.members:
            await channel.set_permissions(member, view_channel=False)
            embed.description = (
                f'User {member.mention} has been removed from this channel {channel.mention}'
            )
        else:
            embed.description = (
                f'User {member.mention} isn\'t in this channel {channel.mention}'
            )

        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def lock(self, ctx, channel: Optional[discord.TextChannel]):
        embed = Embed(color=0x1983ca)

        if not channel:
            channel = ctx.channel

        await channel.set_permissions(
            ctx.guild.default_role, send_messages=False
        )

        embed.description = (
            f'Channel {channel.mention} has been locked.'
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: Optional[discord.TextChannel]):
        embed = Embed(color=0x1983ca)

        if not channel:
            channel = ctx.channel

        await channel.set_permissions(
            ctx.guild.default_role, send_messages=True
        )

        embed.description = (
            f'Channel {channel.mention} has been unlocked.'
        )

        await ctx.send(embed=embed)



async def setup(bot: Brains):
    await bot.add_cog(Moderation(bot))
