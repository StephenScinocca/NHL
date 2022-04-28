import pandas as pd
from pprint import pprint
import numpy as np

import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode()

    #list containing all the shapes
def init_rink():

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
    #rink_shapes.append(parallel_line1_shape)
    #rink_shapes.append(parallel_line2_shape)
    #rink_shapes.append(faceoff_line1_shape)
    #rink_shapes.append(faceoff_line2_shape)
    #rink_shapes.append(faceoff_line3_shape)
    #rink_shapes.append(faceoff_line4_shape)
    #rink_shapes.append(faceoff_line21_shape)
    #rink_shapes.append(faceoff_line22_shape)
    #rink_shapes.append(faceoff_line23_shape)
    #rink_shapes.append(faceoff_line24_shape)
    rink_shapes.append(goal_line1_shape)
    rink_shapes.append(goal_line2_shape)
    rink_shapes.append(goal_line21_shape)
    rink_shapes.append(goal_line22_shape)
    rink_shapes.append(goal_arc1_shape)
    rink_shapes.append(goal_arc2_shape)

    return rink_shapes
