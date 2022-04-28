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

def reset_game_dict():
    game_dict = {
            "GameID": "NA",
            "GameType": "NA",
            "HomeTeamID": "NA",
            "AwayTeamID": "NA",
            "HomeTeamName": "NA",
            "AwayTeamName": "NA",
            "HomeWins": "NA",
            "HomeLosses": "NA",
            "HomeOTLosses": "NA",
            "AwayWins": "NA",
            "AwayLosses": "NA",
            "AwayOTLosses": "NA",
            "Winner": "NA",
            "Date": "NA",
            "HomeScore": "NA",
            "AwayScore": "NA",
            "HomeShots": "NA",
            "AwayShots": "NA",
            "HomeGiveaways": "NA",
            "AwayGiveaways": "NA",
            "HomeTakeaways": "NA",
            "AwayTakeaways": "NA",
            "HomePIM": "NA",
            "AwayPIM": "NA",
            "HomePPG": "NA",
            "AwayPPG": "NA",
            "HomePPA": "NA",
            "AwayPPA": "NA",
            "HomeHits": "NA",
            "AwayHits": "NA",
            "HomeFaceoff": "NA",
            "AwayFaceoff": "NA",
            "P1HomeScore": "NA",
            "P1AwayScore": "NA",
            "P1HomeShots": "NA",
            "P1AwayShots": "NA",
            "P2HomeScore": "NA",
            "P2AwayScore": "NA",
            "P2HomeShots": "NA",
            "P2AwayShots": "NA",
            "P3HomeScore": "NA",
            "P3AwayScore": "NA",
            "P3HomeShots": "NA",
            "P3AwayShots": "NA",
            "OTHomeScore": "NA",
            "OTAwayScore": "NA",
            "OTHomeShots": "NA",
            "OTAwayShots": "NA",
            "GoalieWin": "NA",
            "GoalieLoss": "NA",
            "FirstStar": "NA",
            "SecondStar": "NA",
            "ThirdStar": "NA"
            }
    return game_dict

def set_game_dict(game_dict, live, teams, game_id, gameType, current_date):
    game_dict['GameID'] = game_id
    game_dict['GameType'] = gameType
    game_dict["Date"] = current_date

    home = live['boxscore']['teams']['home']
    game_dict["HomeTeamID"] = home['team']['id']
    game_dict["HomeTeamName"] = home['team']['name']
    game_dict['HomeWins'] = teams['home']['leagueRecord']['wins']
    game_dict['HomeLosses'] = teams['home']['leagueRecord']['losses']
    if game_dict["GameType"] == "R":
        game_dict['HomeOTLosses'] =teams['home']['leagueRecord']['ot']

    homeStats = home['teamStats']['teamSkaterStats']
    game_dict['HomeScore'] = homeStats['goals']
    game_dict['HomeShots'] = homeStats['shots']
    game_dict['HomePIM'] = homeStats['pim']
    game_dict['HomePPG'] = homeStats['powerPlayGoals']
    game_dict['HomePPA'] = homeStats['powerPlayOpportunities']
    game_dict['HomeHits'] = homeStats['hits']
    game_dict['HomeTakeaways'] = homeStats['takeaways']
    game_dict['HomeGiveaways'] = homeStats['giveaways']
    game_dict['HomeFaceoff'] = homeStats['faceOffWinPercentage']

    away = live['boxscore']['teams']['away']
    game_dict["AwayTeamID"] = away['team']['id']
    game_dict["AwayTeamName"] = away['team']['name']
    game_dict['AwayWins'] = teams['away']['leagueRecord']['wins']
    game_dict['AwayLosses'] = teams['away']['leagueRecord']['losses']
    if game_dict["GameType"] == "R":
        game_dict['AwayOTLosses'] =teams['away']['leagueRecord']['ot']

    awayStats = away['teamStats']['teamSkaterStats']
    game_dict['AwayScore'] = awayStats['goals']
    game_dict['AwayShots'] = awayStats['shots']
    game_dict['AwayPIM'] = awayStats['pim']
    game_dict['AwayPPG'] = awayStats['powerPlayGoals']
    game_dict['AwayPPA'] = awayStats['powerPlayOpportunities']
    game_dict['AwayHits'] = awayStats['hits']
    game_dict['AwayTakeaways'] = awayStats['takeaways']
    game_dict['AwayGiveaways'] = awayStats['giveaways']
    game_dict['AwayFaceoff'] = awayStats['faceOffWinPercentage']

    if game_dict['AwayScore'] > game_dict['HomeScore']:
        game_dict['Winner'] = game_dict['AwayTeamID']
    elif game_dict['AwayScore'] < game_dict['HomeScore']:
        game_dict['Winner'] = game_dict['HomeTeamID']
    else:
        try:
            if live['linescore']['shootoutInfo']['away']['scores'] >  live['linescore']['shootoutInfo']['home']['scores']:
                game_dict['Winner'] = game_dict['AwayTeamID']
            elif live['linescore']['shootoutInfo']['away']['scores'] <  live['linescore']['shootoutInfo']['home']['scores']:
                game_dict['Winner'] = game_dict['HomeTeamID']
            else:
                game_dict['Winner'] = -1
        except KeyError:
            print("No shootout info?")
            game_dict['Winner'] = -1

    try:
        periods = live['linescore']['periods']
        p1 = periods[0]
        game_dict['P1HomeScore'] = p1['home']['goals']
        game_dict['P1HomeShots'] = p1['home']['shotsOnGoal']
        game_dict['P1AwayScore'] = p1['away']['goals']
        game_dict['P1AwayShots'] = p1['away']['shotsOnGoal']

        p2 = periods[1]
        game_dict['P2HomeScore'] = p2['home']['goals']
        game_dict['P2HomeShots'] = p2['home']['shotsOnGoal']
        game_dict['P2AwayScore'] = p2['away']['goals']
        game_dict['P2AwayShots'] = p2['away']['shotsOnGoal']

        p3 = periods[2]
        game_dict['P3HomeScore'] = p3['home']['goals']
        game_dict['P3HomeShots'] = p3['home']['shotsOnGoal']
        game_dict['P3AwayScore'] = p3['away']['goals']
        game_dict['P3AwayShots'] = p3['away']['shotsOnGoal']

    except IndexError:
        print(game_dict['GameID'])

    try:
        ot = periods[3]
        game_dict['OTHomeScore'] = ot['home']['goals']
        game_dict['OTHomeShots'] = ot['home']['shotsOnGoal']
        game_dict['OTAwayScore'] = ot['away']['goals']
        game_dict['OTAwayShots'] = ot['away']['shotsOnGoal']
        # game_dict[''] = shot['coordinates']['x']
        # game_dict['y'] = shot['coordinates']['y']
    except IndexError:
        game_dict['OTHomeScore'] = "NA"
        # print("NO OT game")
    #     game_dict['x'] = "NA"
    #     game_dict['y'] = "NA"

    try:
        game_dict['GoalieWin'] = live['decisions']['winner']['fullName']
        game_dict['GoalieLoss'] = live['decisions']['loser']['fullName']
        game_dict['FirstStar'] = live['decisions']['firstStar']['fullName']
        game_dict['SecondStar'] = live['decisions']['secondStar']['fullName']
        game_dict['ThirdStar'] = live['decisions']['thirdStar']['fullName']
    except KeyError:
        game_dict['GoalieWin'] = "NA"

    return game_dict


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
    schedule_link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=12/01/{}&endDate=08/01/{}&expand=schedule.teams,schedule.linescore'.format(seasonStart, seasonEnd)
