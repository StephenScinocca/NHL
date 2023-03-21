import pandas as pd
import argparse as ap
import urllib.request
import json
import os
import pprint as pprint
from urllib.error import URLError, HTTPError, ContentTooShortError

import sys

# link = 'https://statsapi.web.nhl.com/api/v1/game/2018030417/feed/live'
## has information on game 7 of stanley cup finals 2018-19

def parse_command_line():
    parser = ap.ArgumentParser()
    parser.add_argument('season', nargs=2, help='year of season yyyy yyyy')
    # parser.add_argument('seasonStart', nargs=1, help='year season started yyyy')
    # parser.add_argument('seasonEnd', nargs=1, help='year season ended yyyy')
    #parser.add_argument('seasonType', nargs=1, help='R (Regular Season) or P (Playoffs) or Pr (Pre Season)')

    args = parser.parse_args()

    seasonStart = args.season[0]
    seasonEnd = args.season[1]
    #seasonType = args.seasonType[0]


    return seasonStart, seasonEnd  #, season_type

def reset_shot_dict():
    shot_dict = {
            "gameID": "NA",
            "eventTypeId": "NA",
            "shooterID": "NA",
            "shooterName": "NA",
            "shooterTeamID": "NA",
            "goalieID": "NA",
            "goalieName": "NA",
            "goalieTeamID": "NA",
            "x": "NA",
            "y": "NA",
            "period": "NA",
            "periodTime": "NA",
            "date": "NA",
            "emptyNet": "NA",
            "strength": "NA",
            }
    return shot_dict

def set_shot_dict(shot_dict, shot, current_date, game_id, gameData):
    shot_dict['gameID'] = game_id
    shot_dict['eventTypeId'] = shot['result']['eventTypeId']
    shot_dict['shooterTeamID'] = shot['team']['id'] 
    try:
        shot_dict['x'] = shot['coordinates']['x']
        shot_dict['y'] = shot['coordinates']['y']
    except KeyError:
        shot_dict['x'] = "NA"
        shot_dict['y'] = "NA"
    for p in shot['players']:
        if p['playerType'] == "Scorer" or p['playerType'] == "Shooter":
            shot_dict['shooterID'] = p['player']['id']
            shot_dict['shooterName'] = p['player']['fullName']
        if p['playerType'] == "Goalie":
            shot_dict['goalieID'] = p['player']['id']
            shot_dict['goalieName'] = p['player']['fullName']
   
    if gameData['teams']['away'] != shot['team']['id']:
        shot_dict['goalieTeamID'] = gameData['teams']['away']
    else:
        shot_dict['goalieTeamID'] = gameData['teams']['home']
        
    shot_dict['period'] = shot['about']['period']
    shot_dict['periodTime'] = shot['about']['periodTime']
    shot_dict['date'] = current_date
    if shot["result"]["eventTypeId"] == "GOAL":
        shot_dict["emptyNet"] = shot["result"]["emptyNet"]
        shot_dict["strength"] = shot["result"]["strength"]["code"]
    return shot_dict


def download(link, num_retries=2):
    # print('Downloading:', link)
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
# game_id = 2018030417
# game_id_shootout = 2018010039

seasonStart, seasonEnd = parse_command_line()
print(seasonStart)
print(seasonEnd)

games = ()
schedule_link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=08/01/{}&endDate=08/01/{}&expand=schedule.teams,schedule.linescore'.format(seasonStart, seasonEnd)
if seasonStart == 2019:
    schedule_link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=08/01/{}&endDate=09/28/{}&expand=schedule.teams,schedule.linescore'.format(seasonStart, seasonEnd)
elif seasonStart == 2020:
    schedule_link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=12/01/{}&endDate=07/31/{}&expand=schedule.teams,schedule.linescore'.format(seasonStart, seasonEnd)
schedule_data = download(schedule_link)

header_shot = "GameID,eventTypeId,shooterID,shooterName,shooterTeamID,goalieID,goalieName,goalieTeamID,x,y,period,periodTime,date,emptyNet,strength,gameType"
counter = 0
shot_d = reset_shot_dict()
with open("data/shots_{}_{}.csv".format(seasonStart, seasonEnd), "w") as f:
    f.write("{}\n".format(header_shot))
    for date in schedule_data['dates']:
        current_date = date['date']
        for games in date['games']:
            print('Game {}'.format(counter))
            counter +=1
            game_id = games['gamePk']
            link = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
            data = download(link)
            plays = data['liveData']['plays']['allPlays']
            gameData = data['gameData']
            gameType = gameData['game']['type']
            for i in plays:
                # counter +=1
                if i['result']['eventTypeId'] == "SHOT" or i['result']['eventTypeId'] == "GOAL":
                    if i['about']['periodType'] != "SHOOTOUT":
                        # print(counter)
                        # counter +=1
                        shot_d = set_shot_dict(shot_d, i, current_date, game_id, gameData)
                        for j in shot_d:
                            # print(shot_d[j])
                            f.write("{},".format(shot_d[j]))
                        f.write("{}\n".format(gameType))
                        shot_d = reset_shot_dict()
