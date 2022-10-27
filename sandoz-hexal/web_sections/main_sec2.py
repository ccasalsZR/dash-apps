

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd


def update_main_sec2():

    fig1 = go.Figure(go.Indicator(
        mode="number+delta",
        value=20000,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 22000, 'relative': True, 'position' : "right", "valueformat": ".2%"},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig1.update_layout(
        height=100,
    )

    fig2 = go.Figure(go.Indicator(
        mode="number+delta",
        value=20000,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 20030, 'relative': True, 'position' : "right", "valueformat": ".2%"},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig2.update_layout(
        height=100,
    )

    fig3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=20000,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 19000, 'relative': True, 'position' : "right", "valueformat": ".2%"},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=100,
    )

    return fig1, fig2, fig3