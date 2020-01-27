# bot.py
import os
import discord
from discord.ext import commands

#bot token
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
# print(token)

# Initiate Bot instance
bot = commands.Bot(command_prefix='!')

#Start-up notification
@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!:\n'
        "and the gild name is "f'{bot.guilds[0]}')

#
@bot.command(name='tobuy', help = 'Responds what need to be bought')
async def getList(ctx, num_of_list:int):
    response = "Apple!"
    await ctx.send( f'{response}{num_of_list}')
# Run Bot instance
bot.run(token)