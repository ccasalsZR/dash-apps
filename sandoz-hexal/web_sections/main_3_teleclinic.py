#!/usr/bin/virt python

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

import os
from dotenv import load_dotenv
import snowflake.connector as snow

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

load_dotenv()

DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')
DB_SNOW_USER = os.getenv('DB_SNOW_USER')


def run_snowflake_queries(start_date,end_date):


    engine = create_engine(URL(
        account = 'docmorris.eu-central-1',
        user = DB_SNOW_USER,
        password = DB_SNOW_PASS,
        database = 'ECOSYSTEM_PROD',
        # schema = 'public',
        warehouse = 'WH_ECOSYSTEM_DEV',
        # role='myrole',
    ))
    try:
        connection = engine.connect()
        query = open('scripts/teleclinic_ga.sql', 'r').read().replace('%start_date%',start_date)
        query = query.replace('%end_date%',end_date)
        df = pd.read_sql_query(query, engine)

    finally:
        connection.close()
        engine.dispose()

    return df



def get_teleclinic_ga_insigts(start_date,end_date,campaign_selected):


    df = run_snowflake_queries(start_date,end_date)

    
    map_campaign = {
        '2417-docmorris-care-schilddruese':'Thyroids',
        '2430-docmorris-care-ed-asynchron':'ED'
    }

    df['campaing_mapped'] = df['Campaign'].map(map_campaign)
    
    if len(campaign_selected) > 0:
        df = df[df['campaing_mapped'].isin(campaign_selected)]


    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=df['sessions'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig1.update_layout(
        height=120,
    )

    fig2 = go.Figure(go.Indicator(
        mode="number",
        value=df['users'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig2.update_layout(
        height=120,
    )

    fig3 = go.Figure(go.Indicator(
        mode="number",
        value=df['new_users'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=120,
    )

    return [fig1,fig2,fig3]
    # return


# get_teleclinic_ga_insigts('2022-10-01','2022-11-01',['ED'])