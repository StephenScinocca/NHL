import pandas as pd
from pprint import pprint
import numpy as np
import sys

import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import init_notebook_mode, iplot
from NHLHelper import init_rink

# df = pd.read_json('data.json')
# raw = pd.read_csv("data/shots_2018_2019.csv", encoding="windows-1252")
# raw2 = pd.read_csv("data/shots_2017_2018.csv", encoding="windows-1252")

rink_shapes = init_rink()

if len(sys.argv) == 1:
    player = "Auston Matthews"
    year = "2018_2019"
    type = "shots"
elif len(sys.argv) == 2:
    player = sys.argv[1]
    year = "2018_2019"
    type = "shots"
elif len(sys.argv) == 3:
    player = sys.argv[1]
    year = sys.argv[2]
    type = "shots"
elif len(sys.argv) == 4:
    player = sys.argv[1]
    year = sys.argv[2]
    type = sys.argv[3]
else:
    exit("ERROR: Too many prompts")

df = pd.read_json('data.json')
csv = "data/{}_{}.csv".format(type, year)
raw = pd.read_csv(csv, encoding="windows-1252")

# print(raw[0:5])
raw.x = abs(raw.x)
raw.x = raw.x / 100
raw.x = raw.x * 580
raw.y = raw.y / 42.5
raw.y = raw.y * 250
sub = raw.iloc[:,[0,1,2,6,7,8,9,10]]

print(sub[0:5])

single_player = sub[(sub['shooterName'] == player )]

def display_player(single_player):

    sp_shot = single_player[(single_player['eventTypeId'] == "SHOT")]
    sp_goal = single_player[(single_player['eventTypeId'] == "GOAL")]


    point_trace_shot = go.Scatter(
        x = sp_shot.y,
        y = sp_shot.x,
        name = "shots",
        mode = 'markers',
        hovertext=sp_goal.date,
        hoverinfo="text",
        marker = dict(
            size = 5
        ),
        marker_color = 'rgba(0, 0, 250, .3)'
    )

    # print("{}\n\n".format(sp_goal.date))

    testing = "{} period:{} time:{}".format(sp_goal.date, sp_goal.period, sp_goal.periodTime)
    print(testing[0])

    point_trace_goal = go.Scatter(
        x = sp_goal.y,
        y = sp_goal.x,
        name = "goals",
        # customdata = [sp_goal.date],
        # hovertemplate='date:%{customdata}', # <br>z3: %{customdata[1]:.3f}',
        hovertext=sp_goal.date,
        hoverinfo="text",
        mode = 'markers',
        marker = dict(
            size = 5
        ),
        marker_color = 'rgba(0, 100, 0, .8)'
    )


    heatmap_trace = go.Histogram2dContour(
        x = sp_goal.y,
        y = sp_goal.x,
        name='density',
        ncontours=2,
        colorscale='Hot',
        reversescale=True,
        showscale=False,
        contours=dict(coloring='heatmap')
    )

    data = [point_trace_shot, point_trace_goal]
    # data = [point_trace_shot, point_trace_goal, heatmap_trace]




    layout = go.Layout(
        shapes=rink_shapes,
        title = "{} {}".format(year, player),
        width = 500,
        height = 600
    )

    fig = go.Figure(data=data, layout=layout)

    iplot(fig)

display_player(single_player)
