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
from discord.ext.commands.core import command
import config
from utils import emote
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True, manage_webhooks=True, manage_roles=True)
    async def setup(self, ctx):
        """Setup world chat in your guild"""
        channel = discord.utils.get(ctx.guild.channels, name="world-chat")
        if channel != None:
            return await ctx.send(f"{emote.xmark} | You already have {channel.mention}")

        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, read_message_history=True),

            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True
                                                  )
        }
        channel = await guild.create_text_channel('world-chat', topic="Don't rename this channel to keep talking.", overwrites=overwrites)

        try:
            hook = await channel.create_webhook(name="World-Chat", avatar=await ctx.me.avatar_url.read())
        except:
            await ctx.send(f"{emote.xmark} | I don't have permission to create webhooks.")
            return await channel.delete()

        wcignore = discord.utils.get(ctx.guild.roles, name="wc-ignore")
        if not wcignore:
            wcignore = await ctx.guild.create_role(name="wc-ignore", mentionable=False, reason="For world-chat!")

        records = await self.bot.db.fetchval("SELECT webhook FROM guildconfig WHERE guild_id = $1", ctx.guild.id)
        if records:
            self.bot.mwebhooks.remove(records)
            await self.bot.db.execute("UPDATE guildconfig SET webhook = $2 WHERE guild_id = $1", ctx.guild.id, hook.url)
            self.bot.mwebhooks.append(hook.url)
        if not records:
            await self.bot.db.execute("UPDATE guildconfig SET webhook = $2 WHERE guild_id = $1", ctx.guild.id, hook.url)
            self.bot.mwebhooks.append(hook.url)

        em = discord.Embed(color=self.bot.color,
                           title="Welcome To World Chat!")
        em.add_field(name=f"By using {channel.name}, you agree to following rules:",
                     value="`1.`You will not text anything that could hurt someone's sentiments. By this I mean talks related to racism, sex, color, etc.\n`2.`You will not send any type of invite or other URLs.\n`3.`You will not spam random stuff with this.\n\n`Note:` Breaking the rules is a punishable offence and can get you a lifetime ban from using the bot.")
        pin = await channel.send(embed=em)
        await pin.pin()

        m = discord.Embed(color=self.bot.color)
        m.add_field(name='World Chat created!',
                    value=f"Sweet! {channel.mention} has been set up, now the users in your server can use this feature to talk to people from another servers. I've created a role {wcignore.mention} in case needed.Also, be weary when working with world-chat, I suggest not editing anything let the defaults stay.Also, if you find any bugs or have any suggestions then feel free to hit us up on [here]({config.support_server})")
        await ctx.send(embed=m)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        """Disable world chat in your guild"""
        records = await self.bot.db.fetchval("SELECT webhook FROM guildconfig WHERE guild_id = $1", ctx.guild.id)
        if not records:
            return await ctx.send(f"{emote.xmark} | World Chat is already disabled.")

        self.bot.mwebhooks.remove(records)
        await self.bot.db.execute("UPDATE guildconfig SET webhook = Null WHERE guild_id = $1", ctx.guild.id)
        return await ctx.send(f"{emote.check} | World-Chat Turned Off.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        """Set bot's prefix for the guild"""
        self.bot.prefixes[ctx.guild.id] = prefix
        records = await self.bot.db.execute("UPDATE guildconfig SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
        await ctx.send(f"{emote.check} | New guild prefix is **`{prefix}`**")


def setup(bot):
    bot.add_cog(Setup(bot))
