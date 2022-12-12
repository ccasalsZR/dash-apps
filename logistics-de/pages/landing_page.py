


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
    title='Customer Journey'
) # Home page



layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4('Channel'),
            ]),
            dbc.Col([
                html.H4('Customer Base')
            ]),
            dbc.Col([
                html.H4('Orders & Sales')
            ]),
            dbc.Col([
                html.H4('Ship & Deliver')
            ]),
            dbc.Col([
                html.H4('Retention')
            ]),
        ]),

        # Row 1
        dbc.Row([
            dbc.Col([
                html.P('Digital / Traditional'),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Split by RFM (Regency, Frequency, Monetization)')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Category Management')
            ],class_name='grid_box'),
            dbc.Col([
                html.A([
                    html.P('Backlog xyz orders')
                    ],href='/backlog-monitor'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Retention Rate')
            ],class_name='grid_box'),
        ]),

         # Row 2
        dbc.Row([
            dbc.Col([
                html.P('New / Return'),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Cohorts')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Numbers of orders')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Availability')
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
        ]),

         # Row 3
        dbc.Row([
            dbc.Col([
                html.P('Web / Mobile'),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Segments')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Net Sales')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Click to delivery')
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
        ]),

        # Row 4
        dbc.Row([
            dbc.Col([
                html.P('Call / Mail-order / Post'),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Category')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Margin')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Returns')
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
        ]),

        # Row 5
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Basket size')
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Complaints')
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
        ]),

        # Row 6
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),            
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Carrier')
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
        ]),

        dbc.Row([
            dbc.Col([
                html.H6('How do customers interact with us?'),
            ]),
            dbc.Col([
                html.H6('Who are our customers?')
            ]),
            dbc.Col([
                html.H6('What and how much do they buy?')
            ]),
            dbc.Col([
                html.H6('How do we serve them?')
            ]),
            dbc.Col([
                html.H6('Do they come back?')
            ]),
        ]),
    ]),
])