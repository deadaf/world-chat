import discord
import aiohttp
import re
import asyncio
from discord.ext import commands
from utils import emote
from discord import Webhook, AsyncWebhookAdapter


class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        if not message.channel.name == "world-chat":
            return

        if message.author.bot:
            return

        role = discord.utils.get(message.guild.roles, name="wc-ignore")
        if role != None:
            if role in message.author.roles:
                return

        if message.content.startswith("w!"):
            return

        urls = re.findall(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.lower())
        if urls:
            try:
                await message.delete()
            except:
                return await message.channel.send(f"{message.author.mention} | URLs aren't allowed.")

        if "discord.gg" in message.content.lower():
            try:
                await message.delete()
            except:
                return await message.channel.send(f"{message.author.mention} | Advertisements aren't allowed.")
            
        if "discord.com" in message.content.lower():
            try:
                await message.delete()
            except:
                return await message.channel.send(f"{message.author.mention} | Advertisements aren't allowed.")

        try:
            await asyncio.sleep(0.1) #i don't what its doig here lol
            await message.delete()

        except:
            return await message.channel.send(f"{emote.xmark} | World-chat requires `manage_messages` permissions to function properly.")

        for hook in self.bot.mwebhooks:
            try:
                async def send_webhook():
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(
                            f"{hook}", adapter=AsyncWebhookAdapter(session))

                        await webhook.send(content=message.clean_content, username=message.author.name+"#"+message.author.discriminator, avatar_url=message.author.avatar_url)

                await send_webhook()
            except:
                continue


def setup(bot):
    bot.add_cog(MessageEvents(bot))
