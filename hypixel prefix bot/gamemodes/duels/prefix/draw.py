import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import *
from io import BytesIO

class drawprefix(commands.Cog):

    def generateimage(self, player_image, iconcolors, colorcolors):

        self.image = Image.open(player_image)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(mc_font, 160)
        self.other_font = ImageFont.truetype(mc_special, 200)
        self.facefont = ImageFont.truetype(mc_special,130)
        self.numberfont = ImageFont.truetype(mc_font, 100)
        self.height, self.width = self.image.size

        self.drawicons(iconcolors)
        resultimage = self.drawcolors(colorcolors)


        buffer = BytesIO()
        resultimage.save(buffer, format="PNG")
        buffer.seek(0)
        filename = ('prefix.png')
        file = discord.File(buffer, filename=(filename))

        return file


    def drawicons(self, iconcolors):
        
        icontext = f'Icons: {iconcolors["number"]}/12'
        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [icontext]])
        center_x = (self.image.width - variables_width - 700) // 2


        self.draw.text((center_x+15, 450+15), icontext, font=self.numberfont, fill="#3F3F3F")
        self.draw.text((center_x, 450), icontext, font=self.numberfont, fill="#FFFFFF")

        self.draw.text((160+15,710+15), "✫", font=self.other_font, fill='#3F2A00')
        self.draw.text((160,710), "✫", font=self.other_font, fill='#FFAA00')

        data = {
            "Combo": (530,700, "✯", self.other_font),
            "Classic": (900, 700, "✵", self.other_font),
            "NoDebuff": (160, 1100, "❂", self.other_font),
            "Sumo": (530, 1090, "☣", self.other_font),
            "Parkour": (900, 1100, "❀", self.other_font),
            "Bow": (170, 1520, "☯", self.other_font),
            "TNT": (530, 1510, "☃", self.other_font),
            "OP": (900, 1510, "❤", self.other_font),
            "Boxing": (160+15, 1900+15, "GG", self.font),
            "Blitz": (530+15, 1945+15, "^_^", self.facefont),
            "": (850+15, 1945+15, "#???", self.numberfont)
        }

        for key, (x, y, icon, font) in data.items():
            self.draw.text((x+15, y+15), icon, font=font, fill=iconcolors[key]["rgb"])
            self.draw.text((x, y), icon, font=font, fill=iconcolors[key]["hex"])

    
    def drawcolors(self, colorcolors):

        icontext = f'Colors: {colorcolors["number"]}/12'
        variables_width = sum([self.draw.textsize(variable, font=self.font)[0] for variable in [icontext]])
        center_x = (self.image.width - variables_width + 1700) // 2

        self.draw.text((center_x+15, 450+15), icontext, font=self.numberfont, fill="#3F3F3F")
        self.draw.text((center_x, 450), icontext, font=self.numberfont, fill="#FFFFFF")


        self.gold = Image.open(orange).convert("RGBA")
        self.white = Image.open(white).convert("RGBA")
        self.red = Image.open(red).convert("RGBA")
        self.aqua = Image.open(aqua).convert("RGBA")
        self.yellow = Image.open(yellow).convert("RGBA")
        self.green = Image.open(green).convert("RGBA")
        self.blue = Image.open(blue).convert("RGBA")
        self.pink = Image.open(pink).convert("RGBA")
        self.black = Image.open(black).convert("RGBA")
        self.dark_red = Image.open(dark_red).convert("RGBA")
        self.dark_blue = Image.open(dark_blue).convert("RGBA")
        self.dark_purple = Image.open(dark_purple).convert("RGBA")
        
                
        result_image = Image.new('RGBA', (self.image.width, self.image.height), (0, 0, 0, 0))
        result_image.paste(self.image, (0, 0))

        data = {
            "default": (1330, 690, self.gold, 100),
            "white": (1700, 670, self.white, colorcolors[""]),
            "red": (2070, 670, self.red, colorcolors["Boxing"]),
            "aqua": (1330, 1080, self.aqua, colorcolors["OP"]),
            "yellow": (1700, 1080, self.yellow, colorcolors["UHC"]),
            "green": (2070, 1080, self.green, colorcolors["SkyWars"]),
            "blue": (1330, 1490, self.blue, colorcolors["Blitz"]),
            "pink": (1700, 1490, self.pink, colorcolors["Bridge"]),
            "black": (2070, 1490, self.black, colorcolors["MW"]),
            "dark_red": (1330, 1870, self.dark_red, colorcolors["TNT"]),
            "dark_blue": (1700, 1870, self.dark_blue, colorcolors["Combo"]),
            "dark_purple": (2070, 1870, self.dark_purple, colorcolors["Parkour"]),
        }

        for key, (x, y, color, trans) in data.items():

            transparency = trans
            data = color.getdata()
            updated_data = [(r, g, b, int(a * transparency / 40)) for r, g, b, a in data]
            color.putdata(updated_data)
            result_image.paste(color, (x,y), color)
            resultimage = result_image.convert('RGB')

        return resultimage