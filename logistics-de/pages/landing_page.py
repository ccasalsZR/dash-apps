


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
    dcc.Interval(
        id="load_interval", 
        n_intervals=0, 
        max_intervals=0, #<-- only run once
        interval=1
    ),
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
                    html.P('Backlog orders', id='tt_backlog_orders')
                    ],href='/backlog-monitor'
                ),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_open_orders_today',figure={})
                    ]
                    ,type='dot',color='#22594C'
                ),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='chart_hist_open_orders',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Retention Rate')
            ],class_name='grid_box'),
        ]),
        dbc.Tooltip(
            "The number of total open orders.",
            target="tt_backlog_orders",
            placement='auto',
        ),

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


@callback(
    Output('kpi_open_orders_today','figure'),
    Output('chart_hist_open_orders','figure'),

    Input('load_interval','n_intervals')
)
def update_open_orders(n_intervals):

    df = wc.execute_query('scripts/open_orders_created.sql')
    # kpi_open_orders = df[df['backlog_day_cat'] == 'Day 0'] # Today
    fig_kpi = wc.kpi_template(df['open_orders'].sum())

    df = wc.execute_query('scripts/hist_open_orders.sql')
    fig_chart = wc.hist_open_orders(df)
        
    return fig_kpi, fig_chart