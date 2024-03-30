import requests
from discord.ext import commands
from api.errorcodes import statuserrors
from config import API_KEY,save_user

class playerinfo(commands.Cog):

    def __init__(self,bot):
        self.error = statuserrors(bot)        

    async def info(self,ctx,url,username):
        r = requests.get(url)
        data = r.json()
        code = r.status_code
        if code == 200:
            return data
        else:
            await self.error.errorcodes(ctx,code,username)

    async def mojang(self,ctx,username):

        file_path = f'{save_user}/{ctx.author.id}'
        
        if username is None:
            try: 
                with open(file_path,'r') as file:
                    for line in file:
                        uuid = line
            except FileNotFoundError:
                await self.error.notlinked(ctx,username)
                    
        else:
            
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
            data = await self.info(ctx,url,username)
            uuid = data.get('id')
        
        return uuid
        
    
    async def hypixel(self,ctx,username):
        
        uuid = await self.mojang(ctx,username)

        url = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
        info = await self.info(ctx,url,username)
        
        return info
    
    async def guild(self,ctx,username):

        uuid = await self.mojang(ctx,username)
        url = f'https://api.hypixel.net/guild?key={API_KEY}&player={uuid}'
        info = await self.info(ctx,url,username)
        
        return info 

    async def getguild(self, ctx, guildname):
        
        url = f'https://api.hypixel.net/findguild?byName={guildname}&key={API_KEY}'
        info = await self.info(ctx,url,username=guildname)
        gid = info['guild']
        guild = f'https://api.hypixel.net/guild?key={API_KEY}&id={gid}'
        info = await self.info(ctx,url=guild,username=guildname)

        return info


async def setup(bot):
    await bot.add_cog(playerinfo(bot))
