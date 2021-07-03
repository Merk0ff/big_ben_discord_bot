import logging

import discord
import pickledb

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from discord.errors import ClientException

from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = pickledb.load('bot.db', True)
        self.__active_voice_client = []

        if not self.db.exists('channels'):
            self.db.lcreate('channels')

        if not self.db.exists('guilds'):
            self.db.lcreate('guilds')

        self.sched = AsyncIOScheduler()
        self.sched.add_job(self.big_boy, 'cron', minute='*/15')
        self.sched.add_job(self.big_boy_leave, 'cron', minute='*/17')
        self.sched.start()

    @commands.command()
    async def subscribe(self, ctx):
        channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id

        if guild_id not in self.db.lgetall('guilds'):
            self.db.ladd('channels', channel_id)
            self.db.ladd('guilds', guild_id)
            logger.info(f'Subscribe guild: {ctx.guild.name}, {channel_id}')
            await ctx.send('Subscribed')
        else:
            await ctx.send('You already subscribed, unsubscribe first')

    async def big_boy(self):
        time = datetime.now().strftime('%-I%M')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f'./audio_out/{time}.mp3'))

        for i in self.db.lgetall('channels'):
            channel = self.bot.get_channel(i)
            try:
                voice_client = await channel.connect()
            except ClientException:
                continue

            logger.info(f'Played in {channel.name} at {time}')
            voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

            self.__active_voice_client.append(voice_client)

    async def big_boy_leave(self):
        for i in self.__active_voice_client:
            await i.disconnect(force=True)

        self.__active_voice_client = []

    @commands.command()
    async def unsubscribe(self, ctx):
        channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id

        self.db.lremvalue('channels', channel_id)
        self.db.lremvalue('guilds', guild_id)

        await ctx.send('Unsubscribed')
        logger.info(f'Unsubscribe guild: {ctx.guild.name}, {channel_id}')
