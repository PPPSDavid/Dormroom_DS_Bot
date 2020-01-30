# bot.py
import os
import discord
from discord.ext import commands
import IO
import weather
from fuzzywuzzy import fuzz
from googletrans import Translator

SUPPORTED_LANG_LIST = ['en','zh-cn','zh-tw']
LOCATION = 'Ithaca'
DAILY=True

# Check whether a selected language is supported.
def checkSupportedLang(lang:str):
    result = False
    for sLang in SUPPORTED_LANG_LIST:
        if (sLang == lang):
            result = True
    return result

#bot token
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# print(token)

# Initiate Bot instance
bot = commands.Bot(command_prefix='!')

# Start-up notification
@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!:\n'
        "and the gild name is "f'{bot.guilds[0]}')

# Check current-list stored
@bot.command(name='list', help = 'Returns the stored shopping list')
async def getAllList(ctx):
    await ctx.send(IO.readAll())

#Check current-list stored, in a specified language.
@bot.command(name='listTran', help = 'Returns the stored shopping list in desired language')
async def getAllListTran(ctx, lang:str):
    if (not checkSupportedLang(lang)):
        await ctx.send('Hmm, unsupported language detected \n Please use list command to see in English.')
    translator = Translator()
    await ctx.send(translator.translate(IO.readAll(),dest=lang).text)

# Add an item to the list
@bot.command(name = 'addlist', help = 'Add a shopping item to the shopping list')
async def addList(ctx, name:str):
    currentListSearch = IO.searchOBJ(name)
    if (currentListSearch!='None'):
        if (fuzz.partial_ratio(currentListSearch,name)==100):
            await ctx.send("An exact duplicate exist, please recheck!")
        else:
            await ctx.send("Hold on, there exist similiar item in list, do you mean "+currentListSearch+" ?")        
    else: 
        IO.writeOBJ(name)
        await ctx.send("Success!")

# Remove an item from the list
@bot.command(name = 'remove', help = "Remove a certain item from the shopping list")
async def removeList(ctx, name:str):
    currentListSearch = IO.searchOBJ(name)
    if(currentListSearch!='None'):
        if (fuzz.partial_ratio(currentListSearch,name)==100):
            IO.deleteOBJ(currentListSearch)
            await ctx.send("An exact duplicate exist, already removed!")
        else: 
            IO.deleteOBJ(currentListSearch)
            await ctx.send("I believe you mean this: "+currentListSearch+" , and this is now removed!")
    else:
        await ctx.send("Hmm, item not found. Please try again later.")


# Remove all items from a list
@bot.command(name = 'cleanAll', help = "Remove all items from the shopping list")
async def newList(ctx):
    IO.newList()
    await ctx.send("A new shopping list has been created")

# Initiate a split bill that notify group using DM.
@bot.command(name = 'collectMoney', help = 'notify every dorm member to split the bill!')
async def notifyAll(ctx, num:int):
    author = ctx.author
    for member in ctx.guild.members:
        if ((not member.bot) and (member!=author) ):
            member.send('Hi, user '+ author.name + ' has initiate a bill-split, the amount is: '+ num)
    await ctx.send('A Notification has been sent')

# Send out weather service data from given city.
@bot.command(name = 'weather', help = 'provide detailed text weather update at specified location.')
async def weatherPrint(ctx, city:str=LOCATION):
    await ctx.send("Here is your daily weather service: \n" + weather.getCurrWeather(city))


# Run Bot instance
bot.run(token)