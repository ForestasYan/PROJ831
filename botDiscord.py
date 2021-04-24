# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:51:00 2021

@author: forestas yan
"""


import os
from botDiscordFonctions import *

from discord.ext import commands
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()

bot = commands.Bot(command_prefix="$$")


@bot.command(name="pr")
async def pr(ctx, user):
    response = get_user(user)
    print(response)
    
    #uses discord's Embed class to make a stylised message
    embed = make_embed_profile(response)
    await ctx.channel.send(embed=embed)
    

@bot.command(name="top")
async def top(ctx, user):
    response = get_user_best(user)
    await ctx.channel.send(response)
    




load_dotenv(dotenv_path="config.txt")
bot.run(os.getenv("TOKEN"))