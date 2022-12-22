import asyncio

import os
import logging

from dotenv import load_dotenv

from utils.bot import Brains

load_dotenv('secrets.env')
TOKEN = os.getenv("TOKEN")

log = logging.getLogger(__name__)

async def run_bot():
    async with Brains() as bot:
        bot.remove_command('help')
        await bot.start(TOKEN)
        
        

def main():
    asyncio.run(run_bot())
    


if __name__ == '__main__':
    main()
