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
import aiohttp
from discord import Webhook,AsyncWebhookAdapter
from discord.ext import commands
from utils import emote, default


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, *, m):
        """Makes the bot send something"""
        await ctx.message.delete()
        await ctx.send(m)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """Load any extension"""
        try:
            self.bot.load_extension(f"cogs.{name}")

        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"{emote.check} | Loaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        """Unload any extension"""
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"{emote.check} | Unloaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        """Reload any loaded extension."""
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"{emote.check} | Reloaded extension **{name}**")

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: int, *, message):
        """DM any user with UserID"""
        user = self.bot.get_user(user)
        try:
            await user.send(message)
            await ctx.send(f'{emote.check} | Success!')
        except:
            return await ctx.send(f"{emote.xmark} | Could not send message!")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await ctx.send(f"{emote.check} | Shutting down the system ...")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def bc(self,ctx,*,msg):
        """Broadcast a message to all servers using world-chat"""
        for hook in self.bot.mwebhooks:
            try:
                async def send_webhook():
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(
                            f"{hook}", adapter=AsyncWebhookAdapter(session))

                        e = discord.Embed(color = self.bot.color,description=msg)
                        e.set_author(name=ctx.author,icon_url = ctx.author.avatar_url)
                        await webhook.send(embed=e)

                await send_webhook()
            except:
                continue

def setup(bot):
    bot.add_cog(Dev(bot))
