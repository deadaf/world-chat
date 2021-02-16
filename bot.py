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
import asyncpg
import traceback
from utils.cache import cache
from discord.ext import commands
from config import *
from discord.flags import MemberCacheFlags

async def get_prefix(bot, message):
    if not message.guild:
        custom_prefix = 'w!'
        return custom_prefix

    try:
        prefix = bot.prefixes[message.guild.id]
        custom_prefix = prefix
        return commands.when_mentioned_or(custom_prefix)(bot, message)

    except TypeError:
        return

intents = discord.Intents.default()
intents.members=True
bot = commands.Bot(command_prefix=get_prefix,
                   chunk_guilds_at_startup=False,
                   member_cache_flags=MemberCacheFlags.from_intents(intents),
                   case_insensitive=True, intents=intents)

bot.color = 0xecd3a1


for e in extensions:
    try:
        bot.load_extension(e)
        print(f'[EXTENSION] {e} was loaded successfully!')
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tbe = "".join(tb) + ""
        print(f'[WARNING] Could not load extension {e}: {tbe}')


async def create_db_pool():
    bot.db = await asyncpg.create_pool(**SQL_INFO)
    print("----------------\nConnected to Database.")

    QUERIES = open('database/migrate.sql', 'r').read()
    await bot.db.execute(QUERIES)
    print("----------------\nDatabase checkup successfull.")

    await cache(bot)

bot.loop.create_task(create_db_pool())
bot.run(token)
