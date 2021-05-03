# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:51:00 2021

@author: forestas yan
"""


import os
from botDiscordFonctions import *
from requetesAPI import *


from discord.ext import commands
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()

bot = commands.Bot(command_prefix="$$")

@bot.command(name="setprofile")
async def setprofile(ctx, user):
    text = set_profile(user, ctx.author)
    await ctx.channel.send(text)
    
@bot.command(name="p")
async def p(ctx, user):
    response = get_user(user)
    print(response)
    
    #uses discord's Embed class to make a stylised message
    embed = make_embed_profile(response)
    await ctx.channel.send(embed=embed)
    

@bot.command(name="top")
async def top(ctx, user):
    response = get_user_best(user)
    embed = make_embed_top(response, user)
    await ctx.channel.send(embed=embed)


@bot.command(name="s")
async def s(ctx,map_id, user):
    response = get_score_player(map_id, user)

    if response == []:
        user = get_user(user)
        beatmap = get_beatmap(map_id, 0)
        await ctx.channel.send(":x: " + "**" + user[0]['username'] +"**" + " has no play on **" + beatmap[0]['title'] + " [" + beatmap[0]['version'] + "]**")
    else:
        embed = make_embed_score(response, map_id)
        await ctx.channel.send(embed=embed)
    
    
@bot.command(name="rs")
async def rs(ctx, user):
    response = get_user_recent(user)
    
    if response == []:
        user = get_user(user)
        await ctx.channel.send(":x: " + "**" + user[0]['username'] +"**" + " has no play recent play")
    else:
        embed = make_embed_recent_score(user, response)
        await ctx.channel.send(embed=embed)
        
    

load_dotenv(dotenv_path="data/config.txt")
bot.run(os.getenv("TOKEN"))









