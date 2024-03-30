import discord, asyncio, os, json
from discord.ext import commands
from api.uuid import playerinfo
from player.main import General
from player.draw import image
from config import *
from .stats import getbwstats
from .draw import drawbedwars

class Bedwars(commands.Cog):

    def __init__(self,bot):
        self.uuid = playerinfo(bot)
        self.player = General(bot)
        self.draw = image(bot)
        self.stats = getbwstats(bot)
        self.bbedwars = drawbedwars(bot)
        self.dropdown_menus = {}
    
    async def getinfo(self, ctx, username, gamemode):

        info = await self.uuid.hypixel(ctx,username) 
        guildinfo = await self.uuid.guild(ctx,username)
        guild = self.player.guild(guildinfo)
        playerrank = self.player.rank(info)
        player_image = await self.draw.topdisplay(playerrank, guild, ctx, mode="bedwars")

        stats = self.stats.bwlevels(info)
        self.file = await self.bbedwars.generateimage(player_image, stats, gamemode)

        await self.savedrop(player_image, stats, ctx, playerrank, guild, info)
    
    async def savedrop(self, player_image, stats, ctx, playerrank, guild, info):

        if ctx.author.id not in self.dropdown_menus:
            self.dropdown_menus[ctx.author.id] = {'selects': {}}
        self.dropdown_menus[ctx.author.id]['player_image'] = player_image
        self.dropdown_menus[ctx.author.id]['stats'] = stats
        self.dropdown_menus[ctx.author.id]['info'] = info

        await self.dropdownmenu(ctx, playerrank, guild)
    
    async def dropdownmenu(self, ctx, playerrank, guild):

        user_data = self.dropdown_menus.get(ctx.author.id, {})
        player_image = user_data.get('player_image', '')
        stats = user_data.get('stats', '')
        info = user_data.get('info', '')
        options = [
            discord.SelectOption(label="Overall", value="Overall"),
            discord.SelectOption(label="Core", value="Core"),
            discord.SelectOption(label="Solos", value="Solo"),
            discord.SelectOption(label="Doubles",value="Doubles"),
            discord.SelectOption(label="Threes",value="Threes"),
            discord.SelectOption(label="Fours", value="Fours"),
            discord.SelectOption(label="4v4", value="4v4"),
            discord.SelectOption(label="Armed", value="Armed"),
            discord.SelectOption(label="Castle", value="Castle"),
            discord.SelectOption(label="Lucky", value="Lucky"),
            discord.SelectOption(label="Ultimate", value="Ultimate"),
            discord.SelectOption(label="Underworld", value="Underworld"),
            discord.SelectOption(label="Voidless", value="Voidless")
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
            'info': info,
            'stats': stats,
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
                stats = select_data["stats"]
                view = select_data["view"]
                file = await self.bbedwars.generateimage(player_image, stats, gamemode)
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
            filepath = f'{bwlbpath}/{guild["id"]}.json'
            uuid = info["player"]["uuid"]

            with open(filepath, 'r') as file:
                data = json.load(file)

            data[uuid]["rank"] = playerrank
            bwstats = self.stats.getstats(info)
            stats = {}
            for mode, bwmodestats in bwstats.items():
                final_kills = bwmodestats['final_kills']
                final_deaths = bwmodestats['final_deaths']
                stats[mode] = [final_kills, final_deaths]

            data[uuid]["stats"] = stats

            with open(filepath, 'w') as file:
                json.dump(data, file, indent=1)

        except FileNotFoundError:
            return None

        
async def setup(bot):
    await bot.add_cog(Bedwars(bot))