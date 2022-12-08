

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

def kpi_template(value_disp):

    fig = go.Figure(go.Indicator(
        mode="number",
        value=value_disp,
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 40, 'color': '#22594c'},
            'valueformat': ",.0f",
        },
    ))
    fig.update_layout(
        height=100,
    )

    return fig


