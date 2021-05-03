# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 13:42:26 2021

@author: forestas yan
"""


import os
import requests
import json
from requetesAPI import *

from dotenv import load_dotenv
import discord

load_dotenv(dotenv_path="data/config.txt")
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


def get_user_recent(user):
    data = {"k" : k,
            "u" : user,
            "m" : "2"}
    
    request = make_request("get_user_recent", data)
    r = requests.get(request)
    recent_plays = json.loads(r.text)
    return recent_plays


def get_user_best(user):
    data = {"k" : k,
            "u" : user,
            "m" : "2",
            "limit": "5"}
    
    request = make_request("get_user_best", data)
    r = requests.get(request)
    scores = json.loads(r.text)
    
    for score in scores:
        del score['replay_available']
        del score['countgeki']
        del score['perfect']
    return scores


def get_beatmap(map_id, mods):
    data = {"k" : k,
            "b" : map_id,
            "mods" : mods}
    
    request = make_request("get_beatmaps", data)
    r = requests.get(request)
    beatmap = json.loads(r.text)
    for level in beatmap:
        del level['file_md5']
        del level['artist_unicode']
        del level['title_unicode']
        del level['tags']
        del level['genre_id']
        del level['favourite_count']
        del level['language_id']
        del level['rating']
        del level['storyboard']
        del level['video']
        del level['download_unavailable']
        del level['audio_unavailable']
        del level['packs']
        del level['source']
    return beatmap

def get_score_player(map_id, user):
    data = {"k" : k,
            "m" : "2",
            "u" : user,
            "type": "string",
            "b" : map_id}
    
    request = make_request("get_scores", data)
    r = requests.get(request)
    scores = json.loads(r.text)
    
    for score in scores:
        del score['replay_available']
        del score['countgeki']
        del score['perfect']
    return scores
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

