from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from config import *

class image(commands.Cog):
   
    async def topdisplay(self, playerrank, guild, ctx, mode):
        
        match mode:
            case "duels":
                image = Image.open(duels_image)
            case "bedwars":
                image = Image.open(bedwars_image)
            case "skywars":
                image = Image.open(skywars_image)
            case "prefix":
                image = Image.open(prefix_image)

                
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(mc_font, 80)
        other_font = ImageFont.truetype(mc_special, 60)

        variables_width = sum([draw.textsize(variable, font=font)[0] for variable in [playerrank['rank'], playerrank['display'], guild['tag']]])
        x = (image.width - variables_width - 20) // 2
        y = 50

        for color,shadowcolor,rank in zip(playerrank['color'],playerrank['shadow'],playerrank['rank']):

            draw.text((x+15,y+15),rank,font=font,fill=shadowcolor)
            draw.text((x,y),rank,font=font,fill=color)
            char_width, char_height = font.getsize(rank)
            x+= char_width

        draw.text((x+35,y+15),playerrank['display'],font=font,fill=playerrank['shadow'][0])
        draw.text((x+20,y),playerrank['display'],font=font,fill=playerrank['color'][0])

        if guild['tag'] != '[]':
            x += draw.textsize(playerrank['display'], font=font)[0] + 50
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
            
            for gtag in guild['tag']:
                symbols = symbol_to_font
                parts = [gtag]

                for part in parts:
                    symbol_font = symbol_to_font.get(part, font)
                    char_width, char_height = symbol_font.getsize(part)

                    if part in symbols:
                        draw.text((x+15, y+46), part, font=symbol_font, fill=guild["tagcolor"]['rgb'])
                        draw.text((x, y+31), part, font=symbol_font, fill=guild["tagcolor"]['hex'])
                    else:
                        draw.text((x+15, y+15), part, font=symbol_font, fill=guild["tagcolor"]['rgb'])
                        draw.text((x, y), part, font=symbol_font, fill=guild["tagcolor"]['hex'])
                        
                    x += char_width

                if part in symbols:
                    x += 15
        
        filepath = f'{cachefile}/{ctx.message.id}.png'
        image.save(filepath)
        return filepath


async def setup(bot):
    await bot.add_cog(image(bot))