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
        return []
        
async def masterlist_embed():
    servers = url_pars() 

    if servers:
        total_players = 0
        for server in servers:
            players = server.get('players')
            total_players += players

        embed = discord.Embed(
            title = f"Majestic Masterlist [Онлайн: {total_players}]",
            color = int("E81C5A", 16),
        )
        # Устанавливаем иконку для футера
        embed.set_thumbnail(
            url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2Fa%2FAATXAJwzTgrfBJV9YCDB0tMuXy0e4-yMIsb-_WQeMw%3Ds900-c-k-c0xffffffff-no-rj-mo&f=1&nofb=1&ipt=6555cdac49409ace8b08916427a7c5b92fbcf25823dc413a4cfdf60b23b1c7d3&ipo=images" 
        )
    for server in servers:
            name = server.get('name')
            ip = server.get('ip')
            players = server.get('players')
            max_players = server.get('maxPlayersHardLimit')
            status = server.get('status')

            total_players += players

            if status == True:
                status_info = ":white_check_mark:"
            else:
                status_info = ":no_entry:"

            embed.add_field(
                name=f"**{name}** |  {status_info}",
                value=f"**Онлайн:** `{players}/{max_players}`",
                inline=False
            )
            
            time = datetime.now().strftime("%d %B %H:%M")

            embed.set_footer(
                text = f"Информация обновлена  •  {time}"
            )

    channel = bot.get_channel(channelid)
    if channel:
            async for message in channel.history(limit=1):
                await message.edit(embed=embed)
                return
            await channel.send(embed=embed)

# Запускаем периодическую отправку обновлений
@bot.event
async def on_ready():
    while True:
        await masterlist_embed()
        await asyncio.sleep(5)

bot.run(token)

