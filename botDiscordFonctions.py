# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:54:48 2021

@author: forestas yan
"""

import discord
import datetime
import json
from requetesAPI import *

emotes_id = {"X"   : "<:Rank_SS:836211894570319893>",
             "XH"  : "<:Rank_SSH:837678020877746177>",
             "S"    : "<:Rank_S:836211892917370950>",
             "SH"   : "<:Rank_SH:837678020763451412>",
             "A"    : "<:Rank_A:836211892694941717>",
             "B"    : "<:Rank_B:837678020722294894>",
             "C"    : "<:Rank_C:837678018532474912>",
             "D"    : "<:Rank_D:837678018511241257>",
             "F"    : "<:Rank_F:837678018570354728>"}

def set_profile(user, author):
    if get_user(user) != []:
        with open('data/players.json') as f:
            players = json.load(f)
            players[str(author)] = user
            
        with open('data/players.json', 'w') as f:
            json.dump(players, f)
        return ":white_check_mark: Your Osu! profile has been set to " + user
    
    else:
        return ":x: This username is invalid"

#return how long ago a certain date was
def get_interval_of_time(time):

    time1 = datetime.datetime(int(time[:4]), int(time[5:7]), int(time[8:10]), int(time[11:13]), int(time[14:16]), int(time[17:19]))
    time2 = datetime.datetime.utcnow()
    duration = time2 - time1
    days = duration.days
    seconds = duration.seconds
    
    interval = ""
    if days//365 != 0:
        interval += str(days//365) + " years, "
        days = days%365
    if days//31 != 0:
        interval += str(days//31) + " months, "
        days = days%31
    if days != 0:
        interval += str(days) + " days, "
        
    interval += seconds_to_days(seconds)
    return interval


def seconds_to_days(seconds):
    interval = ""
    if seconds//86400 != 0:
        interval += str(seconds//86400) + " days, "
        seconds = seconds%86400
    if seconds//3600 != 0:
        interval += str(seconds//3600) + " hours, "
        seconds = seconds%3600
    if seconds//60 != 0:
        interval += str(seconds//60) + " minutes, "
        seconds = seconds%60
    if seconds != 0:
        interval += str(seconds) + " seconds"
    return interval

#a score can have "mods"
#they are options that modify slightly the map to make it more challenging t the player
def get_mods(enabled_mods):
    possible_mods = {"PF"      : 16384,
                     "FL"      : 1024,
                     "NC"      : 512,
                     "HT"      : 256,
                     "DT"      : 64,
                     "SD"      : 32,
                     "HR"      : 16,
                     "HD"      : 8,
                     "EZ"      : 2,
                     "NF"      : 1,
                     "NM"      : 0}
    
    mods = ""
    for key in possible_mods:
        if enabled_mods >= possible_mods[key]:
            if key != "DT" or ("NC" not in mods):
                enabled_mods -= possible_mods[key]
                mods += key
                
    if len(mods) > 2:
        mods = mods[:-2]
    return mods


def make_embed_profile(response):
    title = ":flag_" + response[0]['country'].lower() + ":  " + response[0]['username'] + "'s Osu!Catch profile"
    text_rank = "**-Rank: **" + response[0]['pp_rank'] + " (" + response[0]['country'] + "#" + response[0]['pp_country_rank'] +")"
    text_pp = "**-Total PP: **"  + response[0]['pp_raw']
    text_accuracy = "**-Accuracy: **" + response[0]['accuracy'][:6] + "%"
    text_playcount = "**-Playcount: **" + response[0]['playcount']
    text_playtime = "**-Playtime: **" + seconds_to_days(int(response[0]['total_seconds_played']))
    text_ranks = "**-Ranks: **" + "<:Rank_SS:836211894570319893>  " + response[0]['count_rank_ss'] + "<:Rank_S:836211892917370950>  " + response[0]['count_rank_s'] + "<:Rank_A:836211892694941717>  " + response[0]['count_rank_a']
    text_footer = "Joined " + get_interval_of_time(response[0]['join_date']) + " ago"
    
    embed = discord.Embed(  title = title,
                            url="https://osu.ppy.sh/users/" + response[0]['user_id'],
                            description =   text_rank + "\n" +
                                            text_pp + "\n" +
                                            text_accuracy + "\n" + "\n" +
                                            text_playcount + "\n" +
                                            text_playtime + "\n" + "\n" +
                                            text_ranks)
    
    embed.set_thumbnail(url = "https://old.ppy.sh/a/" + response[0]['user_id'])
    embed.set_footer(text=text_footer)
    return embed


def make_embed_top(response, user):
    user = get_user(user)
    title = ":flag_" + user[0]['country'].lower() + ":  Top plays for " + user[0]['username'] + " in Catch the beat!"
    text_author = "Top plays for " + user[0]['username']

    embed = discord.Embed(  title = title,
                            url="https://osu.ppy.sh/users/" + response[0]['user_id'],
                            description = "")
    score_id = 1
    for score in response:
        
        mods = get_mods(int(score['enabled_mods']))
    
        if ("HR" in mods) and ("DT" in mods or "NC" in mods):
            beatmap = get_beatmap(score['beatmap_id'], "80")
        elif ("HR" in mods):
            beatmap = get_beatmap(score['beatmap_id'], "16")
        elif ("DT" in mods or "NC" in mods):
            beatmap = get_beatmap(score['beatmap_id'], "64")
        else:
            beatmap = get_beatmap(score['beatmap_id'], "0")
        
        indice = len(score['pp'] ) -1
        for k in range(len(score['pp'])):
            if score['pp'][k] == ".":
                indice = k
                
        amount_key = int(score['count50']) + int(score['count100']) + int(score['count300'] )
        accuracy = amount_key/(amount_key + int(score['countmiss']) + int(score['countkatu']))*100
        
        hyperlink = "(" + "https://osu.ppy.sh/beatmapsets/" + beatmap[0]['beatmapset_id'] + "#fruits/" + beatmap[0]['beatmap_id'] + ")"

        description = "**" + str(score_id) + ". [" + beatmap[0]['title'] + " [" + beatmap[0]['version'] + "]]" + hyperlink + "** + " + get_mods(int(score['enabled_mods'])) + " [" + beatmap[0]['difficultyrating'][:4] + "★]" + "\n" 
        description += "-" + emotes_id[score['rank']] +  " -** " + score['pp'][:indice+2] + "pp **" + "- " + str(accuracy)[:5] + "% " + "- " + score['date'][:10] + "\n"
        description += "- **Score:** " + score['score'] + ", **Combo:** " + score['maxcombo'] + "/" + score['maxcombo'] +  ", **Miss:** " + score['countmiss'] + ", **Dropmiss:** " + score['countkatu']
        
        #The name of the field is not space but a special invisible character
        embed.add_field(name="ㅤ", value = description, inline=False)
        score_id += 1


    embed.set_thumbnail(url = "https://old.ppy.sh/a/" + user[0]['user_id'])
    return embed


def make_embed_score(response, map_id):
    beatmap = get_beatmap(map_id, "0")
    text_author = "Top plays for " + response[0]['username'] + " on " + beatmap[0]['title'] + " [" + beatmap[0]['version'] + "]"
    description = ""
    
    for score in response:
        indice = len(score['pp'] ) -2
        for k in range(len(score['pp'])):
            if score['pp'][k] == ".":
                indice = k
                
        amount_key = int(score['count50']) + int(score['count100']) + int(score['count300'] )
        accuracy = amount_key/(amount_key + int(score['countmiss']) + int(score['countkatu']))*100
        
        description += "- `" + get_mods(int(score['enabled_mods'])) +"`: " +  "**" + score['pp'][:indice+2] + "pp **" + "- " + str(accuracy)[:5] + "% " + "- " + score['date'][:10] + "\n"
        description += "-**Score:** " + score['score'] + ", **Combo:** " + score['maxcombo'] + "/" + str(int(beatmap[0]['max_combo']) - int(beatmap[0]['count_spinner'])) +  ", **Miss:** " + score['countmiss'] + ", **Dropmiss:** " + score['countkatu']
        description += "\n\n"
    
    embed = discord.Embed(  title = "",
                            url = "",
                            description = description)
    
    embed.set_author(name=text_author, url="https://osu.ppy.sh/beatmapsets/" + beatmap[0]['beatmapset_id'] + "#fruits/" + beatmap[0]['beatmap_id'], icon_url="https://old.ppy.sh/a/" + response[0]['user_id'])
    
    embed.set_thumbnail(url = "https://b.ppy.sh/thumb/" + beatmap[0]['beatmapset_id'] + "l.jpg")
    return embed


def make_embed_recent_score(user, response):
    score = response[0]
    mods = get_mods(int(score['enabled_mods']))
    
    if ("HR" in mods) and ("DT" in mods or "NC" in mods):
        beatmap = get_beatmap(response[0]['beatmap_id'], "80")
    elif ("HR" in mods):
        beatmap = get_beatmap(response[0]['beatmap_id'], "16")
    elif ("DT" in mods or "NC" in mods):
        beatmap = get_beatmap(response[0]['beatmap_id'], "64")
    else:
        beatmap = get_beatmap(response[0]['beatmap_id'], "0")
       
    amount_key = int(score['count50']) + int(score['count100']) + int(score['count300'])
    accuracy = amount_key/(amount_key + int(score['countmiss']) + int(score['countkatu']))*100
    
    text_author = beatmap[0]['title'] + " [" + beatmap[0]['version'] + "] + " + get_mods(int(score['enabled_mods'])) + " [" + beatmap[0]['difficultyrating'][:4] + "★]"
    description = "-" + emotes_id[score['rank']] +  " " +  str(accuracy)[:5] + "% " +  "  - Miss: " + score['countmiss'] + ", Dropmiss: " + score['countkatu'] + "\n"
    description += "-Score: " + score['score'] + ", Combo: " + score['maxcombo'] + "/" + beatmap[0]['max_combo'] 
    description += "\n\n"
    text_footer = "Beatmap by " + beatmap[0]['creator'] + " | beatmap ID: " + beatmap[0]['beatmap_id'] + " | beatmapset ID: " + beatmap[0]['beatmapset_id']
    
    
    embed = discord.Embed(  title = "",
                            url = "",
                            description = description)
    
    embed.set_author(name=text_author, url="https://osu.ppy.sh/beatmapsets/" + beatmap[0]['beatmapset_id'] + "#fruits/" + beatmap[0]['beatmap_id'], icon_url="https://old.ppy.sh/a/" + response[0]['user_id'])
    
    for score in response:
        mods = get_mods(int(score['enabled_mods']))
    
    embed.set_thumbnail(url = "https://b.ppy.sh/thumb/" + beatmap[0]['beatmapset_id'] + "l.jpg")
    embed.set_footer(text=text_footer)
    return embed























