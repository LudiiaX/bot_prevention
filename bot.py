from discord.ext.commands import Bot
import discord
from discord.voice_client import VoiceClient
import os
import threading
import time
from pytube import YouTube
# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
bot = Bot("*", intents=intents)



members = []
list_members = []
vc = None
#Amélioration :
#Ne pas se prévenir soit meme quand on rejoint
#Faire une liste de membre par serveur est non global
#   avec un dico
#Faire un code propre, ranger et le deamoniser

@bot.event
async def on_ready():
    global members, lavalink2
    add_members()
    for i in members:
        await i.send("Bot pret")
    await bot.change_presence(status = discord.Status.online, activity=discord.Game("*help"))


@bot.event
async def on_voice_state_update(member, before, after):
    global members
    
    if after.channel != None:
        for i in members:
            if str(after.channel.guild) == str(i.guild.name):
                await i.send(str(member.name) + " vient de se connecter dans " + str(after.channel.name) + " du serveur " + str(after.channel.guild.name))

@bot.command(name='add_me',
             help="permet de s'ajouter du programme de prevention."
)
async def add_me(ctx):
    global list_members
    if ctx.author.name in list_members:
        await ctx.send(f'{ctx.author.mention} tu es déjà dedans idiot.')
    else :
        list_members.append(ctx.author.name)
        add_members()
        await ctx.send(f'{ctx.author.mention} ouais je te pinguerais tkt.')

@bot.command(name='remove_me',
             help="permet de se retirer du programme de prevention."
)
async def remove_me(ctx):
    global list_members
    if ctx.author.name in list_members:
        list_members.remove(ctx.author.name)
        add_members()
        await ctx.send(f'{ctx.author.mention} ok c est bon je te spamerais plus tkt.')


@bot.command(name="bangasound",
             help="permet de mettre la musique Bangarang.")
async def bangasound(ctx):
    global vc
    if ctx.message.author.voice:
        if vc == None:
            author = ctx.message.author
            print(author.voice.channel)
            channel = author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source="music/skrillex-bangarang-feat-sirah-official-music-video.mp3"))
            print("test")
            print(vc)
        else :
            if vc.is_connected() and ctx.message.author.voice.channel != vc.channel:
                vc.move_to(ctx.message.author.voice.channel)
            if not vc.is_connected():
                vc.ctx.message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source="music/skrillex-bangarang-feat-sirah-official-music-video.mp3"))


@bot.command()
async def play(ctx, url):
    global vc
    yt = YouTube(url)
    print(yt)
    print(yt.streams)
    print(yt.streams.filter(only_audio=True))
    stream = yt.streams.last()
    #music = stream.download(output_path="music/")
    if rechercher(yt.title):
        music = "music/"+ yt.title 
    else :
        music = download(url)

    if ctx.message.author.voice:
        if vc == None:
            author = ctx.message.author
            print(author.voice.channel)
            channel = author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source=music))
            print("test")
            print(vc)
        else :
            if vc.is_connected() and ctx.message.author.voice.channel != vc.channel:
                vc.move_to(ctx.message.author.voice.channel)
            if not vc.is_connected():
                vc.ctx.message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source=music))

def rechercher(title):
    print(title)
    with open('music.txt', 'r') as fichier:
        contenu = fichier.read()
    print(contenu)
    liste = contenu.split("\n")
    print(liste)
    for i in liste:
        if title in i:
            print("True")
            return True
    print("False")
    return False

def download(url):
    print("JE DL")
    yt = YouTube(url)
    print(yt.title)
    print(yt.streams.filter(only_audio=True))
    stream = yt.streams.last()
    music = stream.download(output_path="music/", filename=yt.title)
    with open('music.txt', 'a') as fichier:
        fichier.write(yt.title + "\n")
    return music


@bot.command(name="stop",
             help="permet de stoper la musique.")
async def stop(ctx):
    global vc
    vc.stop()

@bot.command(name="deco",
             help="permet de deconnecter le bot.")
async def deco(ctx):
    global vc
    await vc.disconnect()

def add_members():
    global list_members, members
    test = bot.get_all_members()
    members = []
    for i in test:
        if i.name in list_members:
            members.append(i)


bot.run(DISCORD_TOKEN, reconnect=True) #log_handler=None
