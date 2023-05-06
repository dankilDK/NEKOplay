from discord.ext import commands
import random
from data.YT_connect import *
from collections import deque
import data.db_session as db_session
from data.users import User


class Player(commands.Cog, discord.PCMVolumeTransformer):

    def __init__(self, bot):
        self.bot = bot
        self.music_order = {}
        db_session.global_init("db/userinfo.db")

    def play_next(self, g):
        if (len(self.music_order[g]) > 0):
            client, player, name = self.music_order[g][0]
            self.music_order[g].popleft()
            client.play(player, after=lambda e: self.play_next(g))

    @commands.Cog.listener()
    async def on_ready(self):
        print('Player is ready')

    @commands.command(name='neko')
    async def play(self, ctx, op, url):
        print(type(url))
        if url in ['1', '2', '3', '4', '5']:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.discord_id == ctx.author.id).first()
            if user:
                song = eval(f'user.favorite{url}')
                if song:
                    url = song
                else:
                    await ctx.send("В этом слоте нет избранных треков")
                    return
            else:
                await ctx.send("Неть избранных треков, добавь их командой !add_favorite")
                return
        elif url.isdigit():
            await ctx.send("Большие числы, таких слотов нету")
            return
        try:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("bot already jammin' here")

        loop = asyncio.get_event_loop()  # то, что запускается внутри loop выполняется независимо от остальной программы
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        name = data['title']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable='ffmpeg/ffmpeg.exe')
        channel = voice_clients[ctx.guild.id]
        g = ctx.guild.id

        if op == 'play':
            if channel.is_playing():
                channel.stop()
                self.music_order[g].clear()
            try:
                self.music_order[g].append((channel, player, name))
            except KeyError:
                self.music_order[g] = deque()
                self.music_order[g].append((channel, player, name))
            self.play_next(g)
        elif op in ['add', 'push_back', 'push', 'append']:
            try:
                self.music_order[g].append((channel, player, name))
            except KeyError:
                self.music_order[g] = deque()
                self.music_order[g].append((channel, player, name))
            if not channel.is_playing():
                self.play_next(g)
        elif op in ['play_next', 'next', 'push_front', 'appendleft']:
            try:
                self.music_order[g].appendleft((channel, player, name))
            except KeyError:
                self.music_order[g] = deque()
                self.music_order[g].appendleft((channel, player, name))
            if not channel.is_playing():
                self.play_next(g)

    @commands.command(name='pause')
    async def pause(self, ctx):
        voice_clients[ctx.guild.id].pause()

    @commands.command(name='resume', aliases=['continue'])
    async def resume(self, ctx):
        voice_clients[ctx.guild.id].resume()

    @commands.command(name='stop')
    async def stop(self, ctx):
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()

    @commands.command(name='skip')
    async def skip(self, ctx):
        voice_clients[ctx.guild.id].stop()
        print(self.music_order)
        self.play_next(g)

    @commands.command(name='shuffle')
    async def shuffle_songs(self, ctx):
        random.shuffle(self.music_order[ctx.guild.id])

    @commands.command(name='music_order', aliases=['order', 'queue', 'tracklist'])
    async def show_queue(self, ctx):
        res = ""
        g = ctx.guild.id
        for i in range(min(len(self.music_order[g]), 5)):
            res += f'{i + 1}) {self.music_order[g][i][2]}\n'
        if res:
            await ctx.send("Слушайте далее:\n" + res)
        else:
            await ctx.send("Нечего проигрывать :(")

    @commands.command(name='add_favorite')
    async def add_song(self, ctx, slot, url):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.discord_id == ctx.author.id).first()
        if user:
            try:
                exec(f"user.favorite{slot} = url")
                db_sess.add(user)
                db_sess.commit()
            except Exception:
                await ctx.send("Пельмешка, нет такого слота")
        else:
            try:
                user = User()
                user.discord_id = ctx.author.id
                exec(f"user.favorite{slot} = url")
                db_sess.add(user)
                db_sess.commit()
            except Exception:
                await ctx.send("Пельмешка, нет такого слота")

    @commands.command(name='my_favorites')
    async def my_favorites(self, ctx):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.discord_id == ctx.author.id).first()
        if user:
            res = ""
            for i in range(1, 6):
                loop = asyncio.get_event_loop()
                url = eval(f'user.favorite{i}')
                try:
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                    name = data['title']
                    res += f'{i}) {name}\n'
                except Exception:
                    res += f'{i}) Пусто\n'
            await ctx.send(res)
        else:
            ctx.send("Неть избранных треков, добавь их командой !add_favorite")
            return


async def setup(bot):
    await bot.add_cog(Player(bot))
