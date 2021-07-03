from discord.ext import commands

from discord_bot import Music

token = 'ODYwOTI3ODEyMTgxNDI2MTg2.YOCXgQ.uzCm_8Reu1uJkLFAO1y2WmMy83Y'

bot = commands.Bot(command_prefix=commands.when_mentioned_or("="),
                   description='Relatively simple music bot example')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))
bot.run(token)
