from colorama import Fore, init, Style
init(autoreset=True)


async def cache(bot):
    try:
        bot.mwebhooks = []
        results = await bot.db.fetch("SELECT webhook FROM guildconfig")
        for r in results:
            hook = r["webhook"]
            bot.mwebhooks.append(hook)

        print(Fore.GREEN + f'[Cache] Messages loaded!')
    except:
        print(Fore.RED + f'[Cache] Unable to load Messages!')

    try:
        bot.prefixes = {}
        prefixes = await bot.db.fetch("SELECT * FROM guildconfig")
        for res in prefixes:
            bot.prefixes[res['guild_id']] = res['prefix']
        print(Fore.GREEN + f'[Cache] Prefixes loaded!')

    except:
        print(Fore.RED + f'[Cache] Unable to load Prefixes!')
