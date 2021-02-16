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

hidden_cogs = ('Dev', 'Jishaku', 'Events', 'MessageEvents', 'Meta')


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category'
        })

    async def send_bot_help(self, mapping):
        #seriously I don't know why I chose to harcorde it.
        emb = discord.Embed(title="World Chat help menu", color=discord.Colour(
            0xecd3a1), url=f'{config.bot_invite}')
        emb.add_field(name="Admin Commands",
                      value="`setup`, `disable`, `prefix`", inline=False)
        emb.add_field(name="Everyone Commands",
                      value="`ping`, `botinfo`, `invite`, `source`", inline=False)
        emb.set_footer(
            text=f"Type  {self.clean_prefix}<command> to see more detail on a command")

        await self.context.send(embed=emb)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    def common_command_formatting(self, embed_like, command):
        embed_like.title = self.get_command_signature(command)
        if command.description:
            embed_like.description = f"{command.description}\n\n{command.help}"
        else:
            embed_like.description = command.help or 'No help found...'
        embed_like.add_field(name="Aliases", value=" | ".join(
            [f"`{alias}`" for alias in command.aliases]) if command.aliases else f"`{command.name}`")
        embed_like.add_field(
            name="Usage", value=f"`{self.get_command_signature(command)}`")

    async def send_command_help(self, command):
        embed = discord.Embed(colour=discord.Colour(0xecd3a1))
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, cmd):
        e = discord.Embed(color=discord.Colour(0xecd3a1))
        e.title = f"Category: **{cmd.name}**" + \
            (" | " + '-'.join(cmd.aliases) if cmd.aliases else "")
        e.set_author(name=self.context.guild.me.display_name,
                     url=config.support_server, icon_url=self.context.guild.me.avatar_url)
        e.set_footer(
            text=f"Type {self.clean_prefix}<command name> to get more information.")
        cmds = await self.filter_commands(cmd.commands, sort=True)
        for cmd in cmds:
            e.add_field(name=cmd.name + (" | " + '-'.join(cmd.aliases) if cmd.aliases else ""), value=(
                cmd.short_doc if cmd.short_doc else "No description.") + f"\nUsage: `{self.get_command_signature(cmd)}`", inline=False)
        await self.context.send(embed=e)

    async def send_cog_help(self, cog):

        embed = discord.Embed(title='{0.qualified_name} Commands'.format(
            cog), color=discord.Colour(0xecd3a1))
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=command.name, value=f"{command.short_doc or '...'}\n"
                                                     f"Usage: `{self.get_command_signature(command)}`", inline=False)

        await self.get_destination().send(embed=embed)


class Meta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command


def setup(bot):
    bot.add_cog(Meta(bot))
