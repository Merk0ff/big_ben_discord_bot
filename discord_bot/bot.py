import discord
import pickledb

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from discord.errors import ClientException

from datetime import datetime


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = pickledb.load('bot.db', True)
        self.__active_voice_client = []

        if not self.db.exists('channels'):
            self.db.lcreate('channels')

        self.sched = AsyncIOScheduler()
        self.sched.add_job(self.big_boy, 'cron', minute='*/15')
        self.sched.add_job(self.big_boy_leave, 'cron', minute='*/15', second='*/40')
        self.sched.start()

    @commands.command()
    async def subscribe(self, ctx):
        channel = ctx.author.voice.channel

        self.db.ladd('channels', channel.id)

    async def big_boy(self):
        time = datetime.now().strftime('%-I%M')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f'./audio_out/{time}.mp3'))

        for i in self.db.lgetall('channels'):
            channel = self.bot.get_channel(i)
            try:
                voice_client = await channel.connect()
            except ClientException:
                continue

            voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

            self.__active_voice_client.append(voice_client)

    async def big_boy_leave(self):
        for i in self.__active_voice_client:
            await i.disconnect(force=True)

        self.__active_voice_client = []

    @commands.command()
    async def unsubscribe(self, ctx):
        channel_id = ctx.author.voice.channel.id
        self.db.lremvalue('channels', channel_id)
