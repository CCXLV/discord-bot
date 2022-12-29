import discord
import os

from discord.ext import commands

from googleapiclient.discovery import build

from dateutil import parser
from datetime import datetime
from dotenv import load_dotenv

from utils.bot import Brains

load_dotenv('secrets.env')
API_KEY = os.getenv("YOUTUBE_API_KEY")

api_key = API_KEY
api_service_name = "youtube"
api_version = "v3"

youtube = build(serviceName=api_service_name, version=api_version, developerKey=api_key)

class YoutubeSearch(commands.Cog):
    def __init__(self, bot: Brains):
        self.bot = bot

    
    @commands.command()
    async def ytstats(self, ctx, channel_id: str):
        request = youtube.channels().list(
            part=['statistics', 'brandingSettings', 'snippet'],
            id=channel_id,
        )

        response = request.execute()
        
        for snippet_ in response['items']:
            snippet = snippet_['snippet']
            thumbs = snippet['thumbnails']
            medium = thumbs['medium']
            link = medium['url']
            date = snippet['publishedAt']

        parsed_date = parser.parse(date)
        timestamp = datetime.timestamp(parsed_date)
        round_timestamp = round(timestamp)

        for brandingSettings in response['items']:
            full = brandingSettings['brandingSettings']
            channel = full['channel']
            channel_description = channel['description']
            username = channel['title']

        for i in response['items']:
            raw = i['statistics']

        embed = discord.Embed(title=f'{username}', color=0xFF0000)
        
        embed.description = str(channel_description)
        embed.add_field(name='Custom url', value=f"{snippet['customUrl']}", inline=False)
        embed.add_field(name='Created', value=f'<t:{round_timestamp}:R>', inline=False)
        embed.add_field(name='Videos', value=f"{int(raw['videoCount']):,}", inline=False)
        embed.add_field(name='Subscribers', value=f"{int(raw['subscriberCount']):,}", inline=False)
        embed.add_field(name='Views', value=f"{int(raw['viewCount']):,}", inline=False)
        embed.add_field(name='Channel link', value=f'[Link](https://www.youtube.com/channel/{channel_id})')
        embed.set_thumbnail(url=str(link))
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)







async def setup(bot: Brains):
    await bot.add_cog(YoutubeSearch(bot))
