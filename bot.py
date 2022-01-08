# User import file
from discord import embeds
import lcu
import jbGoalKeeper
# System import file
import os
import asyncio
import discord
import youtube_dl
import json
import datetime
import random
import subprocess
from requests import get
from objects import *
from discord import channel,guild
from discord.ext import commands
from dotenv import load_dotenv

# Load Environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')

# Create Bot Object
# intents = discord.Intents().all()
# client = discord.Client()
bot = commands.Bot(command_prefix='~')


#############################################################
#                 這個方法會先下載再撥放                      #
#
# Music bot settings
# youtube_dl.utils.bug_reports_message = lambda: ''
# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }
# ffmpeg_options = {
#     'options': '-vn'
# }
# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)
#         self.data = data
#         self.title = data.get('title')
#         self.url = ""
#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#         filename = data['title'] if stream else ytdl.prepare_filename(data)
#         return filename

#############################################################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("Command Not Found!")
        return
    raise error

@bot.command()
async def debug(ctx):
    await ctx.send("d")

@bot.command(name='purge', discription="Remove msg")
async def purge(ctx, num):
    if int(num) > 10:
        return
    await ctx.channel.purge(limit=int(num))

@bot.command(aliases=['新片','jable'], help='Web Crawler')
async def jav(ctx):
    if str(ctx.channel) != "jayoble_tv":
        return
    buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
    jav = jbGoalKeeper.goalKeeper
    modTime, videoList = jav.getNewest(jav)
    embedMessagesList = []
    current = 1
    for num,item in enumerate(videoList):
        embedMessages = discord.Embed(title="最近更新", description="資料抓取時間："+modTime)
        embedMessages.set_image(url=item['image'])
        embedMessages.add_field(
            name = item['number'], 
            value = "[" + item['description'] + "](https://jable.tv/videos/" + item['number'] + "/)"
        )
        embedMessages.set_footer(text = str(num+1) + "/" + str(len(videoList)))
        embedMessagesList.append(embedMessages)
    msg = await ctx.send(embed=embedMessagesList[0])
    # Add Arrow Reactions
    for btn in buttons:
        await msg.add_reaction(btn)
    while True:
        try:
        # 設閒置時限為5秒
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in buttons, timeout=5.0)
        # 結束
        except asyncio.TimeoutError:
            e = embedMessagesList[current]  
            e.set_footer(text="Time out")
            await msg.delete()
            break
        else:
            pre_page = current

            if reaction.emoji ==  u"\u23EA":
                current = 0
            elif reaction.emoji ==  u"\u25C0":
                if current > 0:
                    current-=1
            elif reaction.emoji ==  u"\u25B6":
                if current < len(embedMessagesList)-1:
                    current+=1
            elif reaction.emoji == u"\u23E9":
                current = len(embedMessagesList)-1
            # 移除使用者點擊的表情
            for btn in buttons:
                await msg.remove_reaction(btn, ctx.author)
            if current != pre_page:
                await msg.edit(embed=embedMessagesList[current])

@bot.command(name='tft', help='Show infomations about TFT')
async def tft(ctx):
    await ctx.send(file=discord.File('tft.jpg'))

@bot.command(name='w', help='Tells everyone who is ths most trolling person')
async def w(ctx):
    if str(ctx.channel) != "林阿罵👅💦":
        return
    await ctx.send("R扣正在查內碼，請稍候")
    child = subprocess.Popen(["python", "lcu.py"], stdout=subprocess.PIPE)
    # print(child.stdout)
    raw_data = ""
    for line in child.stdout:
        # print(line.decode('UTF-8'))
        if "Client not open" in str(line.decode('UTF-8')):
            await ctx.send("客戶端沒開啟")
            return
        raw_data += line.decode('UTF-8')
    # print(raw_data)
    data = json.loads(raw_data)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    if data['availability'] == "offline":
        await ctx.send("現在很安全，☆☆☆☆☆")
    elif data['availability'] == "away":
        await ctx.send("W先生掛離線，請自行斟酌，危險指數★★★☆☆")
    elif data['availability'] == "dnd":
        await ctx.send("W先生遊戲中，請自行斟酌，危險指數★★★★☆")
    elif data['availability'] == "chat":
        await ctx.send("W先生上線綠燈中，危險指數★★★★★")
    # subprocess.call("lcu.py", shell=True)

@bot.command(name='brad', help='Tells everyone who is brad')
async def brad(ctx):
    await ctx.send(brad_contents[random.randint(0, len(brad_contents)-1)])

@bot.command(aliases=['JAYO'], help='Tells everyone who is jayo')
async def jayo(ctx):
    await ctx.send(jayo_contents[random.randint(0, len(jayo_contents)-1)])

@bot.command(name='joke', help='Tells everyone who is ths most trolling person')
async def joke(ctx):
    await ctx.send(jokes[random.randint(0, len(jokes)-1)])

@bot.command(name='sing', help='Sing a song')
async def sing(ctx):
    await ctx.send(songs[random.randint(0, len(songs)-1)])

@bot.command(name='中平', help='Tells everyone who is G8 person')
async def zonPin(ctx):
    await ctx.send("幹你娘觘機掰")

@bot.command(name='ㄘㄨㄚˋ', help='Tells everyone who is G8 person')
async def t(ctx):
    await ctx.send("ㄘㄨㄚˋ英文觘機掰")

