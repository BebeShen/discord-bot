import os
import discord
from discord import channel
from discord import guild
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

banTexts = [
    "子杰",
    "OZJ",
    "ZJ"
]

i2Texts = [
    "i2",
    "哀額",
    "唉額"
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # print(message)
    # 避免機器人自己回應自己的話
    if message.author == client.user:
        return

    if message.content.startswith('/hello'):
        await message.channel.send('Hello!')

    for i2 in i2Texts:
        if i2 in message.content:
            await message.channel.send("講那甚麼洨")
            break

    mute = False
    for banText in banTexts:
        if banText in message.content:
            mute = True
    if mute:
        await message.channel.send("你已被Jessica禁言600秒")
        banPerson = message.author
        await banPerson.edit(mute=True)
        member_guild = banPerson.guild
        banChannel = discord.utils.get(member_guild.voice_channels, name = f"熊熊監獄(歡迎熊能態罷)")
        await banPerson.move_to(banChannel)

client.run(TOKEN)