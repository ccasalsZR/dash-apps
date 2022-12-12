

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


def open_order_chart(df):

    chart = px.bar(
        df,
        x='open_orders',
        y='backlog_day_cat',
        color_discrete_sequence = ['#22594C']
    )
    chart.update_layout(
        plot_bgcolor='#fff'
    )

    return chart