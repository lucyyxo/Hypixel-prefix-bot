import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import mc_font, mc_special
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO

class drawduels(commands.Cog):

    def get_mode(self, gamemode, titles):

        for mode in titles:
            if mode['gamemode'].lower() == gamemode.lower():
                return mode
        return titles[0] 

    def generateimage(self, player_image, titles, gamemode):
        
        gamemode = self.get_mode(gamemode, titles)

        self.image = Image.open(player_image)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(mc_font, 80)
        self.other_font = ImageFont.truetype(mc_special, 60)
        self.height, self.width = self.image.size

        self.progressbar(gamemode)
        self.displaytitles(gamemode, titles)
        self.stats(gamemode)

        buffer = BytesIO()
        self.image.save(buffer, format="PNG")
        buffer.seek(0)
        filename = ('duels.png')
        file = discord.File(buffer, filename=(filename))

        return file
    
    def progressbar(self, gamemode):

        if gamemode["gamemode"] == "":
            overall_req = gamemode['req']*2
        else:
            overall_req = gamemode['req']
        
        current_wins = overall_req - gamemode['reqwins']
        percentage = current_wins / overall_req
        percentagedisplay = round(percentage * 100, 2)
        progress = (f'{current_wins}/{overall_req} [{percentagedisplay}%]')

        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [progress]])
        x = (self.image.width - variables_width) // 2
        self.draw.text((x+15, 270+15), progress, font=self.font, fill='#3F3F3F')        
        self.draw.text((x, 270), progress, font=self.font, fill='#FFFFFF')

        rect_size = (1300, 130)  
        rect_position = ((self.width - rect_size[0] + 200) // 2, (self.height - rect_size[1]) // 2 - 770) 
        corner_radius = 75
        self.draw.rounded_rectangle([rect_position, (rect_position[0] + rect_size[0] + 15, rect_position[1] + rect_size[1] + 15)], corner_radius, fill='#2A2A2A', width=2)
        self.draw.rounded_rectangle([rect_position, (rect_position[0] + rect_size[0], rect_position[1] + rect_size[1])], corner_radius, fill='#b3b3b3', width=2)

        rect_size = (1190, 130) 
        progress_bar_width = int(rect_size[0] * percentage)
        start_x = rect_position[0]
        progress_bar_height = rect_size[1]  
        corner_radius = 50
        p_colors = [gamemode["color"]['hex'], gamemode["nextcolor"]['hex']] 
        custom_cmap = LinearSegmentedColormap.from_list("CustomColormap", p_colors, N=256)
        norm = plt.Normalize(0, 1)
        progress_color = custom_cmap(norm(np.linspace(0, percentage, progress_bar_width)))
        radius = progress_bar_height // 2
        for i in range(progress_bar_width):
            color = tuple(int(c * 255) for c in progress_color[i])
            x = start_x + i + 55
            y = rect_position[1] + 65

            self.draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

        text_width, text_height = self.draw.textsize(f'[{gamemode["numeral"]}]', self.font)
        x = start_x - text_width - 50
        y = rect_position[1]
    
        self.draw.text((x+15,y+15),f'[{gamemode["numeral"]}]',font=self.font,stroke_width=gamemode["stroke"],fill=gamemode["color"]["rgb"])
        self.draw.text((x,y),f'[{gamemode["numeral"]}]',font=self.font,stroke_width=gamemode["stroke"],fill=gamemode["color"]["hex"])

        x = 1950
        self.draw.text((x+15,y+15),f'[{gamemode["next"]}]',font=self.font,stroke_width=gamemode["stroke"],fill=gamemode["nextcolor"]["rgb"])
        self.draw.text((x,y),f'[{gamemode["next"]}]',font=self.font,stroke_width=gamemode["stroke"],fill=gamemode["nextcolor"]["hex"])

    def displaytitles(self, gamemode, titles):

        y = 660
        for title_data in titles:
            title = title_data['title']
            numeral = title_data['numeral']
            color = title_data['color']
            stroke = title_data['stroke']

            title_text = f'{title} {numeral}' if numeral != "I" else title

            if gamemode['title'] == title:
                text_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in f'[{title_text}]'])
                x = (self.image.width - text_width - 1000) // 2
                self.draw.text((x + 15, y + 15), f'[{title_text}]', font=self.font, stroke_width=stroke, fill=color['rgb'])
                self.draw.text((x, y), f'[{title_text}]', font=self.font, stroke_width=stroke, fill=color['hex'])
            else:
                text_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in title_text])
                x = (self.image.width - text_width - 1000) // 2
                self.draw.text((x + 15, y + 15),title_text, font=self.font, stroke_width=stroke, fill=color['rgb'])
                self.draw.text((x, y),title_text, font=self.font, stroke_width=stroke, fill=color['hex'])
            y += 100
    
    def draw_stat(self, title, value, y_position, fill_color, shadow_color):

        formatted_value = '{:,}'.format(value)
        formatted_text = f'{formatted_value} {title}'

        self.draw.text((self.x+15, y_position+15), formatted_text, font=self.font, fill=shadow_color)
        self.draw.text((self.x, y_position), formatted_text, stroke_width=1, font=self.font, fill=fill_color)

    def stats(self, gamemode):
        
        self.x = 1630
        wins,losses,wlr,kills,deaths,kdr,ws,bws = self.getstats(gamemode)

        stats_info = [
            ('Wins', wins, 900, '#55FF55', '#153F15'),
            ('Losses', losses, 1000, '#FF5555', '#3F1515'),
            ('WLR', wlr, 1100, '#FFAA00', '#3F2A00'),
            ('Kills', kills, 1300, '#55FF55', '#153F15'),
            ('Deaths', deaths, 1400, '#FF5555', '#3F1515'),
            ('KDR', kdr, 1500, '#FFAA00', '#3F2A00'),
            ('WS', ws, 1700, '#FFFF55', '#3F3F15'),
            ('BWS', bws, 1800, '#FFFF55', '#3F3F15')
        ]
        
        for title, value, y_position, fill_color, shadow_color in stats_info:
            self.draw_stat(title, value, y_position, fill_color, shadow_color)
    
    def getstats(self, gamemode):
        
        wins = gamemode['wins'] 
        losses = gamemode['losses']   
        
        wlr = round(wins / max(losses,1),2)

        kills = gamemode["kills"]
        deaths = gamemode["deaths"]
        
        kdr = round(kills / max(deaths,1),2)

        ws = gamemode["winstreak"]
        bws = gamemode["best_winstreak"]

        return wins, losses, wlr, kills, deaths, kdr, ws, bws

async def setup(bot):
    await bot.add_cog(drawduels(bot))