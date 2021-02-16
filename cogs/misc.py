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
