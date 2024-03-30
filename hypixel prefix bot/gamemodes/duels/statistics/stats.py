from discord.ext import commands
from config import colors

class getstats(commands.Cog):

    def getduelsstats(self,info):

        modes = {
            '': '',
            'Blitz': 'blitz_duel_',
            'Bow': 'bow_duel_',
            'TNT': 'bowspleef_duel_',
            'Boxing': 'boxing_duel_',
            'Bridge': ['bridge_duel_', 'bridge_doubles_', 'bridge_threes_', 'bridge_four_', 'bridge_2v2v2v2_', 'bridge_3v3v3v3_', 'capture_threes_'],
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

        modews = {
            '': '',
            'Bow': 'bow',
            'Blitz': 'blitz',
            'TNT': 'tnt_games',
            'Boxing': 'boxing',
            'Bridge': 'bridge',
            'Classic': 'classic',
            'Combo': 'combo',
            'MW': 'mega_walls',
            'NoDebuff': 'no_debuff',
            'OP': 'op',
            'Parkour': 'parkour',
            'SkyWars': 'skywars',
            'Sumo': 'sumo',
            'UHC': 'uhc'
        }
        

        score = {}
        for title, mode in modes.items():
            try:
                match title:
                    case 'Bridge' | "MW" | "SkyWars" | "OP" | "UHC":
                        mode_wins = sum([info['player']['stats']['Duels'].get(f'{m}wins', 0) for m in mode])
                        mode_losses = sum([info['player']['stats']['Duels'].get(f'{m}losses', 0) for m in mode])
                        mode_kills = sum([info['player']['stats']['Duels'].get(f'{m}kills', 0) for m in mode])
                        mode_deaths = sum([info['player']['stats']['Duels'].get(f'{m}deaths', 0) for m in mode])

                    case _:
                        wins_key = f'{mode}wins'
                        losses_key = f'{mode}losses'
                        kills_key = f'{mode}kills'
                        deaths_key = f'{mode}deaths'
                        mode_wins = info['player']['stats']['Duels'].get(wins_key, 0)
                        mode_losses = info['player']['stats']['Duels'].get(losses_key, 0)
                        mode_kills = info['player']['stats']['Duels'].get(kills_key, 0)
                        mode_deaths = info['player']['stats']['Duels'].get(deaths_key, 0)
            
                getws = modews.get(title)
                if title == "":
                    ws_key = "current_winstreak"
                    bws_key = "best_overall_winstreak"
                else:
                    ws_key = f'current_{getws}_winstreak'
                    bws_key = f'best_{getws}_winstreak'
                
                mode_ws = info['player']['stats']['Duels'].get(ws_key, 0)
                mode_bws = info['player']['stats']['Duels'].get(bws_key, 0)

            except KeyError:
                mode_wins = 0
                mode_losses = 0
                mode_kills = 0
                mode_deaths = 0
                mode_ws = 0
                mode_bws = 0
                
            score[title] = [
                mode_wins, 
                mode_losses, 
                mode_kills, 
                mode_deaths,
                mode_ws,
                mode_bws
            ]
           
        return score
        
        
    def ttitles(self,info):
        
        score = self.getduelsstats(info)
        
      
        titles = dict(sorted(score.items(), key=lambda item: item[1][0], reverse=True))
        result = []
        
        for mode,(wins, losses, kills, deaths, ws, bws) in titles.items():
            
            title, numeral, color, stroke, req, reqwins, nextnumeral,nextcolor = self.winsreq(wins,mode)  
            title = (f'{mode} {title}')
            title_info = {
            "gamemode": mode,
            "title": title.strip(),
            "wins": int(wins),
            "losses": int(losses),
            "kills": int(kills),
            "deaths": int(deaths),
            "winstreak": int(ws),
            "best_winstreak": int(bws),
            "numeral": numeral,
            "color": color,
            "req": req,
            "stroke": stroke,
            "reqwins": reqwins,
            "next": nextnumeral,
            "nextcolor": nextcolor
            }

            result.append(title_info) 
        return result
        
    def winsreq(self, wins, mode):

        if mode == "":
            try:
                wins /= 2
            except ZeroDivisionError:
                wins = 0

        if wins < 49:
            minimal = 0
            title = "None"
            req = 50
            numeral = 1 + (wins - 0) // req
            color = colors['gray']
            nextcolor = colors['dark_gray']
            stroke = 0
        elif 50 <= wins < 100:
            minimal = 50
            title = 'Rookie'
            req = 10
            numeral = 1 + (wins - 50) // req
            color = colors['dark_gray']
            nextcolor = colors['white']
            stroke = 0
        elif wins < 250:
            minimal = 100
            title = 'Iron'
            req = 30
            numeral = 1 + (wins - 100) // req
            color = colors['white']
            nextcolor = colors['gold']
            stroke = 0
        elif wins < 500:
            minimal = 250
            title = 'Gold'
            req = 50
            numeral = 1 + (wins - 250) // req
            color = colors['gold']
            nextcolor = colors['dark_aqua']
            stroke = 0
        elif wins < 1000:
            minimal = 500
            title = 'Diamond'
            req = 100
            numeral = 1 + (wins - 500) // req
            color = colors['dark_aqua']
            nextcolor = colors['dark_green']
            stroke = 0
        elif wins < 2000:
            minimal = 1000
            title = 'Master'
            req = 200
            numeral = 1 + (wins - 1000) // req
            color = colors['dark_green']
            nextcolor = colors['dark_red']
            stroke = 0
        elif wins < 5000:
            minimal = 2000
            title = 'Legend'
            req = 600
            numeral = 1 + (wins - 2000) // req
            color = colors['dark_red']
            nextcolor = colors['yellow']
            stroke = 2
        elif wins < 10000:
            minimal = 5000
            title = 'Grandmaster'
            req = 1000
            numeral = 1 + (wins - 5000) // req
            color = colors['yellow']
            nextcolor = colors['dark_purple']
            stroke = 2
        elif wins < 25000:
            minimal = 10000
            title = 'Godlike'
            req = 3000
            numeral = 1 + (wins - 10000) // req
            color = colors['dark_purple']
            nextcolor = colors['aqua']
            stroke = 2
        elif wins < 50000:
            minimal = 25000
            title = 'CELESTIAL'
            req = 5000
            numeral = 1 + (wins - 25000) // req
            color = colors['aqua']
            nextcolor = colors['pink']
            stroke = 2
        elif wins < 100000:
            minimal = 50000
            title = 'DIVINE'
            req = 10000
            numeral = 1 + (wins - 50000) // req
            color = colors['pink']
            nextcolor = colors['red']
            stroke = 2
        else:
            minimal = 100000
            title = 'ASCENDED'
            req = 10000
            numeral = 1 + (wins - 100000) // req
            color = colors['red']
            nextcolor = colors['red']
            stroke = 2

        if title == "ASCENDED":
            numeral = min(max(numeral, 1), 50)
        else:
            numeral = min(max(numeral, 1), 5)

        if numeral == 5 and title != "ASCENDED":
            nextnumeral = 1
            nextcolor = nextcolor
        else:
            nextnumeral = numeral + 1
            nextcolor = color

        if mode == '':
            neededwins = (req*2) * numeral + (minimal*2) - (wins*2)
        else:
            neededwins = req * numeral + minimal - wins

        reqwins = int(neededwins)
        numeral = self.convert(int(numeral))
        nextnumeral = self.convert(int(nextnumeral))


        return title, numeral, color, stroke, req, reqwins, nextnumeral, nextcolor
        

    def convert(self,n):
        val = [50, 40, 10, 9, 5, 4, 1]
        syms = ['L', 'XL', 'X', 'IX', 'V', 'IV', 'I']

        result = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                result += syms[i]
                n -= val[i]
            i += 1
        
        return result


async def setup(bot):
    await bot.add_cog(getstats(bot))