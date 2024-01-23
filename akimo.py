import disnake
from disnake.ext import commands
from config import *
import os
from datetime import datetime
import random
from asyncio import sleep
from asyncio import *




bot = commands.Bot(command_prefix="&", help_command=None, case_insensitive=True, intents=disnake.Intents.all(), activity=disnake.activity.Game("0.2.6")) 


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")


start_time = datetime.now()
@bot.command()
async def uptime(ctx):
    uptime = datetime.now() - start_time
    await ctx.send(f"**Uptime:** {uptime}\n**Пинг бота:** {round(bot.latency * 1000)}ms")

#---------------коги----------------------#

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")


bot.run(settings['token'])