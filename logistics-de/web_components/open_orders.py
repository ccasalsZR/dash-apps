

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

def oo_created_today():

    fig = go.Figure(go.Indicator(
        mode="number",
        value=0, #df['Page Views'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 40, 'color': '#a6b3b0'},
            'valueformat': ",.0f",
        },
    ))
    fig.update_layout(
        height=150,
    )

    return fig