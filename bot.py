import os
import asyncio
import discord
import youtube_dl
import json
from dictionary import *
from discord import channel,guild
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')

# Create Bot Object
# intents = discord.Intents().all()
# client = discord.Client()
bot = commands.Bot(command_prefix='~')

# Music bot settings
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
# Download the audio file from the video link
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command()
async def debug(ctx):
    await ctx.send("d")


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    print("Command [play_song]")
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n'.format(bot))
    for guild in bot.guilds:
        for channel in guild.text_channels :
            print("Channel:{}".format(str(channel)))
        print('\nActive in {}\n'.format(guild.name))
        print("--------------------------------------")

@bot.event
async def on_member_update(before, after):
    print("Who:",after)
    print("Status:",str(after.status))
    print("Activity:",str(after.activity))
    if str(after.status) == "online":
        await discord.utils.get(bot.get_all_channels(), name="林阿罵👅💦").send("上甚麼線觘機掰")

@bot.event
async def on_message(message):
    # print(message)
    # 避免機器人自己回應自己的話
    if message.author == bot.user:
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
    await bot.process_commands(message)

banCount = dict()
bot.run(TOKEN)