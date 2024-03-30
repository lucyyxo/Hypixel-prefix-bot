from discord.ext import commands
from config import colors

class getbwstats(commands.Cog):
    
    def getExpReq(self,level):
        progress = level % 100
        if progress > 3:
            return 5000

        levels = {
            0: 500,
            1: 1000,
            2: 2000,
            3: 3500,
        }
        return levels[progress]

    def getLevel(self,exp=0):

        prestiges = exp // 487000
        level = prestiges * 100
        remainingExp = exp - prestiges * 487000 

        for i in range(4):
            expForNextLevel = self.getExpReq(i)
            if remainingExp < expForNextLevel:
                break
            level += 1
            remainingExp -= expForNextLevel

        fractional_level = remainingExp / self.getExpReq(level) 
        level += fractional_level
        
        return level

    def bwlevels(self,info):

        try:
            progress = info['player']['stats']['Bedwars']['Experience']
        except KeyError:
            progress = 0
        try:
            level = info['player']['achievements']['bedwars_level']
        except KeyError:
            level = 0

        nextlevel = level + 1
        percentlevel = self.getLevel(progress)
        percentage = (percentlevel * 100) % 100 / 100
        reqmaxxp = self.getExpReq(level)

        needed_xp = round(((percentage*100)*reqmaxxp) / 100,2)
        color = self.getcolors(level)
        nextlevelcolor = self.getcolors(level=nextlevel)
        star = self.getstar(level)
        nextstar = self.getstar(level=nextlevel)
        gamemode = self.getstats(info)    

        
        stats = {
            "level": int(level),
            "star": f'[{level}{star}]',
            "nextstar": f'[{nextlevel}{nextstar}]',
            "percentage": round(percentage,2),
            "req": f'{needed_xp:.0f}/{reqmaxxp} [{percentage*100:.2f}%]',
            "color": color,
            "nextcolor": nextlevelcolor,
            "gamemode": gamemode
        }

        return stats
    
    def getstats(self,info):
    
        modes = {
            "": "",
            "Solo": "eight_one",
            "Doubles": "eight_two",
            "Threes": "four_three",
            "Fours": "four_four",
            "4v4": "two_four",
            "Armed": "eight_two_armed",
            "Castle": "castle",
            "Lucky": "four_four_lucky",
            "Ultimate": "eight_two_ultimate",
            "Underworld": "four_four_underworld",
            "Voidless": "four_four_voidless"
        }

        bwstats = {}

        for title, mode_info in modes.items():
            stats = {}
            player_stats = info['player']['stats']['Bedwars']
            for stat_key in ['final_kills', 'final_deaths', 'wins', 'losses', 'kills', 'deaths', 'beds_broken', 'beds_lost']:
                if title == "":
                    stat_value = f"{stat_key}_bedwars"
                else:
                    stat_value = f"{mode_info}_{stat_key}_bedwars" 
                stats[stat_key] = player_stats.get(stat_value, 0)
            bwstats[title] = stats

        core_stats = {}
        for stat_key in bwstats[""].keys():
            core_stats[stat_key] = bwstats[""][stat_key] - bwstats["4v4"][stat_key]
        bwstats["Core"] = core_stats
        
        return bwstats
    
    def getstar(self, level):

        if level < 1100:
            star = '✫'
        elif level < 2100:
            star = '✪'
        elif level < 3100:
            star = '⚝'
        else:
            star = '✥'

        return star
    
    def getcolors(self, level):

        
        level_colors = {
        (0, 99): ["gray"] * 5,
        (100, 199): ["white"] * 6,
        (200, 299): ["gold"] * 6,
        (300, 399): ["aqua"] * 6,
        (400, 499): ["dark_green"] * 6,
        (500, 599): ["dark_aqua"] * 6,
        (600, 699): ["dark_red"] * 6,
        (700, 799): ["pink"] * 6,
        (800, 899): ["blue"] * 6,
        (900, 999): ["dark_purple"] * 6,
        (1000, 1099): ["red", "gold", "yellow", "green", "aqua", "pink", "dark_purple"],
        (1100, 1199): ["gray", "white", "white", "white", "white", "gray", "gray"],
        (1200, 1299): ["gray", "yellow", "yellow", "yellow", "yellow", "gold", "gray"],
        (1300, 1399): ["gray", "aqua", "aqua", "aqua", "aqua", "dark_aqua", "gray"],
        (1400, 1499): ["gray", "green", "green", "green", "green", "dark_green", "gray"],
        (1500, 1599): ["gray", "dark_aqua", "dark_aqua", "dark_aqua", "dark_aqua", "blue", "gray"],
        (1600, 1699): ["gray", "red", "red", "red", "red", "dark_red", "gray"],
        (1700, 1799): ["gray", "pink", "pink", "pink", "pink", "dark_purple", "gray"],
        (1800, 1899): ["gray", "blue", "blue", "blue", "blue", "dark_blue", "gray"],
        (1900, 1999): ["gray", "dark_purple", "dark_purple", "dark_purple", "dark_purple", "dark_gray", "gray"],
        (2000, 2099): ["dark_gray", "gray", "white", "white", "gray", "gray", "dark_gray"],
        (2100, 2199): ["white", "white", "yellow", "yellow", "gold", "gold", "gold"],
        (2200, 2299): ["gold", "gold", "white", "white", "aqua", "dark_aqua", "dark_aqua"],
        (2300, 2399): ["dark_purple", "dark_purple", "pink", "pink", "gold", "yellow", "yellow"],
        (2400, 2499): ["aqua", "aqua", "white", "white", "gray", "gray", "dark_gray"],
        (2500, 2599): ["white", "white", "green", "green", "dark_green", "dark_green", "dark_green"],
        (2600, 2699): ["dark_red", "dark_red", "red", "red", "pink", "pink", "dark_purple"],
        (2700, 2799): ["yellow", "yellow", "white", "white", "dark_gray", "dark_gray", "dark_gray"],
        (2800, 2899): ["green", "green", "dark_green", "dark_green", "gold", "gold", "yellow"],
        (2900, 2999): ["aqua", "aqua", "dark_aqua", "dark_aqua", "blue", "blue", "dark_blue"],
        (3000, 3099): ["yellow", "yellow", "gold", "gold", "red", "red", "dark_red"],
        (3100, 3199): ["blue", "blue", "aqua", "aqua", "gold", "gold", "yellow"],
        (3200, 3299): ["red", "dark_red", "gray", "gray", "dark_red", "red", "red"],
        (3300, 3399): ["blue", "blue", "blue", "pink", "red", "red", "dark_red"],
        (3400, 3499): ["dark_green", "green", "pink", "pink", "dark_purple", "dark_purple", "dark_green"],
        (3500, 3599): ["red", "red", "dark_red", "dark_red", "dark_green", "green", "green"],
        (3600, 3699): ["green", "green", "green", "aqua", "blue", "blue", "dark_blue"],
        (3700, 3799): ["dark_red", "dark_red", "red", "red", "aqua", "dark_aqua", "dark_aqua"],
        (3800, 3899): ["dark_blue", "dark_blue", "blue", "dark_purple", "dark_purple", "pink", "dark_blue"],
        (3900, 3999): ["red", "red", "green", "green", "dark_aqua", "blue", "blue"],
        (4000, 4099): ["dark_purple", "dark_purple", "red", "red", "gold", "gold", "yellow"],
        (4100, 4199): ["yellow", "yellow", "gold", "red", "pink", "pink", "dark_purple"],
        (4200, 4299): ["dark_blue", "blue", "dark_aqua", "aqua", "white", "gray", "gray"],
        (4300, 4399): ["black", "dark_purple", "dark_gray", "dark_gray", "dark_purple", "dark_purple", "black"],
        (4400, 4499): ["dark_green", "dark_green", "green", "yellow", "gold", "dark_purple", "pink"],
        (4500, 4599): ["white", "white", "aqua", "aqua", "dark_aqua", "dark_aqua", "dark_aqua"],
        (4600, 4699): ["dark_aqua", "aqua", "yellow", "yellow", "gold", "pink", "dark_purple"],
        (4700, 4799): ["white", "dark_red", "red", "red", "blue", "dark_blue", "blue"],
        (4800, 4899): ["dark_purple", "dark_purple", "red", "gold", "yellow", "aqua", "dark_aqua"],
        (4900, 4999): ["dark_green", "green", "white", "white", "green", "green", "dark_green"],
        (5000, 10000): ["dark_red", "dark_red", "dark_purple", "blue", "blue", "dark_blue", "black"]
        }

        for (low, high), color_names in level_colors.items():
            if low <= level <= high:
                return [colors[color_name] for color_name in color_names]

async def setup(bot):
    await bot.add_cog(getbwstats(bot))