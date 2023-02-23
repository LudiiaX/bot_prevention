from discord.ext.commands import Bot
import discord
import os 

intents = discord.Intents().all()
bot = Bot("*", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

#Amélioration :
#Ne pas se prévenir soit meme quand on rejoint

members = []
list_members = []

@bot.event
async def on_ready():
    global members
    print("Bot pret")
    add_members()
    for i in members:
        await i.send("Bot pret")
    await bot.change_presence(status = discord.Status.online, activity=discord.Game("rien"))

@bot.event
async def on_voice_state_update(member, before, after):
    global members
    if after.channel != None:
        for i in members:
            await i.send(str(member.name) + " vient de se connecter dans " + str(after.channel.name) + " du serveur " + str(after.channel.guild.name))

@bot.command(name='add_me')
async def add_me(ctx):
    global list_members
    if ctx.author.name in list_members:
        await ctx.send(f'{ctx.author.mention} est déjà dans programme de prévention.')
    else :
        list_members.append(ctx.author.name)
        add_members()
        await ctx.send(f'{ctx.author.mention} a été ajouté au programme de prévention.')

@bot.command(name='delete_me')
async def delete_me(ctx):
    global list_members
    if ctx.author.name in list_members:
        list_members.remove(ctx.author.name)
        add_members()
        await ctx.send(f'{ctx.author.mention} a été supprimé du programme de prévention.')


def add_members():
    global list_members, members
    test = bot.get_all_members()
    members = []
    for i in test:
        if i.name in list_members:
            members.append(i)
    
print("Lancement du bot .....")
bot.run(TOKEN)

