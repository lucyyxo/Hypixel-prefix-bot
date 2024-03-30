import os
from discord.ext import commands
from api.uuid import playerinfo
from player.main import General
from player.draw import image
from config import *
from .draw import drawprefix
from .stats import getprefixstats

    
class Prefix(commands.Cog):

    def __init__(self, bot):

        self.uuid = playerinfo(bot)
        self.player = General(bot)
        self.draw = image(bot)
        self.pprefix = drawprefix(bot)
        self.stats = getprefixstats(bot)
    
    async def getinfo(self, ctx, username):

        info = await self.uuid.hypixel(ctx,username) 
        guildinfo = await self.uuid.guild(ctx,username)
        guild = self.player.guild(guildinfo)
        playerrank = self.player.rank(info)
        player_image = await self.draw.topdisplay(playerrank, guild, ctx, mode="prefix")

        iconcolors, colorcolors = self.stats.getreqs(info)
        self.file = self.pprefix.generateimage(player_image, iconcolors, colorcolors)
        await ctx.reply(file=self.file)
        os.remove(player_image)

async def setup(bot):
    await bot.add_cog(Prefix(bot))
