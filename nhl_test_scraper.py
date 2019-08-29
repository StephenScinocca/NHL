import pandas as pd
import argparse as ap
import urllib.request
import json
import os
import pprint as pprint
from urllib.error import URLError, HTTPError, ContentTooShortError

# link = 'http://statsapi.web.nhl.com/api/v1/people/8471214/?hydrate=stats(splits=yearByYear)'
# link = 'http://statsapi.web.nhl.com/api/v1/people/8471222/?hydrate=stats(splits=yearByYear)'
## Alex Ovechkin career stats year by year
## has KHL as well as WCA and Olympics, only want NHL
# id2 = '8471222
start_id = 8471239
begin_id = 8444850
end_id = 8482000
print(end_id - begin_id)
num = 5
count = 0
# id_goalie = '8471239'
header_goalie = None
header_player = None
# link = 'http://statsapi.web.nhl.com/api/v1/people/{}/?hydrate=stats(splits=yearByYear)'.format(start_id)

def reset_player_dict():
    p_dict = {
            "timeOnIce": "NA",
            "assists": "NA",
            "goals": "NA",
            "pim": "NA",
            "shots": "NA",
            "games": "NA",
            "hits": "NA",
            "powerPlayGoals": "NA",
            "powerPlayPoints": "NA", 
            "powerPlayTimeOnIce": "NA",
            "evenTimeOnIce": "NA",
            "penaltyMinutes": "NA",
            "faceOffPct": "NA",
            "shotPct": "NA",
            "gameWinningGoals": "NA",
            "overTimeGoals": "NA",
            "shortHandedGoals": "NA",
            "shortHandedPoints": "NA",
            "shortHandedTimeOnIce": "NA",
            "blocked": "NA",
            "plusMinus": "NA",
            "points": "NA",
            "shifts": "NA"
            }
    return p_dict
        
def reset_goalie_dict():
    g_dict = {
            "timeOnIce": "NA",
            "ot": "NA", 
            "shutouts": "NA",
            "wins": "NA",
            "ties": "NA",
            "losses": "NA",
            "saves": "NA", 
            "powerPlaySaves": "NA", 
            "shortHandedSaves": "NA",
            "evenSaves": "NA",
            "shortHandedShots": "NA",
            "evenShots": "NA",
            "powerPlayShots": "NA",
            "savePercentage": "NA",
            "goalAgainstAverage": "NA",
            "games": "NA", 
            "gamesStarted": "NA", 
            "shotsAgainst": "NA",
            "goalsAgainst": "NA", 
            "powerPlaySavePercentage": "NA",
            "shortHandedSavePercentage": "NA", 
            "evenStrengthSavePercentage": "NA"
            }
    return g_dict
                    
player_dict = reset_player_dict()            
goalie_dict = reset_goalie_dict()           
                              

def download(link, num_retries=2):
    print('Downloading:', link)
    request = urllib.request.Request(link)
    try:
        with urllib.request.urlopen(request) as url:
            html = json.loads(url.read().decode())
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return 0
    return html
for id in range(begin_id, end_id):
    print(count)
    count += 1
    link = 'http://statsapi.web.nhl.com/api/v1/people/{}/?hydrate=stats(splits=yearByYear)'.format(id)
    data = download(link)
    seasons = []
    if data == None:
        print('Cant find player')
    else:
        player = data['people'][0]['stats'][0]['splits']

        if data['people'][0]['primaryPosition']['abbreviation'] == 'G':
            with open("goalies.csv", "a") as f: # change to a eventually?
                if header_goalie == None:
                    header_goalie = "NHL_player_ID, player,season,timeOnIce,ot,shutouts,wins,ties,losses,saves,powerPlaySaves,shortHandedSaves,evenSaves,shortHandedShots,evenShots,powerPlayShots,savePercentage,goalAgainstAverage,games,gamesStarted,shotsAgainst,goalsAgainst,powerPlaySavePercentage,shortHandedSavePercentage,evenStrengthSavePercentage"
                    f.write("{}\n".format(header_goalie))
                for i in player:
                    if i['league']['name'] == 'National Hockey League':
                        f.write("{},".format(id))
                        f.write("{},".format(data['people'][0]['fullName']))
                        f.write("{},".format(i['season']))
                        for j in i['stat']:
                            goalie_dict[j] = i['stat'][j]
                        for j in goalie_dict:
                            f.write("{},".format(goalie_dict[j]))
                        f.write("\n")
                        goalie_dict = reset_goalie_dict()
                print("GOALIE")
        else:
            with open("players.csv", "a") as f: # change to a eventually?
                if header_player == None:
                    header_player = "NHL_player_ID,player,season,timeOnIce,assists,goals,pim,shots,games,hits,powerPlayGoals,powerPlayPoints,powerPlayTimeOnIce,evenTimeOnIce,penaltyMinutes,faceOffPct,shotPct,gameWinningGoals,overTimeGoals,shortHandedGoals,shortHandedPoints,shortHandedTimeOnIce,blocked,plusMinus,points,shifts"
                    f.write("{}\n".format(header_player))
                for i in player:
                    if i['league']['name'] == 'National Hockey League':
                        f.write("{},".format(id))
                        f.write("{},".format(data['people'][0]['fullName']))
                        f.write("{},".format(i['season']))
                        for j in i['stat']:
                            player_dict[j] = i['stat'][j]
                        for j in player_dict:
                            f.write("{},".format(player_dict[j]))
                        f.write("\n")
                        player_dict = reset_player_dict()
                print("PLAYER")


        
# statistics = pd.DataFrame(season, columns = headers)

# pprint(season)

# print(link)