from .tvmlog import TvMLog


async def setup(bot):
    cog = TvMLog(bot)
    bot.add_cog(cog)
