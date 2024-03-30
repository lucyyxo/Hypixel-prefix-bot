import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import mc_font, mc_special
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO

class drawbedwars(commands.Cog):

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
        self.height, self.width = self.image.size

        self.progressbar(stats)
        self.write()
        self.getmodestats(gamemode,stats)

        buffer = BytesIO()
        self.image.save(buffer, format="PNG")
        buffer.seek(0)
        filename = ('bedwars.png')
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

        if level % 100 == 99:
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

        text_width, text_height = self.draw.textsize(star, self.font) # left star
    
        self.drawstar(x=center_x, y=175, star=star, bwcolor=stats['color'])
        self.drawstar(x=start_x-text_width-65, y=rect_position[1], star=star, bwcolor=stats['color'])
        self.drawstar(x=1950, y=rect_position[1], star=stats['nextstar'],bwcolor=stats['nextcolor'])
    
    def drawstar(self, x, y, star, bwcolor):

        symbol_to_font = {
        "✫": self.other_font,
        "✪": self.other_font,
        "⚝": self.other_font,
        "✥": self.other_font,
        }

        for char, color in zip(star, bwcolor):
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

                if part in symbols:
                    x += 15
    
    def write(self):

        data = [
            (330, 800, "Wins", '#153F15', '#55FF55'),
            (1090, 800, "Losses", '#3F1515', '#FF5555'),
            (1990, 800, "WLR", '#3F2A00', '#FFAA00'),
            (325, 1175, "Kills", '#153F15', '#55FF55'),
            (1090, 1175, "Deaths", '#3F1515', '#FF5555'),
            (2000, 1175, "KDR", '#3F2A00', '#FFAA00'),
            (220, 1550, "Final Kills", '#153F15', '#55FF55'),
            (990, 1550, "Final Deaths", '#3F1515', '#FF5555'),
            (1980, 1550, "FKDR", '#3F2A00', '#FFAA00'),
            (145, 1925, "Beds Broken", '#153F15', '#55FF55'),
            (1030, 1925, "Beds Lost", '#3F1515', '#FF5555'),
            (1980, 1925, "BBLR", '#3F2A00', '#FFAA00')
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
        "fkills": '{:,}'.format(stats["gamemode"][gamemode]["final_kills"]),
        "fdeaths": '{:,}'.format(stats["gamemode"][gamemode]["final_deaths"]),
        "fkdr": '{:,}'.format(round(stats["gamemode"][gamemode]["final_kills"] / max(stats["gamemode"][gamemode]["final_deaths"], 1), 2)),
        "bb": '{:,}'.format(stats["gamemode"][gamemode]["beds_broken"]),
        "bl": '{:,}'.format(stats["gamemode"][gamemode]["beds_lost"]),
        "bblr": '{:,}'.format(round(stats["gamemode"][gamemode]["beds_broken"] / max(stats["gamemode"][gamemode]["beds_lost"], 1), 2))
        }

        stats_info = [
            (1650, modestats["wins"], 925, '#55FF55', '#153F15'),
            (0, modestats["losses"], 925, '#FF5555', '#3F1515'),
            (-1650, modestats["wlr"], 925, '#FFAA00', '#3F2A00'),
            (1650, modestats["kills"], 1300, '#55FF55', '#153F15'),
            (0, modestats["deaths"], 1300, '#FF5555', '#3F1515'),
            (-1665, modestats["kdr"], 1300, '#FFAA00', '#3F2A00'),
            (1650, modestats["fkills"], 1675, '#55FF55', '#153F15'),
            (0, modestats["fdeaths"], 1675, '#FF5555', '#3F1515'),
            (-1680, modestats["fkdr"], 1675, '#FFAA00', '#3F2A00'),
            (1650, modestats["bb"], 2050, '#55FF55', '#153F15'),
            (0, modestats["bl"], 2050, '#FF5555', '#3F1515'),
            (-1680, modestats["bblr"], 2050, '#FFAA00', '#3F2A00')
        ]

        for offset, value, y_position, fill_color, shadow_color in stats_info:
            self.draw_stat(offset, value, y_position, fill_color, shadow_color)

async def setup(bot):
    await bot.add_cog(drawbedwars(bot))