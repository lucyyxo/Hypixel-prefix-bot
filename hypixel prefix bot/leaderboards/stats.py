from discord.ext import commands
from config import duelslbpath, API_KEY, bwlbpath, swlbpath
import json, os, discord, asyncio
from api.uuid import playerinfo
from gamemodes.duels.statistics.stats import getstats
from player.main import General
from gamemodes.bedwars.stats import getbwstats
from gamemodes.skywars.stats import getswstats

class LBstats(commands.Cog):

    def __init__(self, bot):

        self.api = playerinfo(bot)
        self.stats = getstats(bot)
        self.rank = General(bot)
        self.bwstats = getbwstats(bot)
        self.swstats = getswstats(bot)

    async def getstats(self, ctx, info, guildinfo, gamemode):

        guildmembers = info["guild"]["members"]
        
        match gamemode:
            case "Duels":
                filepath = f'{duelslbpath}/{guildinfo["id"]}.json' 
            case "Bedwars":
                filepath = f'{bwlbpath}/{guildinfo["id"]}.json' 
            case "SkyWars":
                filepath = f'{swlbpath}/{guildinfo["id"]}.json'  

        guilddata = {}

        if not os.path.isfile(filepath):
            
            await self.embed(ctx, guildinfo, gamemode)
            
            for display in guildmembers:

                uuid = display['uuid']
                url = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
                await asyncio.sleep(0.1)
                info = await self.api.info(ctx, url, username=uuid)
                rank = self.rank.rank(info)

                match gamemode:
                    case "Duels":
                        try:
                            stats = self.stats.getduelsstats(info)
                        except Exception:
                            continue
                    case "Bedwars":
                        try:
                            bwstats = self.bwstats.getstats(info)
                        except Exception:
                            continue
                        stats = {}
                        for mode, bwmodestats in bwstats.items():
                            final_kills = bwmodestats['final_kills']
                            final_deaths = bwmodestats['final_deaths']
                            stats[mode] = [final_kills, final_deaths]
                    case "SkyWars":
                        try:
                            swstats = self.swstats.getstats(info)
                        except Exception:
                            continue
                        stats = {}
                        for mode, swmodestats in swstats.items():
                            kills = swmodestats['kills']
                            deaths = swmodestats['deaths']
                            stats[mode] = [kills, deaths]

                guilddata[uuid] = ({"rank": rank, "stats": stats})
                
            with open(filepath, 'w') as file:
                json.dump(guilddata, file, indent=1)
        
        else:
            return True

    async def embed(self, ctx, guildinfo, gamemode):

        embed = discord.Embed(
        title='Gathering Information',
        description=f'Fetching all information for {guildinfo["name"]}. This may take a while.\n If you want to update stats, please use ".{gamemode} ign".\n The Bot will ping you once its done.\n If you get no result within 5 minutes please try again!',
        color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LBstats(bot))