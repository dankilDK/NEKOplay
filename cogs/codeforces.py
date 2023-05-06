from discord.ext import commands
import requests
import data.db_session as db_session
from data.users import User


class Codeforces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db_session.global_init("db/userinfo.db")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Codeforces is ready')

    @commands.command(name="cf_login")
    async def cf_login(self, ctx, handle):
        params = {
            'handles': handle
        }
        req = requests.get('https://codeforces.com/api/user.info', params=params)
        json_resp = req.json()
        if json_resp['status'] == 'FAILED':
            await ctx.send('Не могу найти тебя, хэндл точно верный?')
            return
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.discord_id == ctx.author.id).first()
        if user:
            user.cf_handle = handle
            db_sess.add(user)
            db_sess.commit()
        else:
            user = User()
            user.discord_id = ctx.author.id
            user.cf_handle = handle
            db_sess.add(user)
            db_sess.commit()
        await ctx.send(f'Отныне и вовеки веков, {str(ctx.author)} сидит на CodeForces с хэндлом "{handle}"')

    @commands.command(name='cf_myinfo')
    async def cf_myinfo(self, ctx):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.discord_id == ctx.author.id).first()
        if user:
            if user.cf_handle:
                params = {
                    'handles': user.cf_handle
                }
                req = requests.get('https://codeforces.com/api/user.info', params=params)
                resp = req.json()
                res = f"```" \
                      f"Handle: {user.cf_handle}\n" \
                      f"Rating: {resp['result'][0]['rating']}\n" \
                      f"Rank: {resp['result'][0]['rank']}" \
                      f"```"
                await ctx.send(res)
            else:
                await ctx.send(f'Аната бака, не связяал себя с хэндлом на CodeForces')
                return
        else:
            await ctx.send(f'Аната бака, не связяал себя с хэндлом на CodeForces')
            return


async def setup(bot):
    await bot.add_cog(Codeforces(bot))
