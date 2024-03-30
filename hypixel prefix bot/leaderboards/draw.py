from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import *
import discord, json
from io import BytesIO

class guildimage(commands.Cog):
   
    def topdisplay(self, ctx, guildinfo, gamemode):

        image = Image.open(guild_image)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(mc_font, 60)
        other_font = ImageFont.truetype(mc_special, 45)

        guilddisplay = f'{guildinfo["name"]} {guildinfo["tag"]} Lvl: [{guildinfo["lvl"]}]'

        variables_width = sum([draw.textsize(variable, font=font)[0] for variable in guilddisplay])
        x = (image.width - variables_width) // 2
        y = 30
        
        draw.text((x+15, y+15), guildinfo["name"], font=font, fill=guildinfo["tagcolor"]["rgb"])
        draw.text((x, y), guildinfo["name"], font=font, fill=guildinfo["tagcolor"]["hex"])

        x += draw.textsize(guildinfo["name"], font=font)[0] + 20

        if guildinfo['tag'] != '[]':
           
            symbol_to_font = {
                "✪": other_font,
                "✧": other_font,
                "❤": other_font,
                "✌": other_font,
                "✿": other_font,
                "➊": other_font,
                "✖": other_font,
                "✓": other_font,
                'Θ': other_font
                }
            
            for gtag in guildinfo['tag']:
                symbols = symbol_to_font
                parts = [gtag]

                for part in parts:
                    symbol_font = symbol_to_font.get(part, font)
                    char_width, char_height = symbol_font.getsize(part)

                    if part in symbols:
                        draw.text((x+15, y+40), part, font=symbol_font, fill=guildinfo["tagcolor"]['rgb'])
                        draw.text((x, y+25), part, font=symbol_font, fill=guildinfo["tagcolor"]['hex'])
                    else:
                        draw.text((x+15, y+15), part, font=symbol_font, fill=guildinfo["tagcolor"]['rgb'])
                        draw.text((x, y), part, font=symbol_font, fill=guildinfo["tagcolor"]['hex'])
                        
                    x += char_width

                if part in symbols:
                    x += 15

        x+=30
       
        draw.text((x+15, y+15), "LvL:", font=font, fill="#3F3F3F")
        draw.text((x, y), "LvL:", font=font, fill="#FFFFFF")
        x += draw.textsize("LvL:", font=font)[0] + 20
        draw.text((x+15, y+15), f'[{guildinfo["lvl"]}]', font=font, fill=guildinfo["tagcolor"]["rgb"])
        draw.text((x, y), f'[{guildinfo["lvl"]}]', font=font, fill=guildinfo["tagcolor"]["hex"])

        y = 250
        
        match gamemode:
            case "Duels":
                data = {
                    "pos": (50, y, colors["white"]),
                    "Name": (690, y, colors["white"]),
                    "Wins": (1540, y, colors["green"]),
                    "Losses": (1880, y, colors["red"]),
                    "WLR": (2350, y, colors["gold"])
                }

            case "Bedwars":
                data = {
                    "pos": (50, y, colors["white"]),
                    "Name": (690, y, colors["white"]),
                    "FKills": (1525, y, colors["green"]),
                    "FDeaths": (1870, y, colors["red"]),
                    "FKDR": (2330, y, colors["gold"])
                }
            
            case "SkyWars":
                data = {
                    "pos": (50, y, colors["white"]),
                    "Name": (690, y, colors["white"]),
                    "Kills": (1540, y, colors["green"]),
                    "Deaths": (1880, y, colors["red"]),
                    "KDR": (2350, y, colors["gold"])
                }

        for key, (x, y, color) in data.items():

            draw.text((x+15,y+15), key, font=font, fill=color["rgb"])
            draw.text((x,y), key, font=font, fill=color["hex"])
        

        filepath = f'{cachefile}/{ctx.message.id}.png'
        image.save(filepath)
        return filepath


