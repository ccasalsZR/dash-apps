

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
    path='/backlog-monitor',
    title='Logistics DE'
) # Home page


# # MAIN EXTRACT TO WORK WITH THE LOCAL FILES ------------------

# DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')
# DB_SNOW_USER = os.getenv('DB_SNOW_USER')

# engine = create_engine(URL(
#         account = 'docmorris.eu-central-1',
#         user = DB_SNOW_USER,
#         password = DB_SNOW_PASS,
#         database = 'EDW',
#         # schema = 'public',
#         warehouse = 'WH_TABLEAU',
#         # role='myrole',
#     ))
# try:
#     connection = engine.connect()
#     query = open('scripts/legal_view.sql', 'r').read()
#     df = pd.read_sql_query(query, engine)

# finally:
#     connection.close()
#     engine.dispose()


# Since there's no input we change the layout to be a function so we can load
#  new data with every-refresh
def layout():
    
    fig_created_today = wc.oo_created_today()
    
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
                dcc.Graph(id='kpi_backlog_erp',figure=fig_created_today)
            ],class_name='grid_box'),
            #  Backlog EWM
            dbc.Col([
                html.P('Backlog EWM'),
                dcc.Graph(id='kpi_backlog_ewm',figure=fig_created_today)
            ],class_name='grid_box'),
            # Ready for logistics
            dbc.Col([
                html.P('Ready for Logistics'),
                dcc.Graph(id='kpi_ready_logistics',figure=fig_created_today)
            ],class_name='grid_box'),
            # In Logistics
            dbc.Col([
                html.P('In Logistics'),
                dcc.Graph(id='kpi_IN_logistics',figure=fig_created_today)
            ],class_name='grid_box'),
            # Sent today
            dbc.Col([
                html.P('Sent today'),
                dcc.Graph(id='kpi_sent_today',figure=fig_created_today)
            ],class_name='grid_box'),
            
        ]),
    ]),
    html.Br()
])


# callback([

# ])
# def update_open_orders():

    

#     return