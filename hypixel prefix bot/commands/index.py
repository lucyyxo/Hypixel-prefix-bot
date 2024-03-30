import discord
from discord.ext import commands
from gamemodes.duels.statistics.main import Duels
from gamemodes.duels.prefix.main import Prefix
from gamemodes.bedwars.main import Bedwars
from gamemodes.skywars.main import SkyWars
from link.linkuser import Link
from link.unlinkuser import Unlink
from leaderboards.main import Guildtop

class duelscommand(commands.Cog):

    def __init__(self, bot):
        self.duels = Duels(bot)
        self.bedwars = Bedwars(bot)
        self.skywars = SkyWars(bot)
        self.prefix = Prefix(bot)
        self.linkuser = Link(bot)
        self.unlinkuser = Unlink(bot)
        self.guild = Guildtop(bot)

    @commands.command(aliases=['d','D','duels'])  
    @commands.cooldown(1,5,commands.BucketType.user)
    async def Duels(self, ctx, username=None):

        await self.duels.getinfo(ctx,username,gamemode="")
    
    @commands.command(aliases=['pr','Pr','PREFIX'])  
    @commands.cooldown(1,5,commands.BucketType.user)
    async def Prefix(self, ctx, username=None):

        await self.prefix.getinfo(ctx,username)
    
    @commands.command(aliases=['bw','BW','bedwars']) 
    @commands.cooldown(1,5,commands.BucketType.user) 
    async def Bedwars(self,ctx ,username=None):

        await self.bedwars.getinfo(ctx,username,gamemode="")
    
    @commands.command(aliases=['sw','SW','skywars']) 
    @commands.cooldown(1,5,commands.BucketType.user) 
    async def SkyWars(self,ctx ,username=None):

        await self.skywars.getinfo(ctx,username,gamemode="")

    @commands.command(aliases=["Link"]) 
    @commands.cooldown(1,5,commands.BucketType.user) 
    async def link(self, ctx ,username=None):

        await self.linkuser.link(ctx,username)
    
    @commands.command(aliases=["Unlink"]) 
    @commands.cooldown(1,5,commands.BucketType.user) 
    async def unlink(self, ctx ,username=None):

        await self.unlinkuser.unlink(ctx,username)

    @commands.command(aliases=["Guild", "guild", "guildtop"]) 
    @commands.cooldown(1,5,commands.BucketType.user) 
    async def gtop(self, ctx, gamemode, *,  guildname):

        match gamemode.lower():
            
            case "d" | "duels":
                await self.guild.getinfo(ctx, guildname, gamemode="Duels", mode="", start_rank=1)

            case "bw" | "bedwars":
                await self.guild.getinfo(ctx, guildname, gamemode="Bedwars", mode="", start_rank=1)

            case "sw" | "skywars":
                await self.guild.getinfo(ctx, guildname, gamemode="SkyWars", mode="", start_rank=1)

            case _:
                await ctx.reply("This bot currenlty only supports Duels, Skywars and Bedwars.")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx,error):
        
        embed = discord.Embed(
        title='Command Cooldown',
        description=f'This command is on cooldown. Please try again in {error.retry_after:.1f} seconds.',
        color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

        await ctx.reply(embed=embed) 

async def setup(bot):
    await bot.add_cog(duelscommand(bot))

