from discord.ext import commands
from config import colors
import math

class General(commands.Cog):

    def monthlycolor(self,info):
        try:
            plusplus_color = info['player']['monthlyRankColor']
            
            match plusplus_color:
                case "GOLD":
                    color = "gold"
                case "AQUA":
                    color = "aqua"
        except KeyError:
            color = "aqua"

        return color

    def pluscolor(self,info):

        try:
            get_plus_color = info['player']['rankPlusColor']
        
            match get_plus_color:
                case 'RED':
                    color = 'red'
                case 'GOLD':
                    color = 'gold'
                case 'GREEN':
                    color = 'green'
                case 'YELLOW':
                    color = 'yellow'
                case 'LIGHT_PURPLE':
                    color = 'pink'
                case 'WHITE':
                    color = 'white'
                case 'BLUE':
                    color = 'blue'
                case 'DARK_GREEN':
                    color = 'dark_green'
                case 'DARK_RED':
                    color = 'dark_red'
                case 'DARK_AQUA':
                    color = 'dark_aqua'
                case 'DARK_PURPLE':
                    color = 'dark_purple'
                case 'DARK_GRAY':
                    color = 'dark_gray'
                case 'DARK_BLUE':
                    color = 'dark_blue'
                case 'BLACK':
                    color = 'black'
        except KeyError:
            color = 'red'

        return color

    def formatrank(self,rank,info):

        match rank:
            
            case "DEMON":
                rank = "[DEMON]"
                rankcolor = colors['white'], colors['white'], colors['white'], colors['white'], colors['white'], colors['white'], colors['white']
            case 'FROG':
                rank = '[FROG]'
                rankcolor = colors['green'], colors['green'], colors['green'], colors['green'], colors['green'], colors['green']
            case "VIP":
                rank = "[VIP]"
                rankcolor = colors['green'], colors['green'], colors['green'], colors['green'], colors['green']
            case "VIP_PLUS":
                rank = "[VIP+]"
                rankcolor = colors['green'], colors['green'], colors['green'], colors['green'], colors['gold'], colors['green']
            case "MVP":
                rank = "[MVP]"
                rankcolor = colors['aqua'], colors['aqua'], colors['aqua'], colors['aqua'], colors['aqua']
            case "MVP_PLUS":
                rank = "[MVP+]"
                pluscolor = self.pluscolor(info)
                rankcolor = colors['aqua'], colors['aqua'], colors['aqua'], colors['aqua'], colors[pluscolor], colors['aqua']
            case "SUPERSTAR":
                rank = "[MVP++]"
                ppcolor = self.monthlycolor(info)
                pluscolor = self.pluscolor(info)
                rankcolor = colors[ppcolor], colors[ppcolor], colors[ppcolor], colors[ppcolor], colors[pluscolor], colors[pluscolor], colors[ppcolor]
            case "YOUTUBER":
                rank = "[YOUTUBE]"
                rankcolor = colors['red'], colors['white'], colors['white'], colors['white'], colors['white'], colors['white'], colors['white'], colors['white'], colors['red']
            case "GAME_MASTER":
                rank = "[GM]"
                rankcolor = colors['dark_green'], colors['dark_green'], colors['dark_green'], colors['dark_green']
            case "ADMIN":
                rank = "[ADMIN]"
                rankcolor = colors['red'], colors['red'], colors['red'], colors['red'], colors['red'] ,colors['red'] ,colors['red']
            case "§d[PIG§b+++§d]":
                rank = "[PIG+++]"
                rankcolor = colors['pink'], colors['pink'], colors['pink'], colors['pink'], colors['aqua'], colors['aqua'], colors['aqua'], colors['pink']
            case "§6[MOJANG]":
                rank = '[MOJANG]'
                rankcolor = colors['gold'], colors['gold'], colors['gold'], colors['gold'], colors['gold'], colors['gold'], colors['gold'], colors['gold']
            case "§c[OWNER]":
                rank = "[OWNER]"
                rankcolor = colors['red'], colors['red'], colors['red'] ,colors['red'] ,colors['red'], colors['red'], colors['red']
            case _:
                rank = ""
                rankcolor = colors['gray'], colors['gray']

        return rank, rankcolor


    def rank(self,info):
        
        try:
            rank = info['player']['prefix']
        except KeyError:

            if info['player']['uuid'] == "8496067cb5444596b6682d233665b916":
                rank = "DEMON"
            elif info ['player']['uuid'] == "5a6d75d91b4043d1af38ee40673c84f1":
                rank = 'FROG'
            elif "rank" in info["player"] and not info["player"]["rank"] == "NORMAL":
                rank = info["player"]["rank"]
            elif "monthlyPackageRank" in info["player"] and not info["player"]["monthlyPackageRank"] == "NONE":
                rank = info["player"]["monthlyPackageRank"]
            elif "newPackageRank" in info["player"]:
                rank = info["player"]["newPackageRank"]
            elif "packageRank" in info["player"]:
                rank = info["player"]["packageRank"]
            else: 
                rank = None 
    
        formatrank,rankcolor = self.formatrank(rank,info)
        displayname = info['player']['displayname']
        
        formatranks = {
            "rank": formatrank.strip(),
            "color": [color['hex'] for color in rankcolor],
            "shadow": [color['rgb'] for color in rankcolor], 
            "display": displayname
            }
        
        return formatranks
    
    def guildlevel(self,guildLevel):

        if guildLevel < 100000:
            guildLevel = 0
        elif guildLevel < 250000: 
            guildLevel = 1
        elif guildLevel < 500000: 
            guildLevel = 2
        elif guildLevel < 1000000: 
            guildLevel = 3
        elif guildLevel < 1750000:
            guildLevel = 4
        elif guildLevel < 2750000:
            guildLevel = 5
        elif guildLevel < 4000000:
            guildLevel = 6
        elif guildLevel < 5500000:
            guildLevel = 8
        elif guildLevel < 7500000:
            guildLevel = 9
        elif guildLevel < 15000000:
            guildLevel = (math.floor((guildLevel - 7500000) / 2500000) + 9)
        else:
            guildLevel = (math.floor((guildLevel - 15000000) / 3000000) + 12)

        return guildLevel

    def guild(self,guildinfo):
        
               
        if 'guild' in guildinfo and guildinfo['guild'] is not None:
            guildid = guildinfo['guild']['_id']
            
            try:
                guildtag = guildinfo['guild']['tag']
            except KeyError:
                guildtag = ""
    
            try:
                guildtagcolor = guildinfo['guild']['tagColor']
                        
                if guildtagcolor == 'GRAY':
                    guildtagcolor = colors['gray']
                elif guildtagcolor == 'DARK_AQUA':
                    guildtagcolor = colors['dark_aqua']
                elif guildtagcolor == 'DARK_GREEN':
                    guildtagcolor = colors['dark_green']
                elif guildtagcolor == 'YELLOW':
                    guildtagcolor = colors['yellow']
                elif guildtagcolor == 'GOLD':
                    guildtagcolor = colors['gold']

            except KeyError:
                guildtagcolor = colors['gray']
            
            guildname = guildinfo['guild']['name']
            try:
                guildLevel = guildinfo['guild']['exp']
            except KeyError:
                guildLevel = 0
            formatguildlevel = self.guildlevel(guildLevel)

        else:
            guildid = ""
            guildtag = ""
            guildtagcolor = ""
            guildname = ""
            formatguildlevel = ""
        
        guildinformation = {
            "tag": '[' + ''.join(guildtag) + ']',
            "tagcolor": guildtagcolor,
            "name": guildname,
            "lvl": formatguildlevel,
            "id": guildid 
        }
        
        return guildinformation


async def setup(bot):
    await bot.add_cog(General(bot))