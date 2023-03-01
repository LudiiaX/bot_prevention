from discord.ext.commands import Bot
import discord
import os
import threading
import time
# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

@bot.event
async def on_ready():
    global members
    print("Bot pret")
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


def add_members():
    global list_members, members
    test = bot.get_all_members()
    members = []
    for i in test:
        if i.name in list_members:
            members.append(i)
    



def deamon():
    # LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
    load_dotenv()

    # GRAB THE API TOKEN FROM THE .ENV FILE.
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().all()
    bot = Bot("*", intents=intents)


    #Amélioration :
    #Ne pas se prévenir soit meme quand on rejoint
    #Faire une liste de membre par serveur est non global
    #   avec un dico
    #Faire un code propre, ranger et le deamoniser

    print("Lancement du bot .....")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    members = []
    list_members = []
    normal_thread = threading.Thread(target=deamon, name="normal_thread")
    normal_thread.start()
    time.sleep(4)