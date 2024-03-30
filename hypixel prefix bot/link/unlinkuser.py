from discord.ext import commands
from api.uuid import playerinfo
import os, discord
from config import save_user

class Unlink(commands.Cog):

    async def unlink(self, ctx, username):

        file_path = f'{save_user}/{ctx.author.id}'

        if os.path.exists(file_path):
            os.remove(file_path)
            embed = discord.Embed(title='Unlinked',description=f'{ctx.author.name} has been unlinked successfully',color=discord.Color.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

            await ctx.reply(embed=embed)
        
        else:
            embed = discord.Embed(title='Not Unlinked',description=f'{ctx.author.name} isnt linked. Try .link hypixel name to connect.',color=discord.Color.red())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

            await ctx.reply(embed=embed)

    
async def setup(bot):
    await bot.add_cog(Unlink(bot))