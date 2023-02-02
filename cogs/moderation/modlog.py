import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import escape_markdown

import time
import difflib
import itertools
from datetime import datetime
import typing as t

from utils.bot import Brains


GUILD_CHANNEL = t.Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel]

MAIN_COLOR = 0x1983ca
POSITIVE_COLOR = 0x309c41
NEGATIVE_COLOR = 0Xcc0202

class ModLog(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot   


    async def send_modlog(self,
        color: discord.Colour,
        title: t.Optional[str],
        text: str,
        member: t.Optional[discord.Member] = None,
        content: t.Optional[str] = None) -> Context:
    
        embed = discord.Embed(description=text[:4093] + '...' if len(text) > 4096 else text)

        if title:
            embed.set_author(name=title)

        embed.timestamp = datetime.utcnow()
        embed.color = color
        
        
        if content and len(content) > 2000:
            content = content[:2000 - 3] + '...'
        


        modlog_channel = self.bot.get_channel() # need an update
        log_message = await modlog_channel.send(
            content=content,
            embed=embed
        )

        return log_message

    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: GUILD_CHANNEL) -> None:
        """Sends a message to log channel if channel gets created in the server."""
    
        if isinstance(channel, discord.CategoryChannel):
            title = 'Category created'
            message = f'{channel.name} (`{channel.id}`)'
        elif isinstance(channel, discord.VoiceChannel):
            title = 'Voice channel created'

            if channel.category:
                message = f'{channel.category}/{channel.name} (`{channel.id}`).'
            else:
                message = f'{channel.name} (`{channel.id}`).'
        else:
            title = "Text channel created"

            if channel.category:
                message = f'{channel.category}\n{channel.name} (`{channel.id}`).'
            else:
                message = f'{channel.name} (`{channel.id}`).'

        await self.send_modlog(POSITIVE_COLOR, title, message)

        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: GUILD_CHANNEL) -> None:
        """Sends a message to log channel if channel gets deleted in the server."""

        if isinstance(channel, discord.CategoryChannel):
            title = 'Category deleted'
            message = f'{channel.name} (`{channel.id}`).'
        elif isinstance(channel, discord.VoiceChannel):
            title = "Voice channel deleted"

            if channel.category:
                message = f'{channel.category}\n{channel.name} (`{channel.id}`).'
            else:
                message = f'{channel.name} (`{channel.id}`).'
        else:
            title = 'Text channel deleted'

            if channel.category:
                message = f'{channel.category}\n{channel.name} (`{channel.id}`).'
            else:
                message = f'{channel.name} (`{channel.id}`).'

        await self.send_modlog(NEGATIVE_COLOR, title, message)
        

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Sends a message in log channel if member joined the server."""

        title = 'Member has joined the server'
        message = f'{member.mention} has joined the server.'

        await self.send_modlog(MAIN_COLOR, title, message, member)

        
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """Sends a message in log channel if member left the server."""

        title = 'Member has left the server'
        message = f'{member.mention} has left the server.'

        
        await self.send_modlog(NEGATIVE_COLOR, title, message, member)

        
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """Sends a message in log channel if a message gets deleted in the server."""

        msg_content = message.content

        if msg_content == f"```{message.content}```":
            msg_content = "Content"
        

        title = 'Message deleted'
        content = f'**Message**\n {msg_content} \n\n sent by {message.author.mention} sent in <#{message.channel.id}> has been deleted.'

        await self.send_modlog(MAIN_COLOR, title, content)
        

    @commands.Cog.listener()
    async def on_message_edit(self, msg_before: discord.Message, msg_after: discord.Message) -> None:
        """Sends a message in log channel if a message gets edited in the server."""

        if msg_before.content == msg_after.content:
            return

        title = "Message edited"

        channel = msg_before.channel

        cleaned_contents = (escape_markdown(msg.clean_content).split() for msg in (msg_before, msg_after))

        diff = difflib.ndiff(*cleaned_contents)
        diff_groups = tuple(
            (diff_type, tuple(s[2:] for s in diff_words))
            for diff_type, diff_words in itertools.groupby(diff, key=lambda s: s[0])
        )

        content_before: t.List[str] = []
        content_after: t.List[str] = []

        for index, (diff_type, words) in enumerate(diff_groups):
            sub = ' '.join(words)
            if diff_type == '-':
                content_before.append(sub)
            elif diff_type == '+':
                content_after.append(sub)
            elif diff_type == ' ':
                if len(words) > 2:
                    sub = (
                        f"{words[0] if index > 0 else ''}"
                        " ... "
                        f"{words[-1] if index < len(diff_groups) - 1 else ''}"
                    )
                content_before.append(sub)
                content_after.append(sub)

        response = (
            f"**Author:** {msg_before.author.mention}\n"
            f"**Channel:** <#{channel.id}> (`{channel.id}`)\n"
            f"**Message ID:** `{msg_before.id}`\n"
            "\n"
            f"**Before**:\n{' '.join(content_before)}\n"
            f"**After**:\n{' '.join(content_after)}\n"
            "\n"
            f"[Jump to message]({msg_after.jump_url})"
        )


        await self.send_modlog(MAIN_COLOR, title, response)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        """Sends a message in log channel when role is created."""
        title = 'Role created'
        content = (
            f'{role.mention}(``{role.id}``) has been created\n'
            f'**Color:** {role.color}\n'
            )

        await self.send_modlog(MAIN_COLOR, title, content)


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """Sends a message in log channel when role is deleted."""
        title = 'Role deleted'
        content = f'**{role.name}**(``{role.id}``) has been deleted.'

        await self.send_modlog(NEGATIVE_COLOR, title, content)


    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):

        title = 'Role edited'

        before_, after_ = [], []


        for before_name in before.permissions:
            before_.append(before_name)
            
        for after_name in after.permissions:
            after_.append(after_name)

        added, removed = [], []
        check = set(after_) - set(before_)

        for name in list(check):
            names = name[0]
            values = name[1]
            if values == True:
                v = True
                s = str(v)
                values = s.replace('True', 'added')
            else:
                v = False
                s = str(v)
                values = s.replace('False', 'removed')

            names_raw = names.replace('_', ' ').replace('guild', 'server') 

            
            if 'added' in values:
                added.append(names_raw)
            else:
                removed.append(names_raw)

        


        if len(added) == 0 and len(removed) > 0 and after_ != before_:
            content = (
                f"**Removed: ** {', '.join(removed)}"
            )
        if len(removed) == 0 and len(added) > 0 and after_ != before_:
            content = (
                f"**Added: ** {','.join(added)}\n"
            )
        elif after_ != before_ and after.name != before.name:
            content = (
                f'**Old name: ** `{before.name}` **New name: ** `{after.name}`\n'
                f"**Added: ** {','.join(added)}\n"
                f"**Removed: ** {', '.join(removed)}"
            )
        elif after_ != before_:
            content = (
                f"**Added: ** {','.join(added)}\n"
                f"**Removed: ** {', '.join(removed)}"
            )
        elif after.name != before.name:
            content = (
                f'**Before name: ** {before.name}\n'
                f'**After name: ** {after.name}'
            )
        else:
            return
           
        
        await self.send_modlog(MAIN_COLOR, title, content)

    
    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):

        title = 'Server edited'
        
        if before.name != after.name:
            message = (f'Server name has been changed:\n'
                       f'Before: `{before.name}`\n'
                       f'After: `{after.name}`')
        elif before.afk_channel != after.afk_channel:
            message = (f'Server AFK channel has been edited:\n'
                       f'Before: {before.afk_channel.mention}\n'
                       f'After: {after.afk_channel.mention}')
        elif before.afk_timeout != after.afk_timeout:
            message = (f'Server AFK timeout has been edited:\n'
                       f'Before: `{before.afk_timeout}`\n'
                       f'After: `{after.afk_timeout}`')
        
        await self.send_modlog(MAIN_COLOR, title, message)


    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):

        title = 'Thread created'
        message = f'Thread {thread.mention} (`{thread.id}`) has been created.'

        await self.send_modlog(POSITIVE_COLOR, title, message)


    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):

        title = 'Thread name edited'
        message = (f'Thread {after.mention} (`{after.id}`) in {after.parent.mention} (`{after.parent.id}`)\n'
                   f'Before: `{before.name}`\n' 
                   f'After: `{after.name}`')

        await self.send_modlog(MAIN_COLOR, title, message)

    
    @commands.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):

        title = 'Thread deleted'
        message = f'Thread **{thread.name}** (`{thread.id}`) in {thread.parent.mention} (`{thread.parent.id}`) deleted.'

        await self.send_modlog(NEGATIVE_COLOR, title, message)

    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        before_roles = []
        after_roles = []
        for role in before.roles:
            before_roles.append(str(role.mention))

        before_roles.reverse()
        before_roles.pop()

        for role in after.roles:
            after_roles.append(str(role.mention))
        
        after_roles.reverse()
        after_roles.pop()

        added, removed = [], []
        
        if after_roles != before_roles:
            add = (set(after_roles) - set(before_roles))
            rem = (set(before_roles) - set(after_roles))
                
        for name in list(add):
            added.append(name)
        for name in list(rem):
            removed.append(name)

        title = 'Member updated'

        if before.nick != after.nick:
            message = (
                f'Member {after.mention} has updated nickname.\n'
                f'Before: `{before.nick}`\n'
                f'After: `{after.nick}`' 
            )
        elif before.roles != after.roles:
            if len(added) != 0 and len(removed) != 0:
                message = (
                    f'Updated {after.mention} roles\n'
                    f'**Added: **{" ".join(added)}\n'
                    f'**Removed: ** {" ".join(removed)}'
                )
            elif len(added) == 0 and len(removed) != 0:
                message = (
                    f'Updated {after.mention} roles\n'
                    f'**Removed: ** {" ".join(removed)}'
                )
            elif len(removed) == 0 and len(added) != 0:
                message = (
                    f'Updated {after.mention} roles\n'
                    f'**Added: **{" ".join(added)}'
                )
            else:
                return
        elif before.guild_avatar != after.guild_avatar:
            message = (
                f'Member {before.mention} has updated server avatar.\n'
            )
        await self.send_modlog(MAIN_COLOR, title, message)

    
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):

        title = 'User banned'
        message = f'User {user.mention} has been banned from server `{guild.name}`.'

        await self.send_modlog(NEGATIVE_COLOR, title, message)


    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):

        title = 'User unbanned'
        message = f'User {user.mention} has been unbanned from server `{guild.name}`.'

        await self.send_modlog(POSITIVE_COLOR, title, message)




async def setup(bot: Brains):
    await bot.add_cog(ModLog(bot))
