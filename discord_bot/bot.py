import re
import logging

import discord
import pickledb

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from discord.errors import ClientException

from datetime import datetime, timezone, timedelta

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
        self.sched.add_job(self.big_boy_leave, 'cron', minute='*/1')
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

    async def get_time(self, channel_id):
        if tz := self.db.get(f'{channel_id}_tz'):
            tzinfo = timezone(timedelta(hours=tz))
            return datetime.now(tzinfo).strftime('%-I%M')

        return datetime.now().strftime('%-I%M')

    async def big_boy(self):
        for i in self.db.lgetall('channels'):
            channel = self.bot.get_channel(i)
            time = await self.get_time(i)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f'./audio_out/{time}.mp3'))
            try:
                voice_client = await channel.connect()
            except ClientException:
                continue

            logger.info(f'Played in {channel.name} at {time}')
            voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

            self.__active_voice_client.append(voice_client)

    async def big_boy_leave(self):
        out = []

        for i in self.__active_voice_client:
            if not i.is_playing():
                await i.disconnect(force=True)
            else:
                out.append(i)

        self.__active_voice_client = out

    @commands.command()
    async def test(self, ctx):
        channel = ctx.author.voice.channel
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./audio_out/100.mp3'))
        voice_client = await channel.connect()
        voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        self.__active_voice_client.append(voice_client)

    @commands.command()
    async def set_tz(self, ctx, arg):
        match = re.match(r'[+-](?:[1-9]|[1][0-2])\b', arg)

        if match:
            channel_id = ctx.author.voice.channel.id
            self.db.set(f'{channel_id}_tz', int(match[0]))
            await ctx.send(f'TZ successfully set to {match[0]}')
        else:
            await ctx.send(f'IDK about this TZ: {arg}')


    @commands.command()
    async def unsubscribe(self, ctx):
        channel_id = ctx.author.voice.channel.id
        guild_id = ctx.guild.id

        self.db.lremvalue('channels', channel_id)
        self.db.lremvalue('guilds', guild_id)

        await ctx.send('Unsubscribed')
        logger.info(f'Unsubscribe guild: {ctx.guild.name}, {channel_id}')
