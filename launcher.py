import asyncio
import asyncpg

import os
import logging

import config

from utils.bot import Brains

log = logging.getLogger(__name__)

async def run_bot():
    async with asyncpg.create_pool(config.postgresql) as pool:
        async with Brains() as bot:
            bot.pool = pool
            bot.remove_command('help')
            await bot.start(config.token)
        
        

def main():
    asyncio.run(run_bot())
    


if __name__ == '__main__':
    main()
