

import plotly.express as px
import plotly.graph_objects as go

import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL


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

def hist_open_orders(df):

    chart = px.line(
        df,
        x='eod_dt',
        y='open_orders',
        color_discrete_sequence = ['#22594C']
    )
    chart.update_layout(
        plot_bgcolor='#fff',
        yaxis={'title': None},
        xaxis={'title': None, 'visible': False},
        margin=dict(l=10, r=10, t=20, b=10),
        height=200,
    )
    # chart.show(config=dict(displayModeBar=False))

    return chart

DB_SNOW_USER = os.getenv('DB_SNOW_USER')
DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')

def execute_query(script):
    engine = create_engine(URL(
            account = 'docmorris.eu-central-1',
            user = DB_SNOW_USER,
            password = DB_SNOW_PASS,
            database = 'EDW',
            # schema = 'public',
            warehouse = 'WH_TABLEAU',
            # role='myrole',
        ))
    try:
        connection = engine.connect()
        query = open(script, 'r').read()        
        df = pd.read_sql_query(query, engine)
    finally:
        connection.close()
        engine.dispose()
    return df