from discord.ext import commands
from config import colors

class getswstats(commands.Cog):

    def formatted_star(self,star):
        throwout = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','l','r','§']
        for substring in throwout:
            star = star.replace(substring, "")
        return star
        
    def sw_xp_to_lvl(self,xp):
        xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
        if xp >= 15000:
            return (xp - 15000) / 10000 + 12
        else:
            for i in range(len(xps)):
                if xp < xps[i]:
                    return i + float(xp - xps[i-1]) / (xps[i] - xps[i-1])
        
    def neededxp(self,level):
        match int(level):
            case 1:
                req = 20
            case 2:
                req = 50
            case 3:
                req = 80
            case 4:
                req = 100
            case 5:
                req = 250
            case 6:
                req = 500
            case 7:
                req = 1000
            case 8:
                req = 1500
            case 9:
                req = 2500
            case 10:
                req = 4000
            case 11:
                req = 5000
            case _:
                req = 10000
        return req
    
    def swstats(self, info):
        
        try:
            xp = info['player']['stats']['SkyWars']['skywars_experience']
            level = self.sw_xp_to_lvl(xp)
        except KeyError:
            level = 0

        star = self.formatted_star(info['player']['stats']['SkyWars']['levelFormatted'])

        reqxp = self.neededxp(level)
        percentage = (level * 100) % 100 / 100
        needed_xp = int(round(reqxp*(percentage*100) / 100))

        level = int(level)

        color = self.swcolors(level)
        nextlevelcolor = self.swcolors(level=level+1)
        gamemode = self.getstats(info)

        stats = {
            "level": level,
            "star": f'[{level}{star}]',
            "nextstar": f'[{level+1}{star}]',
            "percentage": round(percentage,2),
            "req": f'{needed_xp:.0f}/{reqxp} [{percentage*100:.2f}%]',
            "color": color,
            "nextcolor": nextlevelcolor,
            "gamemode": gamemode
        }
        return stats

    def getstats(self, info):

        modes = {
            "": "",
            "Solo": "solo",
            "Doubles": "team",
            "Ranked": "ranked",
            "Mega": "mega"
        }

        swstats = {}

        for title, mode_info in modes.items():
            stats = {}
            player_stats = info['player']['stats']['SkyWars']
            for stat_key in ["wins", "losses", "kills", "deaths", "assists", "bow_kills", "time_played", "heads", "heads_eww", "heads_yucky", "heads_meh",
                            "heads_decent", "heads_salty", "heads_tasty", "heads_succulent", "heads_sweet", "heads_divine", "heads_heavenly"]:
                if title == "":
                    stat_value = stat_key
                else:
                    stat_value = f"{stat_key}_{mode_info}"
                
                stats[stat_key] = player_stats.get(stat_value, 0)
            
            playtime = self.getplaytime(seconds=stats["time_played"])
            stats["time_played"] = playtime
            
            stat_key = "activeKit"
            if title == "":
                mode_info = "SOLO"
            elif title == "Ranked":
                mode_info ="RANKED"
            elif title == "Mega":
                mode_info = "MEGA"
            else:
                mode_info = "SOLO" if mode_info == "solo" else "TEAMS"
                
            stat_value = f"{stat_key}_{mode_info}"
            stats[stat_value] = player_stats.get(stat_value, "random")
            activekit = stats[stat_value].split("_")[-1]
            stats["activeKit"] = activekit.capitalize()
            stats = {key: value for key, value in stats.items() if key not in ['activeKit_SOLO', 'activeKit_TEAMS', "activeKIT_RANKED", 'activeKitM_MEGA']}
            swstats[title] = stats

        return swstats
    
    def swcolors(self, level):

        
        level_colors = {
        (0, 4): ["gray"] * 4,
        (5, 9): ["white"] * 4,
        (10, 14): ["gold"] * 5,
        (15, 19): ["aqua"] * 5,
        (20, 24): ["dark_green"] * 5,
        (25, 29): ["dark_aqua"] * 5,
        (30, 34): ["dark_red"] * 5,
        (35, 39): ["pink"] * 5,
        (40, 44): ["blue"] * 5,
        (45, 49): ["dark_purple"] * 5,
        (50, 54): ["red", "gold", "yellow", "green", "aqua"],
        (55, 59): ["gray", "white", "white", "white","gray"],
        (60, 64): ["dark_red", "red", "red", "red", "dark_red"],
        (65, 69): ["red", "white", "white", "white", "red"],
        (70, 74): ["yellow", "gold", "gold", "gold", "yellow"],
        (75, 79): ["white", "blue", "blue", "blue" "white"],
        (80, 84): ["white", "aqua", "aqua", "aqua", "white"],
        (85, 89): ["white", "dark_aqua", "dark_aqua", "dark_aqua", "white"],
        (90, 94): ["green", "dark_aqua", "dark_aqua", "dark_aqua", "green"],
        (95, 99): ["red", "yellow", "yellow", "yellow", "red"],
        (100, 104): ["blue", "dark_blue", "dark_blue", "dark_blue", "dark_blue", "blue"],
        (105, 109): ["gold", "dark_red", "dark_red", "dark_red", "dark_red", "gold"],
        (110, 114): ["dark_blue", "aqua", "aqua", "aqua", "aqua", "dark_blue"],
        (115, 119): ["dark_gray", "gray", "gray", "gray", "gray", "dark_gray"],
        (120, 124): ["pink", "dark_purple", "dark_purple", "dark_purple", "dark_purple", "pink"],
        (125, 129): ["white", "yellow", "yellow", "yellow", "yellow", "white"],
        (130, 134): ["red", "yellow", "yellow", "yellow", "yellow", "red"],
        (135, 139): ["gold", "red", "red", "red", "red", "gold"],
        (140, 144): ["green", "red", "red", "red", "red", "green"],
        (145, 149): ["green", "aqua", "aqua", "aqua", "aqua", "green"],
        (150, 1000): ["red", "gold", "yellow", "green", "aqua", "pink", "dark_purple", "red"]
        }
        
        for (low, high), color_names in level_colors.items():
            if low <= level <= high:
                return [colors[color_name] for color_name in color_names]
    
            
    def getplaytime(self,seconds):

        seconds_per_minute = 60
        minutes_per_hour = 60
        hours_per_day = 24
        days_per_month = 30
        days_per_year = 365.25  

        years = seconds // (seconds_per_minute * minutes_per_hour * hours_per_day * days_per_year)
        seconds = seconds % (seconds_per_minute * minutes_per_hour * hours_per_day * days_per_year)
        months = seconds // (seconds_per_minute * minutes_per_hour * hours_per_day * days_per_month)
        seconds = seconds % (seconds_per_minute * minutes_per_hour * hours_per_day * days_per_month)
        days = seconds // (seconds_per_minute * minutes_per_hour * hours_per_day)
        seconds = seconds % (seconds_per_minute * minutes_per_hour * hours_per_day)
        hours = seconds // (seconds_per_minute * minutes_per_hour)
        minutes = (seconds % (seconds_per_minute * minutes_per_hour)) // seconds_per_minute
        seconds = seconds % seconds_per_minute
        playtime = [f'{years}y',f'{months}mo',f'{days}d',f'{hours}h',f'{minutes}m',f'{seconds}s']
        non_zero_data = [item for item in playtime if not item.startswith("0")]

        sorted_data = sorted(non_zero_data, key=playtime.index)

        if sorted_data == []:
            highest_units = "0s"
        elif len(sorted_data) >= 2:
            highest_units = sorted_data[:2]
        else:
            highest_units = sorted_data
        
        if highest_units == "0s":
            playtime = ''.join([element.replace('.0', '') for element in highest_units]) 
        else:
            playtime = ', '.join([element.replace('.0', '') for element in highest_units])
        
        return playtime

async def setup(bot):
    await bot.add_cog(getswstats(bot))
        

