from discord.ext import commands
from api.uuid import playerinfo
import os, discord
from config import save_user

class Link(commands.Cog):

    def __init__(self, bot):
        self.uuid = playerinfo(bot)
    
    async def link(self, ctx, username):
        
        info = await self.uuid.hypixel(ctx,username) 
        file_path = f'{save_user}/{ctx.author.id}'
        if 'socialMedia' in info['player']:
            links = info['player']['socialMedia']['links']
            uuid = info["player"]["uuid"]

            if 'DISCORD' in links and links['DISCORD'].lower() == ctx.author.name.lower():
        
                user_info = f"{uuid}"
                if os.path.exists(file_path):
                    embed = discord.Embed(title='User already linked',description=f'{ctx.author.name} has already been linked.',color=discord.Color.green())
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                    await ctx.reply(embed=embed)
                    return
                
                else:
                    with open(file_path, 'a') as file:
                        file.write(user_info)

                        embed = discord.Embed(title='Player saved',description=f'Successfully linked {ctx.author.name} to {username}',color=discord.Color.green())
                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                        await ctx.reply(embed=embed)
                        return
            else:
                embed = discord.Embed(title='Names dont match',description=f'Please make sure to link your discord account correctly on hypixel. This also includes having the updated discord tag in.',color=discord.Color.red())
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                await ctx.reply(embed=embed)
               
        else:
            embed = discord.Embed(title='No Account found',description=f'No Discord linked.',color=discord.Color.red())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Link(bot))
