from discord.ext import commands
import json


class Banwords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Banwords are ready')

    @commands.command(name='add_banword')
    @commands.has_permissions(administrator=True)
    async def add_banword(self, ctx, *args):
        string = " ".join(args)
        mas = string.split("-")
        print(mas)
        new_banword = '-'.join(mas[1:])
        with open('data/censored.json', encoding='utf-8') as bad_words:
            censored = json.load(bad_words)
        censored[mas[0]] = new_banword
        with open('data/censored.json', "w", encoding='utf-8') as bad_words:
            json.dump(censored, bad_words, ensure_ascii=False)
            await ctx.send(f'Отныне и во веки веков "{mas[0]}" это "{new_banword}"')
            a = open("data/Flag.txt", "w")
            a.write("True")
            a.close()

    @commands.command(name='del_banword')
    @commands.has_permissions(administrator=True)
    async def del_banword(self, ctx, *args):
        word = ' '.join(args)
        with open('data/censored.json', encoding='utf-8') as bad_words:
            censored = json.load(bad_words)
        if word in censored:
            del censored[word]
        else:
            await ctx.send("Незнаю кто из нас балбес но это слово не запрещено")
            return
        with open('data/censored.json', "w", encoding='utf-8') as bad_words:
            json.dump(censored, bad_words, ensure_ascii=False)
            await ctx.send(f'отныне и во веки веков "{word}" это "{word}"')


async def setup(bot):
    await bot.add_cog(Banwords(bot))
