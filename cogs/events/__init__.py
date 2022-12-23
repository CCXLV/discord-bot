from .error_handler import ErrorHandler


class Handler(
    ErrorHandler
):
    """This class is the event handler for the bot."""
    
    pass

async def setup(bot):
    await bot.add_cog(Handler(bot))
