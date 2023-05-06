from discord.ext import commands
import random
import data.slot_machine as slot_machine

dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessionStorage = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Generators and Games are ready')

    @commands.command(name='roll_dice')  # Бросок D6
    async def roll_dice(self, ctx, count):
        res = [random.choice(dashes) for _ in range(int(count))]
        await ctx.send(" ".join(res))

    @commands.command(name='randint')  # радномное число в диапозоне
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name='spin')
    async def spin(self, ctx, bet):
        bet = int(bet)
        try:
            self.sessionStorage[ctx.author.id] -= bet
            if self.sessionStorage[ctx.author.id] < 0:
                await ctx.send(f'У Вас мало деняк, у Вас их {self.sessionStorage[ctx.author.id] + bet}')
                self.sessionStorage[ctx.author.id] += bet
                return
        except KeyError:
            self.sessionStorage[ctx.author.id] = 10
            self.sessionStorage[ctx.author.id] -= bet
            if self.sessionStorage[ctx.author.id] < 0:
                await ctx.send(f'У Вас мало деняк, у Вас их {self.sessionStorage[ctx.author.id] + bet}')
                self.sessionStorage[ctx.author.id] += bet
                return
        vals, resp, win = slot_machine.make_spin(bet)
        await ctx.send(vals + '\n' + resp)
        self.sessionStorage[ctx.author.id] += win

    @commands.command(name='spin_rules')
    async def spin_rules(self, ctx):
        res = '''
    ```
Изначально, у Вас есть 10 монет. Вы можете сыграть в слот-машину командой !spin x, x - Ваша ставка.
Ваш выигрыш зависит от значений на слотах.
Нет одинаковых - вы потеряли свою ставку
Если выпала хотя бы одна "вишня", то Вы ничего не теряете
Два одинаковых - Вы получаете удвоенную ставку
Три одинаковых - Вы получаете пятикратную ставку
Три "семёрки" - Вы получаете десятикратную ставку
    ```
            '''
        await ctx.send(res)

    @commands.command(name='monies')
    async def monies(self, ctx):
        if ctx.author.id in self.sessionStorage:
            await ctx.send(f'У вас {self.sessionStorage[ctx.author.id]} монет')
        else:
            self.sessionStorage[ctx.author.id] = 10
            await ctx.send('У вас 10 монет')


async def setup(bot):
    await bot.add_cog(Games(bot))