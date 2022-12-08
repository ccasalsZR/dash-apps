

from random import random
from dash import html, callback, Output, Input, dcc


import os
# from dotenv import load_dotenv
# import snowflake.connector as snow


import dash, dash_table
from dash.dash_table.Format import Format, Scheme, Trim
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

from dotenv import load_dotenv
load_dotenv()


import web_components as wc


dash.register_page(
    __name__,
    path='/',
    title='Logistics DE'
) # Home page


# # MAIN EXTRACT TO WORK WITH THE LOCAL FILES ------------------

DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')
DB_SNOW_USER = os.getenv('DB_SNOW_USER')



def load_datasets():

    dff = []

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
        query = open('scripts/open_orders_created.sql', 'r').read()
        df = pd.read_sql_query(query, engine)
        dff.append(df)

        query = open('scripts/backlog_EWM_logistics.sql', 'r').read()
        df = pd.read_sql_query(query, engine)
        dff.append(df)

        query = open('scripts/pta_clearance.sql', 'r').read()
        df = pd.read_sql_query(query, engine)
        dff.append(df)

        query = open('scripts/amount_failed.sql', 'r').read()
        df = pd.read_sql_query(query, engine)
        dff.append(df)

    finally:
        connection.close()
        engine.dispose()

    return dff

# Since there's no input we change the layout to be a function so we can load
#  new data with every-refresh
def layout():
    
    ds = load_datasets()

    df_1 = ds[0].copy()
    fig_backorder = wc.kpi_template(df_1['backorder'].sum())

    kpi_open_orders = df_1[df_1['is_today'] == True]
    fig_created_today = wc.kpi_template(kpi_open_orders['open_orders'].sum())

    kpi_open_before_orders = df_1[df_1['is_today'] == False]
    fig_created_before_today = wc.kpi_template(kpi_open_before_orders['open_orders'].sum())

    df_2 = ds[1].copy()
    fig_in_logistics = wc.kpi_template(df_2['in_logistics'].sum())
    fig_backlog_ewm = wc.kpi_template(df_2['backlog_ewm'].sum())
    fig_sent_today = wc.kpi_template(df_2['sent_today'].sum())
    fig_crossdock_starter = wc.kpi_template(df_2['crossdock_starter'].sum())

    df_3 = ds[2].copy() # pta_clerance
    fig_pta_clearance = wc.kpi_template(df_3['pta_clearance'].sum())

    df_4 = ds[3].copy() # amount_failed
    fig_amount_failed = wc.kpi_template(df_4['amount_failed'].sum())

    fig_backlog_erp = wc.kpi_template(0)
    fig_failed_orders = wc.kpi_template(0)
    fig_not_processed = wc.kpi_template(0)
    fig_ready_logistics = wc.kpi_template(0)
    fig_ready_WAMAS = wc.kpi_template(df_2['backlog_ewm'].sum() - df_4['amount_failed'].sum() - df_2['crossdock_starter'].sum())

    

    
    return html.Div([
    dbc.Container([
        html.Br(),
        dbc.Row([
            html.H3('DCA Order Flow',className='h3-sub'),
        ]),
        html.Hr(),
        dbc.Row([
            # Created Today
            dbc.Col([
                html.P('Created Today'),
                dcc.Graph(id='kpi_created_today',figure=fig_created_today)
            ],class_name='grid_box'),
            # Backlog ERP
            dbc.Col([
                html.P('Backlog ERP'),
                dcc.Graph(id='kpi_backlog_erp',figure=fig_backlog_erp)
            ],class_name='grid_box'),
            #  Backlog EWM
            dbc.Col([
                html.P('Backlog EWM'),
                dcc.Graph(id='kpi_backlog_ewm',figure=fig_backlog_ewm)
            ],class_name='grid_box'),
            # Ready for logistics
            dbc.Col([
                html.P('Ready for Logistics'),
                dcc.Graph(id='kpi_ready_logistics',figure=fig_ready_logistics)
            ],class_name='grid_box'),
            # In Logistics
            dbc.Col([
                html.P('In Logistics'),
                dcc.Graph(id='kpi_IN_logistics',figure=fig_in_logistics)
            ],class_name='grid_box'),
            # Sent today
            dbc.Col([
                html.P('Sent today'),
                dcc.Graph(id='kpi_sent_today',figure=fig_sent_today)
            ],class_name='grid_box'),
            
        ]),
        dbc.Row([
            dbc.Col([
                html.P('Created Before Today'),
                dcc.Graph(id='kpi_created_today',figure=fig_created_before_today)
            ],class_name='grid_box'),
            dbc.Col([
                html.P('In PTA aprroval'),
                dcc.Graph(id='kpi_created_today',figure=fig_pta_clearance)
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Crossdock starter'),
                dcc.Graph(id='kpi_created_today',figure=fig_crossdock_starter)
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Back Order'),
                dcc.Graph(id='kpi_created_today',figure=fig_backorder)
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Failed'),
                dcc.Graph(id='kpi_created_today',figure=fig_amount_failed)
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Failed Orders'),
                dcc.Graph(id='kpi_created_today',figure=fig_failed_orders)
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Ready for WAMAS'),
                dcc.Graph(id='kpi_created_today',figure=fig_ready_WAMAS)
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Not Processed'),
                dcc.Graph(id='kpi_created_today',figure=fig_not_processed)
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
    ]),
    html.Br()
])


# callback([

# ])
# def update_open_orders():

    

#     return