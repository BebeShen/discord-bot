import os
from typing import Tuple
import discord
import youtube_dl
import json
from dictionary import *
from discord import channel
from discord import guild
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_update(before, after):
    print("Who:",after)
    print("Status:",str(after.status))
    print("Activity:",str(after.activity))
    if str(after.status) == "online":
        await discord.utils.get(client.get_all_channels(), name="林阿罵👅💦").send("上甚麼線觘機掰")

@client.event
async def on_message(message):
    # print(message)
    # 避免機器人自己回應自己的話
    if message.author == client.user:
        return
    if str(message.channel) in channels:
        for i2 in i2Texts:
            if i2 in message.content:
                await message.channel.send("講那甚麼洨")
                break

        mute = False
        for banText in banTexts:
            if banText in message.content:
                mute = True
        if "歐" in message.content and "杰" in message.content:
            mute = True

        if mute:
            banPerson = message.author
            await message.channel.purge(limit=1)
            await message.channel.send(f"{banPerson.mention}，您所發送的訊息違反本伺服器第0條規則[含有本伺服器禁止提及之人事物]，因此該訊息已被刪除\n並經由大老二Jessica判處後將您送至熊熊監獄坐牢")
            # 記錄犯罪次數
            banCount = dict()
            # Opening JSON file
            with open('banCount.json', 'r') as f:
                # returns JSON object as a dictionary
                banCount = json.load(f)
            print(banCount)

            if banPerson.name in banCount.keys():
                banCount[banPerson.name]+=1
            else:
                print("Not in list")
                banCount.update({banPerson.name:1})
            if banCount[banPerson.name] < 3:
                await message.channel.send(f"{banPerson.name} 您違法第{banCount[banPerson.name]}次")
            elif banCount[banPerson.name] > 3 and banCount[banPerson.name] <= 10:
                await message.channel.send(f"{banPerson.name} 請注意！您已經違法第{banCount[banPerson.name]}次")
            elif banCount[banPerson.name] > 10 and banCount[banPerson.name] <= 20:
                await message.channel.send(f"警告！{banPerson.name}已經違法第{banCount[banPerson.name]}次，本頻道有暴露的可能性")
            else:
                await message.channel.send(f"{banPerson.name}已經違法第{banCount[banPerson.name]}次，這個人是內鬼的機率很高")

            with open('banCount.json', 'w') as f:
                json_object = json.dumps(banCount, indent = 4)
                f.write(json_object)

            # 移動至監獄
            banChannel = discord.utils.get(message.guild.voice_channels, name = f"熊熊監獄(歡迎熊能態罷)")
            if banPerson.voice is not None:
                await banPerson.edit(mute=True)
                # print(str(banPerson.voice.channel))
                await banPerson.move_to(banChannel)

# @client.command()
# async def play(ctx, url : str):
#     server = ctx.message.server
#     voiceChannel = client.voice_client_in(server)
#     player = await voiceChannel.create_ytdl_player(url)

banCount = dict()
client.run(TOKEN)