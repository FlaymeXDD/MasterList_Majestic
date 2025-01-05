import requests
import discord
import asyncio

from dotenv import load_dotenv
import os

from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
bot = discord.Client(intents=intents)

load_dotenv()
token = os.getenv("TOKEN")
channelid = int(os.getenv("CHANNEL_ID"))

def url_pars():
    url = "https://api1master.majestic-files.com/meta/servers"
    response = requests.get(url)
    temp = response.json()
        
    if 'result' in temp:
        full_info = temp['result']
        if 'servers' in full_info:
            servers = [server for server in full_info['servers'] if server.get('region') != 'eu']
            servers = sorted(servers, key=lambda server: int(server['id'][2:]))
            return servers
    return []  # Return empty list if no servers are found

async def masterlist_embed():
    servers = url_pars()

    if servers:
        total_players = 0
        icon = ""

        for server in servers:
            players = server.get('players')
            total_players += players

        embed = discord.Embed(
            title = f"Общий онлайн: {total_players:,.0f}".replace(",", " "),
            color=int("E81C5A", 16),
        )

        for server in servers:
            name = server.get('name')
            players = server.get('players')
            max_players = server.get('maxPlayersHardLimit')
            status = server.get('status')

            if status:
                status_info = "<:Checkmark:1325243634588586045>"
            else:
                status_info = "<:trialmoderator:1325243800234233897>"

            if name == 'New York':
                icon = "<:ru1:1325245154524921856>"
            elif name == 'Detroit':
                icon = "<:ru2:1325245156039069726>" 
            elif name == 'Chicago':
                icon = "<:ru3:1325245158018777181>"  
            elif name == 'San Francisco':
                icon = "<:ru4:1325245159260291132>"  
            elif name == 'Atlanta':
                icon = "<:ru5:1325245160380043274>"  
            elif name == 'San Diego':
                icon = "<:ru6:1325238312478183514>"
            elif name == 'Los Angeles':
                icon = "<:ru7:1325245163433492480>"  
            elif name == 'Miami':
                icon = "<:ru8:1325245165341900971>"  
            elif name == 'Las Vegas':
                icon = "<:ru9:1325245190214254602>"  
            elif name == 'Washington':
                icon = "<:ru10:1325245168902869032>"      
            elif name == 'Dallas':
                icon = "<:ru11:1325247054959611954>"  
            elif name == 'Boston':
                icon = "<:ru12:1325247445709492265>"  
            elif name == 'Houston':
                icon = "<:RU13:1325247254193373326>"  

            embed.set_author(
                    name="Majestic Masterlist",
                    icon_url = "https://yt3.googleusercontent.com/tQ4uUwYvV0qwDs_Q51NUNUB0ypgR-Spf5JAJbNfejnoh9n9WDl6isvS-hM3GAozz3XLAHjDw9Rs=s900-c-k-c0x00ffffff-no-rj" 
            )
            
            embed.add_field(
                name=f"**{name}**  {icon}\n**Статус сервера:** {status_info}\tㅤ",
                value=f"**Онлайн:** `{players}/{max_players}`\nㅤ",
                inline=True
            )

            time = datetime.now().strftime("%d %B  %H:%M")
            embed.set_footer(
                text=f"Информация обновлена  •  {time}"
            )

        channel = bot.get_channel(channelid)
        if channel:
            async for message in channel.history(limit=1):
                if message.author == bot.user and message.embeds:  # Проверка на наличие эмбеда
                    try:
                        await message.edit(embed=embed)  # Обновление существующего эмбеда
                        return 
                    except discord.errors.Forbidden:
                        await channel.send(embed=embed)  # Если нельзя редактировать, отправляем новый
                        return
            await channel.send(embed=embed)  # Отправка нового эмбеда, если его нет


# Periodically send updates
@bot.event
async def on_ready():
    while True:
        await masterlist_embed()
        await asyncio.sleep(5)

bot.run(token)