@bot.command(name='show', help='Show records of violation')
async def show(ctx):
    print(str(ctx.channel))
    if str(ctx.channel) == "避難所💬" or str(ctx.channel) == "離題":
        return
    banHistory = {}
    # Opening JSON file
    with open('banHistory.json', 'r', encoding="utf-8") as f:
        # returns JSON object as a dictionary
        banHistory = json.load(f)
    banHistoryCount = len(banHistory)
    embedVar = discord.Embed(title="犯罪歷史紀錄", description="看一下誰都在那邊亂講話", color=discord.Colour.dark_grey())
    people = list(banHistory.keys())
    lengths = list(len(banHistory[p]) for p in banHistory)
    maxP = people[lengths.index(max(lengths))]
    count = 0
    for ct in banHistory[maxP]:
        if count >= 6:
            break
        embedVar.add_field(name="犯罪人", value=maxP, inline=True)
        embedVar.add_field(name="犯罪內容", value=ct["banContent"], inline=True)
        embedVar.add_field(name="犯罪日期", value=ct["banDate"], inline=True)
        count+=1
    embedVar.set_footer(text="目前由{}奪下 [犯罪王] 的稱號！總共違法了{}次".format(maxP, max(lengths)))
    await ctx.channel.send(embed=embedVar)

#############################################################
# TODO                                                      #
#   1. Play list add to Queue                               #
#   2. [Pause/Stop] command : To stop music                 #
#   3. [Skip]       command : To skip music now playing     #
#   4. [Add]        command : Add a music into playlist     #
#   5. [Queue]      command : List all music in queue       #
#   6. [Clean]      command : Clean up all queue            #
#   7. [Seek]       command : Seek at some music point      #
#   8. [History]    command : Show the violation history    #
#############################################################

# TODO Alias to `connect`
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
    print("Command [~play_song]")
    try :
        '''
            Play youtube music "without" download version
        '''
        ydl_opts = {'format': 'bestaudio', 'default-search': "ytdlsearch"}
        url_prefix = "https://www.youtube.com/watch?v="
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try :
                get(arg)
            except:
                # Search music by key_words
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)
                URL = info['entries'][0]['url']
                await ctx.send("正在播放：\n{}".format(url_prefix + info['entries'][0]['display_id']))
            else:
                # Search music by url
                info = ydl.extract_info(arg, download=False)
                URL = info['entries'][0]['url']
                await ctx.send("正在播放：\n{}".format(url_prefix + info['entries'][0]['display_id']))
        server = ctx.message.guild
        voice_channel = server.voice_client
        
        # TODO Self-Connect to Voice Channel if not connect

        voice_channel.play(discord.FFmpegPCMAudio(URL))

        '''
            Play youtube music "with" download version
        '''
        # server = ctx.message.guild
        # voice_channel = server.voice_client
        
        # await ctx.send("Downloading Music...")
        # async with ctx.typing():
        #     filename = await YTDLSource.from_url(url, loop=bot.loop)
        #     voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        # await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("There is something wrong.")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n'.format(bot))
    for guild in bot.guilds:
        # for channel in guild.text_channels :
        #     print("Channel:{}".format(str(channel)))
        print('\nActive in {}\n'.format(guild.name))
        print("--------------------------------------")

# TODO Check someone is online
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
        # if "歐" in message.content and "杰" in message.content:
        #     mute = True

        if mute:
            banHistory = {}
            # Opening JSON file
            with open('banHistory.json', 'r', encoding="utf-8") as f:
                # returns JSON object as a dictionary
                banHistory = json.load(f)
            banHistoryCount = len(banHistory)
            # print(banHistory)
            banPerson = message.author
            # print(str(banPerson.name), datetime.datetime.now(), message.content)
            if str(banPerson.name) not in banHistory:
                banHistory[str(banPerson.name)] = [{
                    "banContent":message.content,
                    "banDate":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }] 
            else:
                banHistory[str(banPerson.name)].append({
                    "banContent":message.content,
                    "banDate":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            # print(banHistory)
            
            for b in banHistory:
                banHistory[b] = sorted(
                    banHistory[b],
                    key = lambda x: datetime.datetime.strptime(x["banDate"], '%Y-%m-%d %H:%M:%S'),
                    reverse = True 
                )
                # banHistory[b].sort(
                #     key=lambda date: datetime.datetime.strptime(banHistory[b], "%d-%b-%y"), 
                #     reverse=True
                # )

            with open('banHistory.json', 'w', encoding='utf8') as f:
                # Set `ensure_ascii` to `False` for JSON file saving chinese context
                json_object = json.dumps(banHistory, ensure_ascii=False, indent=4, sort_keys=True, default=str)
                f.write(json_object)
            await message.channel.purge(limit=1)
            await message.channel.send(f"{banPerson.mention}，您所發送的訊息違反本伺服器第0條規則[含有本伺服器禁止提及之人事物]，因此該訊息已被刪除\n並經由大老二Jessica判處後將您送至熊熊監獄坐牢")
            # 記錄犯罪次數
            banCount = dict()
            # Opening JSON file
            with open('banCount.json', 'r', encoding="utf-8") as f:
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
            elif banCount[banPerson.name] > 20 and banCount[banPerson.name] <= 35:
                await message.channel.send(f"{banPerson.name}已經違法第{banCount[banPerson.name]}次，這個人是內鬼的機率很高")
            else:
                await message.channel.send(f"{banPerson.name} 違法第{banCount[banPerson.name]}次，這個可以踢掉了吧")

            with open('banCount.json', 'w', encoding="utf-8") as f:
                json_object = json.dumps(banCount, ensure_ascii=False, indent = 4)
                f.write(json_object)

            # 移動至監獄
            banChannel = discord.utils.get(message.guild.voice_channels, name = f"蘇聯熊熊監獄(歡迎熊能態罷)")
            if banPerson.voice is not None:
                await banPerson.edit(mute=True)
                # print(str(banPerson.voice.channel))
                await banPerson.move_to(banChannel)
    await bot.process_commands(message)

PlayList = list()
bot.run(TOKEN)