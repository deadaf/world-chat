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
