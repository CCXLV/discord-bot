from .moderation import Moderation
from .modlog import ModLog

class Mod(
    Moderation,
    ModLog
):

    pass

async def setup(bot):
    await bot.add_cog(Mod(bot))
