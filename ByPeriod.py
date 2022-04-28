import pandas as pd
from pprint import pprint
import numpy as np
import argparse as ap

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

def parse_command_line():
    parser = ap.ArgumentParser()
    parser.add_argument('season', nargs=2, help='year of season yyyy yyyy')
    # parser.add_argument('playerName', nargs=2, help='Name of player Sidney Crosby')
    parser.add_argument('eventType', nargs=1, help='name of event HIT or SHOT')
    parser.add_argument('gameType', nargs=1, help='R (Regular Season) or P (Playoffs) or Pr (Pre Season)')

    args = parser.parse_args()

    start_season = args.season[0]
    end_season = args.season[1]
    # player_name = "{} {}".format(args.playerName[0], args.playerName[1])
    event_type = args.eventType[0]
    game_type = args.gametype[0]

    #seasonType = args.seasonType[0]


    return start_season, end_season, event_type

def ByPeriodData(start_season = "2018", end_season = "2019", eventType = "SHOT", gameType = "R", emptyNet = True, strength = None):
    et = eventType.lower()
    if et == "goal":
        et = "shot"

    raw = pd.read_csv("data/{}s_{}_{}.csv".format(et, start_season, end_season), encoding="windows-1252")
    sub = raw[(raw["gameType"] == gameType)]
    # if eventType == "SHOT":
    #     sub = sub[(sub["eventTypeId"] == "SHOT")]
    if eventType == "GOAL":
        sub = sub[(sub["eventTypeId"] == "GOAL")]
        if emptyNet == True:
            sub = sub[(sub["emptyNet"] == "False")]
        if strength != None:
            sub = sub[(sub["strength"] == strength)]
    print(len(sub))
    p1 = sub[(sub["period"] == 1)]
    p2 = sub[(sub["period"] == 2)]
    p3 = sub[(sub["period"] == 3)]

    total_games = 1312
    if int(start_season) < 2017: #30 teams
        total_games = 1230
    elif int(start_season) < 2021: # 31 teams
        total_games = 1271
    else:
        total_games = 1312 # 32 teams

    chart = [len(p1)/(total_games*2), len(p2)/(total_games*2), len(p3)/(total_games*2)]
    print(chart)
    df = pd.DataFrame({"{}s".format(event_type.lower()): chart, 'Period': [1,2,3]})
    print(df)
    # ax = df.plot.bar(x='Period', y="{}s".format(event_type.lower()), rot=0, color = ["r","g","b"], title = "{}s per period in {}_{}".format(et, start_season, end_season))
    # fig = px.bar(df, x = "period", y = et)
    # fig.show()

    return chart



start_season, end_season, event_type = parse_command_line()
print(start_season)
print(end_season)
print(event_type)

start = int(start_season)
end = int(end_season)
period_info = np.zeros([(end-start),3])
emptyNet = False
strength = "EVEN"
i = 0
while int(start_season)+i < int(end_season):
    temp_start = str(int(start_season)+i)
    temp_end = str(int(start_season)+i+1)
    period_info[i] = ByPeriodData(temp_start, temp_end, event_type, emptyNet, strength)
    i += 1
    # start_season = temp_season

print(period_info.mean(axis = 0))
print(period_info)

df = pd.DataFrame({"{}s".format(event_type.lower()): period_info.mean(axis = 0), 'Period': [1,2,3]})
print(df)
ax = df.plot.bar(x='Period', y="{}s".format(event_type.lower()), rot=0, color = ["r","g","b"], title = "Averaged {}s per period from {} to {}".format(event_type.lower(), start_season, end_season))

plt.show()