schedule_data = download(schedule_link)

header_game = "GameID,GameType,HomeTeamID,AwayTeamID,HomeTeamName,AwayTeamName,HomeWins,HomeLosses,HomeOTLosses,AwayWins,AwayLosses,AwayOTLosses,Winner,Date,HomeScore,AwayScore,HomeShots,AwayShots,HomeGiveaways,AwayGiveaways,HomeTakeaways,AwayTakeaways,HomePIM,AwayPIM,HomePPG,AwayPPG,HomePPA,AwayPPA,HomeHits,AwayHits,HomeFaceoff,AwayFaceoff,P1HomeScore,P1AwayScore,P1HomeShots,P1AwayShots,P2HomeScore,P2AwayScore,P2HomeShots,P2AwayShots,P3HomeScore,P3AwayScore,P3HomeShots,P3AwayShots,OTHomeScore,OTAwayScore,OTHomeShots,OTAwayShots,GoalieWin,GoalieLoss,FirstStar,SecondStar,ThirdStar"
counter = 0
count_dates = 0
game_d = reset_game_dict()
print(schedule_data['totalGames'])
print(len(schedule_data['dates']))

# with open("data/games_{}_{}.csv".format(seasonStart, seasonEnd), "w") as f:
#     f.write("{}\n".format(header_game))
#     for date in schedule_data['dates']:
#         current_date = date['date']
#         count_dates +=1
#         for game in date['games']:
#             print('Game {}'.format(counter))
#             counter +=1
#             if game['gameType'] == "A":
#                 print("HEY NOW YOU'RE AN ALL STAR")
#                 # continue
#             game_id = game['gamePk']
#             link = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
#             data = download(link)
#             # plays = data['liveData']['plays']['allPlays']
#             gameType = data['gameData']['game']['type']
#             gameData = data['gameData']
#             teams = game['teams']
#             live = data['liveData']
#             game_d = set_game_dict(game_d, live, teams, game_id, gameType, current_date)
#             for j in game_d:
#                 # print(game_d[j])
#                 f.write("{},".format(game_d[j]))
#             # f.write("{}\n".format(gameType))
#             # f.write("{}\n".format(current_date))
#             f.write("\n")
#             game_d = reset_game_dict()

# print(count_dates)

            # for i in plays:
            #     # counter +=1
            #     if i['result']['eventTypeId'] == "SHOT" or i['result']['eventTypeId'] == "GOAL":
            #         if i['about']['periodType'] != "SHOOTOUT":
            #             # print(counter)
            #             # counter +=1
            #             game_d = set_game_dict(game_d, i, current_date, game_id)
            #             for j in game_d:
            #                 # print(game_d[j])
            #                 f.write("{},".format(game_d[j]))
            #             f.write("{}\n".format(gameType))
            #             game_d = reset_game_dict()
