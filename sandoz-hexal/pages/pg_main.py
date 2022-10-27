
from random import random
from dash import html, callback, Output, Input, dcc

import os
from dotenv import load_dotenv
# import snowflake.connector as snow


import dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date


from web_sections import main_sec1, main_sec2


dash.register_page(
    __name__,
    path='/',
    title='Sandox Hexal - DocMorris Analytics'
) # Home page

layout = html.Div([
    html.Br(),
    dbc.Container([
        # ENGAGEMENT SECTION --------------------------------------------------------------
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
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='ga_sessions',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            
            dbc.Col([
                html.P('New Users'),
                dcc.Loading(
                    id='loading-2',
                    children=[dcc.Graph(id='ga_visits',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Active Users'),
                dcc.Loading(
                    id='loading-3',
                    children=[dcc.Graph(id='ga_unique_users',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box')
        ]),
        dbc.Row([
            dbc.Col([
                html.P('Evolution of activity'),
                dcc.Loading(
                    id='loading-4',
                    children=[dcc.Graph(id='ga_evolution_chart',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box')
        ]),
        html.Br(),
        # CONVERSION --------------------------------------------------------------------
        html.H1('Conversion'),
        dbc.Row([
            dbc.Col([
                html.P('Clickouts to TC'),
                dcc.Loading(
                    id='loading-5',
                    children=[dcc.Graph(id='conversion-kpi-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Clickouts to "116117"'),
                dcc.Loading(
                    id='loading-6',
                    children=[dcc.Graph(id='conversion-kpi-2',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Questionnaire'),
                dcc.Loading(
                    id='loading-7',
                    children=[dcc.Graph(id='conversion-kpi-3',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),
        html.Br(),
        # TELECLINIC CONVERSION ---------------------------------------------------------
        html.H1('Teleclinic Conv.'),
    ]),
    html.Br()
])

@callback(
    Output('ga_sessions', 'figure'),
    Output('ga_visits', 'figure'),
    Output('ga_unique_users', 'figure'),
    Output('ga_evolution_chart', 'figure'),

    Output('conversion-kpi-1', 'figure'),
    Output('conversion-kpi-2', 'figure'),
    Output('conversion-kpi-3', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_graph(start_date,end_date):

    engagement = main_sec1.update_main_sec1(start_date,end_date)
    conversion = main_sec2.update_main_sec2()

    
    return [engagement[0],engagement[1],engagement[2],engagement[3],
        conversion[0],conversion[1],conversion[2]
    ]

