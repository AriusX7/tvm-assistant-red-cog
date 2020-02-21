from .tvm import TvM


async def setup(bot):
    cog = TvM(bot)
    bot.add_cog(cog)
