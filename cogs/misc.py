"""
MIT License

Copyright (c) 2021 deadshot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import discord
from discord.ext import commands
import config
from utils import emote


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        """Get bot's invite link"""
        m = discord.Embed(
            color=self.bot.color, description=f"[Click here to invite me]({config.bot_invite})\n[Click here to join support server]({config.support_server})")
        try:
            await ctx.send(embed=m)
        except:
            try:
                await ctx.author.send(embed=m)
            except:
                return

            await ctx.send(f"{emote.xmark} | I don't have permissions to send invite here and your PMs are also closed.")

    @commands.command()
    async def botinfo(self, ctx):
        """Get bot's basic info"""
        u = self.bot.get_user(config.dev)
        tu = sum(g.member_count for g in self.bot.guilds)
        embed = discord.Embed(color=self.bot.color)
        embed.description = f"**Total Guilds:** {len(self.bot.guilds)}\n**Total Users:** {tu}\n**Library:** discord.py"
        embed.set_footer(text="Author: {}".format(u), icon_url=u.avatar_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):
        """Get current bot ping"""
        await ctx.send(f'Pong!🏓 : **{round(self.bot.latency * 1000)}ms**')

    @commands.command()
    async def source(self,ctx):
        """Get bot's source"""
        await ctx.send("I am open-sourced at: \n<https://github.com/deadaf/world-chat>")
def setup(bot):
    bot.add_cog(Misc(bot))
