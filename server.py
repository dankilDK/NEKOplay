import sys
import asyncio
import discord
import data.ffmpeg_extractor
from discord.ext import commands
import random, logging, json
import os
import data.merge_sort as mergesort
from proccess.env import TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

with open('data/censored.json', encoding='utf-8') as bad_words:
    censored = json.load(bad_words)


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ваши песни ꈍᴗꈍ"))
    logger.info(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        logger.info(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})')


@bot.event
async def on_member_join(self, member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}!'
    )


@bot.event
async def on_message(message):
    global censored
    if message.author == bot.user:
        return
    a = open("data/Flag.txt", "r")
    isit = a.readline().strip()
    if isit == "True":
        with open('data/censored.json', encoding='utf-8') as bad_words:
            censored = json.load(bad_words)
        a.close()
        a = open("data/Flag.txt", "w")
        a.write("False")
        a.close()
    is_bad = False
    msg = message.content
    keys = list(censored.keys())
    keys = mergesort.msort(keys)
    for i in keys:
        if i in msg:
            is_bad = True
            msg = msg.split(i)
            msg = censored[i].join(msg)
        elif i.upper() in msg:
            is_bad = True
            msg = msg.split(i.upper())
            print(censored[i].upper())
            msg = censored[i].upper().join(msg)
        elif i.capitalize() in msg:
            is_bad = True
            msg = msg.split(i.capitalize())
            msg = censored[i].capitalize().join(msg)
    if msg[0] == '!':
        is_bad = False
    if is_bad:
        await message.delete()
        name = str(message.author).split('#')[0]
        good_message = f'{name} хотел сказать: "{msg}"'
        await message.channel.send(good_message)
    await bot.process_commands(message)


async def load():
    cogs = ['cogs.manual', 'cogs.generators_and_games', 'cogs.banword_management', 'cogs.player', 'cogs.codeforces']
    for cog in cogs:
        await bot.load_extension(cog)

async def main(TOKEN):
    async with bot:
        await load()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main(TOKEN))
