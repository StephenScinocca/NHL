import pandas as pd
from pprint import pprint
import numpy as np
import argparse as ap

import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

def parse_command_line():
    parser = ap.ArgumentParser()
    parser.add_argument('season', nargs=1, help='year of season yyyy_yyyy')
    parser.add_argument('playerName', nargs=2, help='Name of player Sidney Crosby')
    parser.add_argument('eventType', nargs=1, help='name of event HIT or SHOT')

    #parser.add_argument('seasonType', nargs=1, help='R (Regular Season) or P (Playoffs) or Pr (Pre Season)')

    args = parser.parse_args()

    season = args.season[0]
    player_name = "{} {}".format(args.playerName[0], args.playerName[1])
    event_type = args.eventType[0]

    #seasonType = args.seasonType[0]


    return season, player_name, event_type  #, season_type

def generate_rink_shapes():
    #list containing all the shapes
    rink_shapes = []

    outer_rect_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='-250',
        y0='0',
        x1='250',
        y1='516.2',
        line=dict(
            width=1,
        )
    )


    outer_line_shape = dict(
        type='line',
        xref='x',
        yref='y',
        x0='200',
        y0='580',
        x1='-200',
        y1='580',
        line=dict(
            width=1,
        )
    )



    outer_arc1_shape = dict(
        type='path',
         xref='x',
        yref='y',
        path='M -200 580 C -217 574, -247 532, -250 516.2',
        line=dict(
            width=1,
        )
    )


    outer_arc2_shape = dict(
        type='path',
         xref='x',
        yref='y',
        path='M 200 580 C 217 574, 247 532, 250 516.2',
        line=dict(
            width=1,
        )
    )


    center_red_line_shape = dict(
        type='line',
        xref='x',
        yref='y',
        x0='-250',
        y0='0',
        x1='250',
        y1='0',
        line=dict(
            width=1,
            color='rgba(255, 0, 0, 1)'
        )
    )


    end_line_shape = dict(
        type='line',
        xref='x',
        yref='y',
        x0='-250',
        y0='516.2',
        x1='250',
        y1='516.2',
        line=dict(
            width=1,
            color='rgba(255, 0, 0, 1)'
        )
    )



    blue_line_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='250',
        y0='150.8',
        x1='-250',
        y1='145',
        line=dict(
            color='rgba(0, 0, 255, 1)',
            width=1
        ),
        fillcolor='rgba(0, 0, 255, 1)'
    )



    center_blue_spot_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='2.94',
                y0='2.8',
                x1='-2.94',
                y1='-2.8',
                line=dict(
                    color='rgba(0, 0, 255, 1)',
                    width=1
                ),
                fillcolor='rgba(0, 0, 255, 1)'
    )



    red_spot1_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='135.5',
                y0='121.8',
                x1='123.5',
                y1='110.2',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )


    red_spot2_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-135.5',
                y0='121.8',
                x1='-123.5',
                y1='110.2',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )


    red_spot1_circle_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='217.6',
                y0='487.2',
                x1='41.2',
                y1='313.2',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )



    red_spot2_circle_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-217.6',
                y0='487.2',
                x1='-41.2',
                y1='313.2',
                line=dict(
                    width=1,
                    color='rgba(255, 0, 0, 1)'
                )
    )


    red_spot21_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='135.5',
                y0='405.1',
                x1='123.5',
                y1='395.3',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )



    red_spot22_shape = dict(
                type='circle',
                xref='x',
                yref='y',
                x0='-135.5',
                y0='405.1',
                x1='-123.5',
                y1='395.3',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                ),
                fillcolor='rgba(255, 0, 0, 1)'
    )


    parallel_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='230',
                y0='416.4',
                x1='217.8',
                y1='416.4',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    parallel_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='230',
                y0='384',
                x1='217.8',
                y1='384',
                line=dict(
                    color='rgba(255, 0, 0, 1)',
                    width=1
                )
    )

    faceoff_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='141.17',
                y0='423.4',
                x1='141.17',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='117.62',
                y0='423.4',
                x1='117.62',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line3_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='153',
                y0='406',
                x1='105.8',
                y1='406',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line4_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='153',
                y0='394.4',
                x1='105.8',
                y1='394.4',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )



    faceoff_line21_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-141.17',
                y0='423.4',
                x1='-141.17',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line22_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-117.62',
                y0='423.4',
                x1='-117.62',
                y1='377',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line23_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-153',
                y0='406',
                x1='-105.8',
                y1='406',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )

    faceoff_line24_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-153',
                y0='394.4',
                x1='-105.8',
                y1='394.4',
                line=dict(
                    color='rgba(10, 10, 100, 1)',
                    width=1
                )
    )


    goal_line1_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='64.7',
                y0='516.2',
                x1='82.3',
                y1='580',
                line=dict(
                    width=1
                )
    )

    goal_line2_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='23.5',
                y0='516.2',
                x1='23.5',
                y1='493',
                line=dict(
                    width=1
                )
    )

    goal_line21_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-64.7',
                y0='516.2',
                x1='-82.3',
                y1='580',
                line=dict(
                    width=1
                )
    )

    goal_line22_shape = dict(
                type='line',
                xref='x',
                yref='y',
                x0='-23.5',
                y0='516.2',
                x1='-23.5',
                y1='493',
                line=dict(
                    width=1
                )
    )


    # mirror images of "goal_line1" and "goal_line2" along with the Y-axis

    goal_arc1_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M 23.5 493 C 20 480, -20 480, -23.5 493',
                line=dict(
                    width=1,
                )
    )

    goal_arc2_shape = dict(
                type='path',
                xref='x',
                yref='y',
                path='M 17.6 516.2 C 15 530, -15 530, -17.6 516.2',
                line=dict(
                    width=1,
                )
    )


    rink_shapes.append(outer_line_shape)
    rink_shapes.append(outer_rect_shape)
    rink_shapes.append(outer_arc1_shape)
    rink_shapes.append(outer_arc2_shape)
    rink_shapes.append(center_red_line_shape)
    rink_shapes.append(end_line_shape)
    rink_shapes.append(blue_line_shape)
    rink_shapes.append(center_blue_spot_shape)
    rink_shapes.append(red_spot1_shape)
    rink_shapes.append(red_spot2_shape)
    rink_shapes.append(red_spot1_circle_shape)
    rink_shapes.append(red_spot2_circle_shape)
    rink_shapes.append(red_spot21_shape)
    rink_shapes.append(red_spot22_shape)
    rink_shapes.append(goal_line1_shape)
    rink_shapes.append(goal_line2_shape)
    rink_shapes.append(goal_line21_shape)
    rink_shapes.append(goal_line22_shape)
    rink_shapes.append(goal_arc1_shape)
    rink_shapes.append(goal_arc2_shape)

    return rink_shapes

