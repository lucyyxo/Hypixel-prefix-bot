from discord.ext import commands
import discord, os, asyncio
from api.uuid import playerinfo
from player.main import General
from .draw import guildimage
from .draw import drawlb
from .stats import LBstats

class Guildtop(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.player = playerinfo(bot)
        self.general = General(bot)
        self.guild = guildimage(bot)
        self.lb = LBstats(bot)
        self.drawguild = drawlb(bot)
        self.dropdown_menus = {}

    async def getinfo(self, ctx, guildname, gamemode, mode, start_rank):
        
        info = await self.player.getguild(ctx, guildname)
        guildinfo = self.general.guild(guildinfo=info)
        await self.lb.getstats(ctx, info, guildinfo, gamemode)
        guildimg = self.guild.topdisplay(ctx, guildinfo, gamemode)
        
        self.file = self.drawguild.generateimage(guildimg, guildinfo, mode, start_rank, gamemode)
        
        await self.savedrop(ctx, guildimg, guildinfo, mode, gamemode, start_rank)

    
    async def savedrop(self, ctx, guildimg, guildinfo, mode, gamemode, start_rank):

        if ctx.author.id not in self.dropdown_menus:
            self.dropdown_menus[ctx.author.id] = {'selects': {}}
        self.dropdown_menus[ctx.author.id]['guildimage'] = guildimg
        self.dropdown_menus[ctx.author.id]['guildinfo'] = guildinfo
        self.dropdown_menus[ctx.author.id]["start_rank"] = start_rank
        self.dropdown_menus[ctx.author.id]["mode"] = mode


        await self.dropdownmenu(ctx, guildimg, guildinfo, mode, gamemode, start_rank)

    async def dropdownmenu(self, ctx, guildimg, guildinfo, mode, gamemode, start_rank):

        user_data = self.dropdown_menus.get(ctx.author.id, {})
        guildimg = user_data.get('guildimage', '')
        guildinfo = user_data.get('guildinfo', '')
        start_rank = user_data.get("start_rank", "")
        mode = user_data.get("mode", "")

        match gamemode:
            case "Duels":
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
            case "Bedwars":
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
            
            case "SkyWars":
                options = [
                    discord.SelectOption(label="Overall", value="Overall"),
                    discord.SelectOption(label="Solos", value="Solo"),
                    discord.SelectOption(label="Doubles", value="Doubles"),
                    discord.SelectOption(label="Ranked", value="Ranked"),
                    discord.SelectOption(label="Mega", value="Mega")
                ]

        select = discord.ui.Select(placeholder="Overall",options=options)
        increase = discord.ui.Button(label="🡅", style=discord.ButtonStyle.green, custom_id="scrollup")
        decrease = discord.ui.Button(label="🡇", style=discord.ButtonStyle.red, custom_id="scrolldown")
        view = discord.ui.View()
        view.add_item(increase)
        view.add_item(decrease)
        view.add_item(select)
        message = await ctx.reply(file=self.file,view=view)

        user_data['selects'][message.id] = {
            'select': select,
            'guildimage': guildimg,
            'guildinfo': guildinfo,
            'view': view,
            "mode": mode,
            "gamemode": gamemode,
            "start_rank": start_rank
        } 

        self.dropdown_menus[ctx.author.id] = user_data
        select.callback = self.callback
        increase.callback = self.buttons
        decrease.callback = self.buttons

        await asyncio.sleep(300)
        user_data = self.dropdown_menus.get(ctx.author.id, {})
        select_data = user_data.get('selects', {}).get(message.id)
        if select_data:
            view.remove_item(select)
            view.remove_item(increase) 
            view.remove_item(decrease)
            await message.edit(view=view)
            os.remove(select_data["guildimage"])
            del user_data['selects'][message.id]
            self.dropdown_menus[ctx.author.id] = user_data
    
    async def callback(self, interaction: discord.Interaction):
        
        try:
            user_id = interaction.user.id
            message_id = interaction.message.id
            user_data = self.dropdown_menus.get(user_id, {})
            select_data = user_data.get('selects', {}).get(message_id)
            if select_data:
                mode = interaction.data["values"][0]
                if mode == 'Overall':
                    mode = ''
                gamemode = select_data["gamemode"]
                guildimg = select_data['guildimage']
                guildinfo = select_data['guildinfo']
                view = select_data["view"]

                file = self.drawguild.generateimage(guildimg, guildinfo, mode=mode, start_rank=1, gamemode=gamemode)
                await self.update_select_menu(user_id, message_id, mode)
                await interaction.response.edit_message(attachments=[file],view=view)
                select_data["mode"] = mode
                select_data["start_rank"] = 1
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
    
    async def buttons(self, interaction:discord.Interaction):
        try:
            action = interaction.data["custom_id"]
            user_id = interaction.user.id
            message_id = interaction.message.id
            user_data = self.dropdown_menus.get(user_id, {})
            select_data = user_data.get('selects', {}).get(message_id)
            if select_data:
                mode = select_data["mode"]
                gamemode = select_data["gamemode"]
                guildimg = select_data['guildimage']
                guildinfo = select_data['guildinfo']
                view = select_data["view"]
                
                if action == "scrolldown":
                    select_data["start_rank"] += 10
                elif action == "scrollup":
                    select_data["start_rank"] -= 10
        
                if select_data["start_rank"] < 1:
                    select_data["start_rank"] = 1
                
                file = self.drawguild.generateimage(guildimg, guildinfo, mode, start_rank=select_data["start_rank"], gamemode=gamemode)
                await interaction.response.edit_message(attachments=[file],view=view)
            else:
                await interaction.response.send_message(content="This Interaction was either ended or not used by the original user.",ephemeral=True)
            
        except: 
            if action == "scrolldown":
                select_data["start_rank"] -= 10
            elif action == "scrollup":
                    select_data["start_rank"] += 10
            if select_data["start_rank"] < 1:
                    select_data["start_rank"] = 1


async def setup(bot):
    await bot.add_cog(Guildtop(bot))
