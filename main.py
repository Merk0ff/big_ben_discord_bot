from pathlib import Path

from discord.ext import commands

from discord_bot import Music
from big_ben_sampler import BigBanSampler

token = 'ODYwOTI3ODEyMTgxNDI2MTg2.YOCXgQ.uzCm_8Reu1uJkLFAO1y2WmMy83Y'

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!!"),
                   description='Relatively simple music bot example')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


if __name__ == "__main__":
    if not Path('./audio_out').is_dir():
        sampler = BigBanSampler()
        sampler.save()

    bot.add_cog(Music(bot))
    bot.run(token)
