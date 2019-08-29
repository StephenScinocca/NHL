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
    parser.add_argument('seasonStart', nargs=1, help='year season started yyyy')
    parser.add_argument('seasonEnd', nargs=1, help='year season ended yyyy')
    #parser.add_argument('seasonType', nargs=1, help='R (Regular Season) or P (Playoffs) or Pr (Pre Season)')

    args = parser.parse_args()

    seasonStart = args.seasonStart[0]
    seasonEnd = args.seasonEnd[0]
    #seasonType = args.seasonType[0]


    return seasonStart, seasonEnd  #, season_type

def reset_shot_dict():
    shot_dict = {
            "eventTypeId": "NA",
            "shooterID": "NA",
            "shooterName": "NA",
            "shooterTeamID": "NA",
            "goalieID": "NA",
            "goalieName": "NA",
            "x": "NA",
            "y": "NA",
            "period": "NA",
            "periodTime": "NA",
            "date": "NA"
            }
    return shot_dict

def set_shot_dict(shot_dict, shot, current_date):
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
    shot_dict['period'] = shot['about']['period']
    shot_dict['periodTime'] = shot['about']['periodTime']
    shot_dict['date'] = current_date
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
schedule_data = download(schedule_link)

header_shot = "eventTypeId,shooterID,shooterName,shooterTeamID,goalieID,goalieName,x,y,period,periodTime,date,gameType"
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
            gameType = data['gameData']['game']['type']
            
            for i in plays:
                # counter +=1
                if i['result']['eventTypeId'] == "SHOT" or i['result']['eventTypeId'] == "GOAL":
                    if i['about']['periodType'] != "SHOOTOUT":
                        # print(counter)
                        # counter +=1
                        shot_d = set_shot_dict(shot_d, i, current_date)
                        for j in shot_d:
                            # print(shot_d[j])
                            f.write("{},".format(shot_d[j]))
                        f.write("{}\n".format(gameType))
                        shot_d = reset_shot_dict()
                        
        

