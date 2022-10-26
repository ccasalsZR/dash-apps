
from random import random
from dash import html, callback, Output, Input, dcc

import os
from dotenv import load_dotenv
# import snowflake.connector as snow


import dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date


from web_sections import main_sec1


dash.register_page(
    __name__,
    path='/',
    title='Vital Signs'
) # Home page

layout = html.Div([
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('Engagement'),
            ]) ,           
            dbc.Col([
                 dcc.DatePickerRange(
                    id='my-date-picker-range',
                    start_date=date(2022, 10, 1),
                    end_date=date(2022, 10, 26)
                ),
            ], style= {'display':'flex', 'align-items':'right'}, className= 'flex-row-reverse')
        ]),
        dbc.Row([
            dbc.Col([
                html.P('Sessions'),
                dcc.Graph(id='ga_sessions',figure={})
            ],class_name='grid_box'),
            
            dbc.Col([
                html.P('New Users'),
                dcc.Graph(id='ga_visits',figure={})
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Active Users'),
                dcc.Graph(id='ga_unique_users',figure={})
            ],class_name='grid_box')
        ]),
        html.Br(),
        html.H1('Conversion'),
        html.Br(),
        html.H1('Teleclinic Conv.'),
    ]),
    html.Br()
])

@callback(
    Output('ga_sessions', 'figure'),
    Output('ga_visits', 'figure'),
    Output('ga_unique_users', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_graph(start_date,end_date):

    print(start_date)
    print(end_date)

    el1 = main_sec1.update_main_sec1(start_date,end_date)
    
    return el1[0],el1[1],el1[2]

