import discord, asyncio, os, json
from discord.ext import commands
from api.uuid import playerinfo
from .stats import getstats
from player.main import General
from player.draw import image
from .draw import drawduels
from config import *

    
class Duels(commands.Cog):

    def __init__(self, bot):

        self.uuid = playerinfo(bot)
        self.statcount = getstats(bot)
        self.player = General(bot)
        self.draw = image(bot)
        self.dduels = drawduels(bot)
        self.dropdown_menus = {}

    async def getinfo(self, ctx, username, gamemode):

        info = await self.uuid.hypixel(ctx,username) 
        guildinfo = await self.uuid.guild(ctx,username)
        guild = self.player.guild(guildinfo)
        playerrank = self.player.rank(info)
        titles = self.statcount.ttitles(info)
       
        player_image = await self.draw.topdisplay(playerrank, guild, ctx, mode="duels")
        self.file = self.dduels.generateimage(player_image, titles, gamemode)
        await self.savedrop(player_image, titles, info, ctx, playerrank, guild)
    
    async def savedrop(self, player_image, titles, info, ctx, playerrank, guild):
        
        if ctx.author.id not in self.dropdown_menus:
            self.dropdown_menus[ctx.author.id] = {'selects': {}}
        self.dropdown_menus[ctx.author.id]['player_image'] = player_image
        self.dropdown_menus[ctx.author.id]['titles'] = titles
        self.dropdown_menus[ctx.author.id]['info'] = info

        await self.dropdownmenu(ctx, playerrank, guild)
    
    async def dropdownmenu(self, ctx, playerrank, guild):
        
        
        user_data = self.dropdown_menus.get(ctx.author.id, {})
        player_image = user_data.get('player_image', '')
        titles = user_data.get('titles', '')
        info = user_data.get('info', '')
        options = [
            discord.SelectOption(label="Overall", value="Overall"),
            discord.SelectOption(label="BlitzSG", value="Blitz"),
            discord.SelectOption(label="Bow", value="Bow"),
            discord.SelectOption(label="Bow Spleef",value="TNT"),
            discord.SelectOption(label="Boxing",value="Boxing"),
            discord.SelectOption(label="Bridge", value="Bridge"),
            discord.SelectOption(label="Classic", value="Classic"),
            discord.SelectOption(label="Combo", value="Combo"),
            discord.SelectOption(label="MegaWalls",value="MW"),
            discord.SelectOption(label="NoDebuff",value="NoDebuff"),
            discord.SelectOption(label="OP", value="OP"),
            discord.SelectOption(label="Parkour", value="Parkour"),
            discord.SelectOption(label="SkyWars", value="SkyWars"),
            discord.SelectOption(label="Sumo",value="Sumo"),
            discord.SelectOption(label="UHC",value="UHC"),
        ]

        select = discord.ui.Select(placeholder="Overall",options=options)
        view = discord.ui.View()
        view.add_item(select)
        self.ctx = ctx
        message = await ctx.reply(file=self.file,view=view)
        self.savelb(playerrank, guild, info)

        user_data['selects'][message.id] = {
            'select': select,
            'player_image': player_image,
            'titles': titles,
            'info': info,
            'view': view
        } 

        self.dropdown_menus[ctx.author.id] = user_data
        select.callback = self.callback

        await asyncio.sleep(300)
        user_data = self.dropdown_menus.get(ctx.author.id, {})
        select_data = user_data.get('selects', {}).get(message.id)
        if select_data:
            os.remove(select_data["player_image"])
            view.remove_item(select)
            await message.edit(view=view)
            del user_data['selects'][message.id]
            
            self.dropdown_menus[ctx.author.id] = user_data
        
    
    async def callback(self, interaction: discord.Interaction):

        try:
            user_id = interaction.user.id
            message_id = interaction.message.id
            user_data = self.dropdown_menus.get(user_id, {})
            select_data = user_data.get('selects', {}).get(message_id)
            if select_data:
                gamemode = interaction.data["values"][0]
                if gamemode == 'Overall':
                    gamemode = ''
                player_image = select_data['player_image']
                titles = select_data["titles"]
                info = select_data["info"]
                view = select_data["view"]
                file = self.dduels.generateimage(player_image, titles, gamemode)
                await self.update_select_menu(user_id, message_id, gamemode)
                await interaction.response.edit_message(attachments=[file],view=view)
            else:
                await interaction.response.send_message(content="This Interaction was either ended or not used by the original user.",ephemeral=True)
        except:
            await interaction.response.send_message(content="This Interaction was either ended or not used by the original user.",ephemeral=True)

    
    async def update_select_menu(self, user_id, message_id, gamemode):

        user_data = self.dropdown_menus.get(user_id, {})
        select_data = user_data.get('selects', {}).get(message_id)
        if select_data:
            select = select_data['select']
            select.placeholder = gamemode

    
    def savelb(self, playerrank, guild, info):

        try:
            filepath = f'{duelslbpath}/{guild["id"]}.json'
            uuid = info["player"]["uuid"]
            
            with open(filepath, 'r') as file:
                data = json.load(file)

            data[uuid]["rank"] = playerrank
            data[uuid]["stats"] = self.statcount.getduelsstats(info)

            with open(filepath, 'w') as file:
                json.dump(data, file, indent=1)

        except FileNotFoundError:
            return None


async def setup(bot):
    await bot.add_cog(Duels(bot))