class drawlb(commands.Cog):

    def generateimage(self, guildimg, guildinfo, mode, start_rank, gamemode):
        
        self.image = Image.open(guildimg)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(mc_font, 80)
        self.other_font = ImageFont.truetype(mc_special, 60)
        self.smallfont = ImageFont.truetype(mc_font, 60)
        self.height, self.width = self.image.size

        self.readdata(guildinfo, mode, start_rank, gamemode)

        buffer = BytesIO()
        self.image.save(buffer, format="PNG")
        buffer.seek(0)
        filename = ('guild.png')
        file = discord.File(buffer, filename=(filename))

        return file

    def readdata(self, guildinfo, mode, start_rank, gamemode):
        
        match gamemode:
            case "Duels":
                filepath = f'{duelslbpath}/{guildinfo["id"]}.json' 
            case "Bedwars":
                filepath = f'{bwlbpath}/{guildinfo["id"]}.json'
            case "SkyWars":
                filepath = f'{swlbpath}/{guildinfo["id"]}.json'

        with open(filepath, "r") as file:
            data = json.load(file)
        
        player_wins = {}

        for uuid, player_data in data.items():

            rank = player_data['rank']
            stats = player_data['stats']

            wins = stats.get(mode, [0, 0])[0]
            losses = stats.get(mode, [0, 0])[1]
            
            player_wins[uuid] = (wins, losses, rank)

        
        sorted_players = sorted(player_wins.items(), key=lambda x: x[1][0], reverse=True)
        
        x = 70
        y = 400
        end_rank = start_rank+9
    
        for player_info, (uuid, (wins, losses, rank)) in enumerate(sorted_players[start_rank - 1:end_rank], start=start_rank):
            wlr = round(wins / max(losses, 1), 2)
            
            poscolor = self.getposcolor(start_rank)
            if start_rank > 9:
                x-=10
                bonus = 40
            else:
                bonus = 0
            
            self.draw.text((x + 15, y + 15), f'#{start_rank}', font=self.smallfont, fill=poscolor["rgb"])
            self.draw.text((x, y), f'#{start_rank}', font=self.smallfont, fill=poscolor["hex"])
            x += self.draw.textsize(f'#{start_rank}', font=self.smallfont)[0] + 125 - bonus

            for i,char in enumerate(rank["rank"]):
                color = rank["color"][i % len(rank["color"])]
                scolor = rank["shadow"][i % len(rank["shadow"])]
                self.draw.text((x+15, y+15), char, font=self.smallfont, fill=scolor)
                self.draw.text((x, y), char, font=self.smallfont, fill=color)
                char_width, char_height = self.smallfont.getsize(char)
                x += char_width
            
            x += 20

            self.draw.text((x + 15, y + 15), rank["display"], font=self.smallfont, fill=rank["shadow"][0])
            self.draw.text((x, y), rank["display"], font=self.smallfont, fill=rank["color"][0])

            color = self.winscolor(wins, mode)
            wins = "{:,}".format(wins)
            x = self.getxcoord(stat=wins, extra=605)
            
            self.draw.text((x+15, y+15), wins, font=self.smallfont, fill=color["rgb"])
            self.draw.text((x, y), wins, font=self.smallfont, fill=color["hex"])


            losses = "{:,}".format(losses)
            x = self.getxcoord(stat=losses, extra=1400)

            self.draw.text((x+15, y+15), losses, font=self.smallfont, fill="#3F3F3F")
            self.draw.text((x, y), losses, font=self.smallfont, fill="#FFFFFF")

            color = self.wlrcolor(wlr)
            wlr = "{:,}".format(wlr)
            x = self.getxcoord(stat=wlr, extra=2200)

            self.draw.text((x+15, y+15), wlr, font=self.smallfont, fill=color["rgb"])
            self.draw.text((x, y), wlr, font=self.smallfont, fill=color["hex"])
            
            start_rank += 1
            y += 150
            x = 75
            
    
    def getposcolor(self, start_rank):

        if start_rank == 1:
            return colors["gold"]
        elif start_rank == 2:
            return colors["gray"]
        elif start_rank == 3:
            return colors["brown"]
        else:
            return colors["white"]
    

    def getxcoord(self, stat, extra):

        variables_width = sum([self.draw.textsize(variable, font=self.smallfont)[0] for variable in [stat]])
        x = (self.image.width - variables_width + extra) // 2

        return x 
    

    def winscolor(self, wins, mode):

        if mode == "":
            wins = wins / 2

        if wins < 50:
            color = colors["gray"]
        elif wins < 100:
            color = colors["dark_gray"]
        elif wins < 250:
            color = colors["white"]
        elif wins < 500:
            color = colors["gold"]
        elif wins < 1000:
            color = colors["dark_aqua"]
        elif wins < 2000:
            color = colors["dark_green"]
        elif wins < 5000:
            color = colors["dark_red"]
        elif wins < 10000:
            color = colors["yellow"]
        elif wins < 25000:
            color = colors["dark_purple"]
        elif wins < 50000:
            color = colors["aqua"]
        elif wins < 100000:
            color = colors["pink"]
        else:
            color = colors["red"]

        return color

    def wlrcolor(self, wlr):

        if wlr < 1:
            color = colors["dark_gray"]
        elif wlr < 2:
            color = colors["white"]
        elif wlr < 3:
            color = colors["gold"]
        elif wlr < 5:
            color = colors["dark_aqua"]
        elif wlr < 7.5:
            color = colors["dark_green"]
        elif wlr < 10:
            color = colors["dark_red"]
        elif wlr < 20:
            color = colors["yellow"]
        elif wlr < 40:
            color = colors["dark_purple"]
        elif wlr < 60:
            color = colors["aqua"]
        elif wlr < 80:
            color = colors["pink"]
        elif wlr < 100:
            color = colors["red"]
        else:
                color = colors["red"]

        return color
        

async def setup(bot):
    await bot.add_cog(guildimage(bot))
    await bot.add_cog(drawlb(bot))
        