import discord
from discord.ext import commands, tasks
import config
from utils import emote
import aiohttp
from discord import Webhook, AsyncWebhookAdapter
from discord.ext.commands import errors


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanup.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f" -------------------------------------")
        print(f"Logging In---------------------------------")
        print(f"Logged In as: {self.bot.user.name}({self.bot.user.id})")
        print(f"Connected Guilds:", len(self.bot.guilds))
        print(f"Connected Users", len(self.bot.users))
        self.bot.load_extension('jishaku')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="w!help | w!setup"))

        async def log_webhook():
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    f"{config.host_logs}", adapter=AsyncWebhookAdapter(session))
                await webhook.send("World-Chat just logged in.")

        await log_webhook()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        prefix = 'w!'
        self.bot.prefixes[guild.id] = prefix
        record = await self.bot.db.fetchrow("SELECT * FROM guildconfig WHERE guild_id = $1", guild.id)
        if not record:
            await self.bot.db.execute("INSERT INTO guildconfig (guild_id , prefix) VALUES ($1,$2)", guild.id, "w!")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        record = await self.bot.db.fetchrow("SELECT * FROM guildconfig WHERE guild_id = $1", guild.id)
        if record != None:
            await self.bot.db.execute("DELETE from guildconfig WHERE guild_id = $1", guild.id)

    @tasks.loop(minutes=1)
    async def cleanup(self):
        await self.bot.wait_until_ready()
        record = await self.bot.db.fetch("SELECT * FROM guildconfig")
        glist = []
        for r in record:
            gl = r['guild_id']
            glist.append(gl)

        for g in self.bot.guilds:
            if not g.id in glist:
                await self.bot.db.execute("INSERT INTO guildconfig (guild_id , prefix) VALUES ($1,$2)", g.id, "w!")

    def cog_unload(self):
        self.cleanup.cancel()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if hasattr(ctx.command, 'on_error'):
            return

        elif isinstance(err, errors.MissingRequiredArgument):
            await ctx.send(f'{emote.xmark} | You missed the `{err.param.name}` argument.')
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(
                ctx.command)
            return await ctx.send_help(helper)

        elif isinstance(err, commands.BadArgument):

            if isinstance(err, commands.MessageNotFound):
                await ctx.send(f'{emote.xmark} | A message for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.MemberNotFound):
                await ctx.send(f'{emote.xmark} | A member for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.UserNotFound):
                await ctx.send(f'{emote.xmark} | A user for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.ChannelNotFound):
                await ctx.send(f'{emote.xmark} | A channel/category for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.RoleNotFound):
                await ctx.send(f'{emote.xmark} | A role for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.EmojiNotFound):
                await ctx.send(f'{emote.xmark} | An emoji for the argument `{err.argument}` was not found.')
            elif isinstance(err, commands.ChannelNotReadable):
                await ctx.send(f'{emote.xmark} | I do not have permission to read the channel `{err.argument}`')
            elif isinstance(err, commands.PartialEmojiConversionFailure):
                await ctx.send(f'{emote.xmark} | The argument `{err.argument}` did not match the partial emoji format.')
            elif isinstance(err, commands.BadInviteArgument):
                await ctx.send(f'{emote.xmark} | The invite that matched that argument was not valid or is expired.')
            elif isinstance(err, commands.BadBoolArgument):
                await ctx.send(f'{emote.xmark} | The argument `{err.argument}` was not a valid True/False value.')
            elif isinstance(err, commands.BadColourArgument):
                await ctx.send(f'{emote.xmark} | The argument `{err.argument}` was not a valid colour.')

            else:
                helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(
                    ctx.command)
                return await ctx.send_help(helper)

        elif isinstance(err, commands.CommandNotFound):
            return

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"{emote.xmark} | This command is on cooldown. Try again in {err.retry_after:.2f} seconds.")
            return

        elif isinstance(err, commands.NoPrivateMessage):
            return

        elif isinstance(err, commands.BotMissingPermissions):
            permissions = '\n'.join(
                [f'> {permission}' for permission in err.missing_perms])
            message = f'{emote.xmark} | I am missing **`{permissions}`** permissions to run the command `{ctx.command}`.\n'
            try:
                await ctx.send(message)
            except discord.Forbidden:
                try:
                    await ctx.author.send(f"Hey It looks like, I can't send messages in that channel.\nAlso I am misssing **`{permissions}`** permissions to run the command.")
                except discord.Forbidden:
                    pass
            return

        elif isinstance(err, commands.CheckFailure):
            return

        elif isinstance(err, discord.Forbidden):
            return

        elif isinstance(err, errors.CommandInvokeError):
            return

        else:
            return


def setup(bot):
    bot.add_cog(Events(bot))
