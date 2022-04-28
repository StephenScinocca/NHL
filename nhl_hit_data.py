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

def reset_hit_dict():
    hit_dict = {
            "eventTypeId": "NA",
            "hitterID": "NA",
            "hitterName": "NA",
            "hitterTeamID": "NA",
            "hitteeID": "NA",
            "hitteeName": "NA",
            "x": "NA",
            "y": "NA",
            "period": "NA",
            "periodTime": "NA",
            "date": "NA"
            }
    return hit_dict

def set_hit_dict(hit_dict, hit, current_date):
    hit_dict['eventTypeId'] = hit['result']['eventTypeId']
    hit_dict['hitterTeamID'] = hit['team']['id']
    try:
        hit_dict['x'] = hit['coordinates']['x']
        hit_dict['y'] = hit['coordinates']['y']
    except KeyError:
        hit_dict['x'] = "NA"
        hit_dict['y'] = "NA"
    for p in hit['players']:
        if p['playerType'] == "Hitter":
            hit_dict['hitterID'] = p['player']['id']
            hit_dict['hitterName'] = p['player']['fullName']
        if p['playerType'] == "Hittee":
            hit_dict['hitteeID'] = p['player']['id']
            hit_dict['hitteeName'] = p['player']['fullName']
    hit_dict['period'] = hit['about']['period']
    hit_dict['periodTime'] = hit['about']['periodTime']
    hit_dict['date'] = current_date
    return hit_dict


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

header_hit = "eventTypeId,hitterID,hitterName,hitterTeamID,hitteeID,hitteeName,x,y,period,periodTime,date,gameType"
counter = 0
hit_d = reset_hit_dict()
with open("data/hits_{}_{}.csv".format(seasonStart, seasonEnd), "w") as f:
    f.write("{}\n".format(header_hit))
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
                if i['result']['eventTypeId'] == "HIT":
                    # print(counter)
                    # counter +=1
                    hit_d = set_hit_dict(hit_d, i, current_date)
                    for j in hit_d:
                        # print(hit_d[j])
                        f.write("{},".format(hit_d[j]))
                    f.write("{}\n".format(gameType))
                    hit_d = reset_hit_dict()
