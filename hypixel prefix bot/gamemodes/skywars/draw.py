import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import mc_font, mc_special
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO

class drawskywars(commands.Cog):

    def get_mode(self, gamemode, stats):
        
        for mode in stats['gamemode']:
            if gamemode.lower() == mode.lower():
                return mode
        return stats['gamemode'][0]


    async def generateimage(self, player_image, stats, gamemode):
        
        gamemode = self.get_mode(gamemode, stats)

        self.image = Image.open(player_image)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(mc_font, 80)
        self.other_font = ImageFont.truetype(mc_special, 60)
        self.smallfont = ImageFont.truetype(mc_font, 70)
        self.headfont = ImageFont.truetype(mc_font, 50)
        self.height, self.width = self.image.size

        self.progressbar(stats)
        self.write()
        self.getmodestats(gamemode,stats)
        self.drawheads(gamemode, stats)

        buffer = BytesIO()
        self.image.save(buffer, format="PNG")
        buffer.seek(0)
        filename = ('skywars.png')
        file = discord.File(buffer, filename=(filename))

        return file

    def progressbar(self,stats):

        progress = stats["req"]
        percentage = stats["percentage"]
        level = stats["level"]
        star = stats['star']

        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [progress]])
        x = (self.image.width - variables_width) // 2
        self.draw.text((x+15, 400+15), progress, font=self.font, fill='#3F3F3F')        
        self.draw.text((x, 400), progress, font=self.font, fill='#FFFFFF')

        rect_size = (1300, 130)  
        rect_position = ((self.width - rect_size[0] + 200) // 2, (self.height - rect_size[1]) // 2 - 650) 
        corner_radius = 75
        self.draw.rounded_rectangle([rect_position, (rect_position[0] + rect_size[0] + 15, rect_position[1] + rect_size[1] + 15)], corner_radius, fill='#2A2A2A', width=2)
        self.draw.rounded_rectangle([rect_position, (rect_position[0] + rect_size[0], rect_position[1] + rect_size[1])], corner_radius, fill='#b3b3b3', width=2)

        rect_size = (1190, 130) 
        progress_bar_width = int(rect_size[0] * percentage)
        start_x = rect_position[0]
        progress_bar_height = rect_size[1]  
        corner_radius = 50

        if level % 10 == 4 and level < 150 or level % 10 == 9 and level < 150:
            p_colors = [stats["color"][-2]["hex"],stats["nextcolor"][-2]["hex"]]
        else:
            p_colors = []
            for color in stats['color']:
                p_colors.append(color['hex'])

        custom_cmap = LinearSegmentedColormap.from_list("CustomColormap", p_colors, N=256)
        norm = plt.Normalize(0, 1)
        progress_color = custom_cmap(norm(np.linspace(0, percentage, progress_bar_width)))
        radius = progress_bar_height // 2
        for i in range(progress_bar_width):
            color = tuple(int(c * 255) for c in progress_color[i])
            x = start_x + i + 55
            y = rect_position[1] + 65

            self.draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
        
        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [star]])
        center_x = (self.image.width - variables_width - 20) // 2 # center star

        text_width, text_height = self.draw.textsize(star, self.font) 

        if len(star) == 8:
            bonus = 15
        else: 
            bonus = 65
    
        self.drawstar(x=center_x, y=175, star=star, swcolor=stats['color'])
        self.drawstar(x=start_x-text_width-bonus, y=rect_position[1], star=star, swcolor=stats['color'])
        self.drawstar(x=1950, y=rect_position[1], star=stats['nextstar'],swcolor=stats['nextcolor'])
    
    def drawstar(self, x, y, star, swcolor):

        symbol_to_font = {
        star[-2]: self.other_font,
        }

        for char, color in zip(star, swcolor):
            symbols = symbol_to_font.keys()
            parts = [char]

            for part in parts:
                if part in symbols:
                    symbol_font = symbol_to_font.get(part, self.font)
                    self.draw.text((x+15, y + 46), part, font=symbol_font, fill=color['rgb'])
                    self.draw.text((x, y + 31), part, font=symbol_font, fill=color['hex'])
                else:
                    self.draw.text((x+15, y+15), part, font=self.font, fill=color['rgb'])
                    self.draw.text((x, y), part, font=self.font, fill=color['hex'])

                char_width, char_height = self.font.getsize(part)
                x += char_width

                if "♗" in part or '♕' in part or "⋆" in part or '★' in part or "☆" in part or "☼" in part or "⍟" in part or "⚡" in part or "ಠ" in part or "❣" in part:
                    x-=20
                elif part in symbols:
                    x += 20 
                if 'Ω' in part or "☬" in part:
                    x-=10
    
    def write(self):

        data = [
            (330, 800, "Wins", '#153F15', '#55FF55'),
            (1090, 800, "Losses", '#3F1515', '#FF5555'),
            (1990, 800, "WLR", '#3F2A00', '#FFAA00'),
            (325, 1175, "Kills", '#153F15', '#55FF55'),
            (1090, 1175, "Deaths", '#3F1515', '#FF5555'),
            (2000, 1175, "KDR", '#3F2A00', '#FFAA00'),
            (260, 1550, "Assists", '#153F15', '#55FF55'),
            (1000, 1550, "Time Played", '#3F1515', '#FF5555'),
            (250, 1925, "Bow Kills", '#153F15', '#55FF55'),
            (995, 1925, "Current Kit", '#3F1515', '#FF5555')
        ]

        for x, y, label, rgb_color, hex_color in data:
            self.draw.text((x + 15, y + 15), label, font=self.smallfont, fill=rgb_color)
            self.draw.text((x, y), label, font=self.smallfont, fill=hex_color)
    
    def draw_stat(self, offset, value, y_position, fill_color, shadow_color):

        formatted_text = f'{value}'
        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [formatted_text]])
        x = (self.image.width - variables_width - offset) // 2
        self.draw.text((x + 15, y_position + 15), formatted_text, font=self.font, fill=shadow_color)
        self.draw.text((x, y_position), formatted_text, stroke_width=1, font=self.font, fill=fill_color)

    
    def getmodestats(self, gamemode, stats):

        modestats = {
            "wins": '{:,}'.format(stats["gamemode"][gamemode]["wins"]),
            "losses": '{:,}'.format(stats["gamemode"][gamemode]["losses"]),
            "wlr": '{:,}'.format(round(stats["gamemode"][gamemode]["wins"] / max(stats["gamemode"][gamemode]["losses"], 1), 2)),
            "kills": '{:,}'.format(stats["gamemode"][gamemode]["kills"]),
            "deaths": '{:,}'.format(stats["gamemode"][gamemode]["deaths"]),
            "kdr": '{:,}'.format(round(stats["gamemode"][gamemode]["kills"] / max(stats["gamemode"][gamemode]["deaths"], 1), 2)),
            "assists": '{:,}'.format(stats["gamemode"][gamemode]["assists"]),
            "timeplayed": stats["gamemode"][gamemode]["time_played"],
            "bowkills": '{:,}'.format(stats["gamemode"][gamemode]["bow_kills"]),
            "currentkit": stats["gamemode"][gamemode]["activeKit"]
        }
        
        stats_info = [
            (1650, modestats["wins"], 925, '#55FF55', '#153F15'),
            (0, modestats["losses"], 925, '#FF5555', '#3F1515'),
            (-1650, modestats["wlr"], 925, '#FFAA00', '#3F2A00'),
            (1650, modestats["kills"], 1300, '#55FF55', '#153F15'),
            (0, modestats["deaths"], 1300, '#FF5555', '#3F1515'),
            (-1665, modestats["kdr"], 1300, '#FFAA00', '#3F2A00'),
            (1650, modestats["assists"], 1675, '#55FF55', '#153F15'),
            (0, modestats["timeplayed"], 1675, '#FF5555', '#3F1515'),
            (1650, modestats["bowkills"], 2050, '#55FF55', '#153F15'),
            (0, modestats["currentkit"], 2050, '#FF5555', '#3F1515'),
        ]

        for offset, value, y_position, fill_color, shadow_color in stats_info:
            self.draw_stat(offset, value, y_position, fill_color, shadow_color)
    
    def drawheads(self, gamemode, stats):

        modestats = {
            "Heads": '{:,}'.format(stats["gamemode"][gamemode]["heads"]),
            "Eww": '{:,}'.format(stats["gamemode"][gamemode]["heads_eww"]),
            "Yucky": '{:,}'.format(stats["gamemode"][gamemode]["heads_yucky"]),
            "Meh": '{:,}'.format(stats["gamemode"][gamemode]["heads_meh"]),
            "Decent": '{:,}'.format(stats["gamemode"][gamemode]["heads_decent"]),
            "Salty": '{:,}'.format(stats["gamemode"][gamemode]["heads_salty"]),
            "Tasty": '{:,}'.format(stats["gamemode"][gamemode]["heads_tasty"]),
            "Succulent": '{:,}'.format(stats["gamemode"][gamemode]["heads_succulent"]),
            "Sweet": '{:,}'.format(stats["gamemode"][gamemode]["heads_sweet"]),
            "Divine": '{:,}'.format(stats["gamemode"][gamemode]["heads_divine"]),
            "Heavenly": '{:,}'.format(stats["gamemode"][gamemode]["heads_heavenly"])
        }

        headdata = [
            (1760, 1580, "Eww", "#151515", "#555555") ,
            (1760, 1640, "Yucky", "#2A2A2A", "#AAAAAA"),
            (1760, 1700, "Meh", "#3F3F3F", "#FFFFFF"),
            (1760, 1760, "Decent", "#3F3F15", "#FFFF55"),
            (1760, 1820, "Salty", "#153F15", "#55FF55"),
            (1760, 1880, "Tasty", "#002A2A", "#00AAAA"),
            (1760, 1940, "Succulent", "#3F153F", "#FF55FF"),
            (1760, 2000, "Sweet", "#153F3F", "#55FFFF"),
            (1760, 2060, "Divine", "#3F2A00", "#FFAA00"),
            (1760, 2120, "Heavenly", "#2A002A", "#AA00AA")
        ]

        for x, y, label, rgb_color, hex_color in headdata:

            self.draw.text((x + 15, y + 15), label, font=self.headfont, fill=rgb_color)
            self.draw.text((x, y), label, font=self.headfont, fill=hex_color)
            x += self.draw.textsize(label, font=self.headfont)[0] + 5
            self.draw.text((x+15, y+15), f": {modestats[label]}", font=self.headfont, fill="#3F3F3F")
            self.draw.text((x, y), f": {modestats[label]}", font=self.headfont, fill="#FFFFFF")

        y = 1510
        variables_width = sum([self.draw.textsize(variable, font=self.headfont)[0] for variable in f'Heads: {modestats["Heads"]}'])
        x = (self.image.width - variables_width + 1650) // 2
        self.draw.text((x+15, y+15), "Heads", font=self.headfont, fill="#2A002A")
        self.draw.text((x, y), "Heads", font=self.headfont, fill="#AA00AA")
        x += self.draw.textsize("Heads", font=self.headfont)[0] + 5
        self.draw.text((x+15, y+15), f": {modestats['Heads']}", font=self.headfont, fill="#3F3F3F")
        self.draw.text((x, y), f": {modestats['Heads']}", font=self.headfont, fill="#FFFFFF")


async def setup(bot):
    bot.add_cog(drawskywars(bot))