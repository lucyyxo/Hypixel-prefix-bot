import discord
from discord.ext import commands
from config import *
import asyncio
import os

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():

    print(f'{bot.user} is online')
    z = 0
    for guild in bot.guilds:
        print(f'{guild.name}')
        z+=1
    print(z)

async def main():
    async with bot:
        for file in os.listdir(controlpath):
            if file.endswith(".py"):
                await bot.load_extension(f"commands.{file[:-3]}")

        await bot.start(BOT)


@bot.remove_command('help')
@bot.group(invoke_without_command=True)
async def help(ctx):
        embed = discord.Embed(
        title='help',
        description='overview for commands',
        color=discord.Color.pink()
        )
        embed.add_field(name='Duels', value ='.d lucyyxo',inline=False)
        embed.add_field(name='prefix',value='.pr lucyyxo',inline=False)
        embed.add_field(name='guild gamemode top10',value= '.gtop d starsight',inline=False)
        embed.add_field(name="link",value=".link lucyyxo",inline=False)
        embed.add_field(name="BedWars",value=".bw lucyyxo",inline=False)
        embed.add_field(name="SkyWars",value=".sw lucyyxo",inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar) 
        await ctx.send(embed=embed) 

if __name__ == "__main__":
    asyncio.run(main())