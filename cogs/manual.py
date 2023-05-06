import discord
from discord.ext import commands


class Manual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Manual is ready')

    @commands.command(name='manual', aliases=['guide', 'support', 'commands'])
    async def manual(self, ctx):
        msg = '''
```
Привет! Я NEKOplay, и я помогаю вам на сервере! Вот что я умею:

Генераторы:
roll_dice x - Бросить x кубиков
randint mn mx - Случайное число от mn до mx
spin x - сыграть в "слот-машину" со ставкой x монет (абсолютно бесплатно, но вы реальных призов нет :P)
spin_rules - правила "слот-машины"
monies - посмотреть число монет в "слот-машине"

Музыка:
neko play url - включить песню по ссылке, очищает очередь
neko add/push_back/push/append url - добавляет песню в конец очереди
neko play_next/next/push_front/appendleft url - добавляет песню в начало очереди
В этих командах можно заменить ссылку на число от 1 до 5, и тогда включится ваша любимая песня ꈍᴗꈍ

pause - поставить трек на паузу
resume - продолжить воспроизведение
stop - остановить песню и убрать из голосового
skip/continue - пропустить текущую песню
shuffle - перемешать очередь
music_order/order/queue/tracklist - показать до 5 следующих песен в очереди

Избранные песни:
У Вас есть по 5 слотов для любимых песен, чтобы упростить работу с командами neko
add_favorite 1/2/3/4/5 url - на соответствующий слот песню по ссылке
my_favorites - показать ваши любимые песни

А ещё я умею поправлять Ваши сообщения, чтобы всё было культурно! 
```
            '''
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Manual(bot))