def player_graph(season = "2018_2019", player_name = "Sidney Crosby", event_type = "HIT"):
    et = event_type.lower()
    if et == "save":
        et = "shot"
    raw = pd.read_csv("data/{}s_{}.csv".format(et, season), encoding="windows-1252")
    raw.x = abs(raw.x)
    raw.x = raw.x / 100
    raw.x = raw.x * 580
    raw.y = raw.y / 42.5
    raw.y = raw.y * 250
    sub = raw[(raw["gameType"] == "R")]

    # sub.x = abs(sub.x)
    # sub.x = sub.x / 100
    # sub.x = sub.x * 580
    # sub.y = sub.y / 42.5
    # sub.y = sub.y * 250

    if event_type == "HIT":
        sp1 = sub[(sub['hitterName'] == player_name )]
        sp2 = sub[(sub['hitteeName'] == player_name )]
        n1 = "Got hit"
        n2 = "Hits"
        mc1 = 'rgba(0, 0, 250, .8)'
        mc2 = 'rgba(0, 100, 0, .8)'
        event = "Hitting"

    if event_type == "SHOT":
        single_player = sub[(sub['shooterName'] == player_name )]
        sp1 = single_player[(single_player['eventTypeId'] == "SHOT")]
        sp2 = single_player[(single_player['eventTypeId'] == "GOAL")]
        n1 = "shots"
        n2 = "goals"
        mc1 = 'rgba(0, 0, 250, .3)'
        mc2 = 'rgba(0, 100, 0, .8)'
        event = "Shooting"

    if event_type == "SAVE":
        single_player = sub[(sub['goalieName'] == player_name )]
        sp1 = single_player[(single_player['eventTypeId'] == "SHOT")]
        sp2 = single_player[(single_player['eventTypeId'] == "GOAL")]
        n1 = "saves"
        n2 = "goals"
        mc1 = 'rgba(0, 0, 250, .3)'
        mc2 = 'rgba(0, 100, 0, .8)'
        event = "Saving"

    point_trace_1 = go.Scatter(
        x = sp1.y,
        y = sp1.x,
        name = "{}".format(n1),
        mode = 'markers',
        hovertext=sp1.date,
        hoverinfo="text",
        marker = dict(
            size = 5
        ),
        marker_color = mc1
    )

    point_trace_2 = go.Scatter(
        x = sp2.y,
        y = sp2.x,
        name = "{}".format(n2),
        mode = 'markers',
        hovertext=sp2.date,
        hoverinfo="text",
        marker = dict(
            size = 5
        ),
        marker_color = mc2
    )

    data = [point_trace_1, point_trace_2]
    # data2 = [point_trace_hitee]

    rink_shapes = generate_rink_shapes()

    layout = go.Layout(
        shapes=rink_shapes,
        title = "{} {} {}".format(season, player_name, event),
        width = 500,
        height = 600
    )

    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


season, player_name, event_type = parse_command_line()
print(season)
print(player_name)
print(event_type)

player_graph(season, player_name, event_type)

# if event_type == "Sho"
