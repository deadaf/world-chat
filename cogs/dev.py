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
