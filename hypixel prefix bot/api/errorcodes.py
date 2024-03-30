from discord.ext import commands
import discord

class statuserrors(commands.Cog):

    async def errorcodes(self,ctx,code,username):

        match code:
            case 429:
                embed = discord.Embed(title='API Error',description=f'Failed to fetch stats for {username}. Please try again later.',color=discord.Color.red())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                await ctx.reply(embed=embed)
            case 404:
                embed = discord.Embed(title='Player not found',description=f'Failed to fetch stats for {username}. Did you spell their name right?',color=discord.Color.red())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                await ctx.reply(embed=embed)
    
    async def notfound(self,ctx,username):
        
        embed = discord.Embed(title='Player not found',description=f'Failed to fetch stats for {username}. Did you spell their name right?',color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

        await ctx.reply(embed=embed)
    
    async def notlinked(self,ctx,username):
        embed = discord.Embed(title='User not linked',description=f'Please link by using ".link (hypixelname)".',color=discord.Color.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)
    

async def setup(bot):
    await bot.add_cog(statuserrors(bot))