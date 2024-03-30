from discord.ext import commands
from config import colors

class getprefixstats(commands.Cog):

    def getduelsstats(self,info):

        modes = {
            '': '',
            'Blitz': 'blitz_duel_',
            'Bow': 'bow_duel_',
            'TNT': 'bowspleef_duel_',
            'Boxing': 'boxing_duel_',
            'Bridge': 'bridge_',
            'Classic': 'classic_duel_',
            'Combo': 'combo_duel_',
            'MW': ['mw_duel_', 'mw_doubles_'],
            'NoDebuff': 'potion_duel_',
            'OP': ['op_duel_', 'op_doubles_'],
            'Parkour': 'parkour_eight_',
            'SkyWars': ['sw_duel_', 'sw_doubles_'],
            'Sumo': 'sumo_duel_',
            'UHC': ['uhc_duel_', 'uhc_doubles_', 'uhc_four_', 'uhc_meetup_']
        }

        score = {}
        for title, mode in modes.items():
            if title == 'Bridge':
                mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                mode_kills = info['player']['stats']['Duels'].get(f'{mode}kills', 0)
            elif title == 'MW':
                mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                mode_kills = sum([info['player']['stats']['Duels'].get(f'{m}kills', 0) for m in mode])
            elif title == 'UHC':
                mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                mode_kills = sum([info['player']['stats']['Duels'].get(f'{m}kills', 0) for m in mode])
            elif title == 'SkyWars':
                mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                mode_kills = sum([info['player']['stats']['Duels'].get(f'{m}kills', 0) for m in mode])
            elif title == 'OP':
                mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                mode_kills = sum([info['player']['stats']['Duels'].get(f'{m}kills', 0) for m in mode])
            else:
                wins_key = f'{mode}wins'
                kills_key = f'{mode}kills'
                mode_wins = info['player']['stats']['Duels'].get(wins_key, 0)
                mode_kills = info['player']['stats']['Duels'].get(kills_key, 0)
                
            score[title] = [mode_wins, mode_kills]
        
        return score

    
    def getreqs(self,info):

        score = self.getduelsstats(info)
        iconcolors = {}
        colorcolors = {}

        iconreqs = {
            "Combo": (5000, colors["dark_blue"]),
            "Classic": (5000, colors["dark_aqua"]),
            "NoDebuff": (5000, colors["yellow"]),
            "Sumo": (5000, colors["green"]),
            "Parkour": (2500, colors["dark_purple"]),
            "Bow": (5000, colors["white"]),
            "TNT": (5000, colors["dark_red"]),
            "OP": (5000, colors["aqua"]),
            "Boxing": (5000, colors["red"]),
            "Blitz": (5000, colors["blue"]),
            "": (20000, colors["white"])
        }
        
        colorreqs = {
            "": (5000, 1),
            "Boxing": (2500, 0),
            "OP": (2500, 0),
            "UHC": (2500, 1),
            "SkyWars": (2500, 1),
            "Blitz": (2500, 0),
            "Bridge": (2500, 1),
            "MW": (2500, 1),
            "TNT": (2500, 0),
            "Combo": (2500, 0),
            "Parkour": (1000, 0)
        }

        count = 1
        for game_mode, (threshold, color) in iconreqs.items():
            if score[game_mode][0] >= threshold:
                iconcolors[game_mode] = color
                count +=1
            else:
                iconcolors[game_mode] = colors["gray"]
        iconcolors["number"] = count

        count = 1
        for game_mode, (threshold, index) in colorreqs.items():
            if score[game_mode][index] >= threshold:
                colorcolors[game_mode] = 100
                count +=1
            else:
                colorcolors[game_mode] = 15
        colorcolors["number"] = count
        
        return iconcolors, colorcolors
    

async def setup(bot):
    await bot.add_cog(getprefixstats(bot))