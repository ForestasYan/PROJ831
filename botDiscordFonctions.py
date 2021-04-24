# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:54:48 2021

@author: forestas yan
"""

import os
import requests
import json
from dotenv import load_dotenv
import discord

load_dotenv(dotenv_path="config.txt")
k = os.getenv("k")


def make_request(request_type, data):
    request = "https://osu.ppy.sh/api/" + request_type + "?"
    
    for element in data:
        request += element + "=" + data[element] + "&"
        
    request = request[:-1]
    return request


def get_user(user):
    data = {"k" : k,
            "u" : user,
            "m" : "2"}
    
    request = make_request("get_user", data)
    r = requests.get(request)
    profile = json.loads(r.text)
    return profile


def get_user_best(user):
    data = {"k" : k,
            "u" : user,
            "m" : "2",
            "limit" : "1"}
    
    request = make_request("get_user_best", data)
    r = requests.get(request)
    scores = json.loads(r.text)
    
    for score in scores:
        del score['replay_available']
        del score['countgeki']
        del score['perfect']
    return scores



def make_embed_profile(response):
    title = ":flag_" + response[0]['country'].lower() + ":  " + response[0]['username'] + "'s osu! profile"
    text_rank = "**-Rank: **" + response[0]['pp_rank'] + "(" + response[0]['country'] + "#" + response[0]['pp_country_rank'] +")"

    embed = discord.Embed(  title = title,
                            url="https://old.ppy.sh/u/" + response[0]['user_id'],
                            description =   text_rank + "\n" +
                                            "**-Total PP: **"  + response[0]['pp_raw'])
    
    embed.set_thumbnail(url = "https://old.ppy.sh/a/" + response[0]['user_id'])
    embed.set_footer(text="He's a good guy")
    return embed























