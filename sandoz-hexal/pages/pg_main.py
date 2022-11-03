
from random import random
from dash import html, callback, Output, Input, dcc

import os
from dotenv import load_dotenv
import snowflake.connector as snow


import dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta


from web_sections import main_1_engagement, main_2_conversion, main_3_teleclinic, main_4_marketing


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
                    start_date=date(date.today().year, date.today().month-1, date.today().day),
                    end_date=date.today() + timedelta(days=-1)
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
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Page Views'),
                dcc.Loading(
                    id='loading-15',
                    children=[dcc.Graph(id='page_views-1',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Avg. Session Duration'),
                dcc.Loading(
                    id='loading-16',
                    children=[dcc.Graph(id='avg_session_duration-1',figure={})],
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
        dbc.Row([
            dbc.Col([
                html.P('Sessions'),
                dcc.Loading(
                    id='loading-12',
                    children=[dcc.Graph(id='Sessions-2',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Users'),
                dcc.Loading(
                    id='loading-13',
                    children=[dcc.Graph(id='users-2',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Page Views'),
                dcc.Loading(
                    id='loading-14',
                    children=[dcc.Graph(id='new_users-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),
        
        html.Br(),
        # MARKETING CAMPAING ------------------------------------------------------------
        html.H1("Marketing Campaign"),
        dbc.Row([
            dbc.Col([
                html.P('Spend'),
                dcc.Loading(
                    id='loading-6',
                    children=[dcc.Graph(id='spend-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('CPM'),
                dcc.Loading(
                    id='loading-7',
                    children=[dcc.Graph(id='cpm-1',figure={})],
                    type='dot',color='#22594C'
                ), 
                html.P('Impressions'),
                dcc.Loading(
                    id='loading-8',
                    children=[dcc.Graph(id='impressions-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('CTR'),
                dcc.Loading(
                    id='loading-9',
                    children=[dcc.Graph(id='ctr-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Cost per Click'),
                dcc.Loading(
                    id='loading-10',
                    children=[dcc.Graph(id='cost_per_click-1',figure={})],
                    type='dot',color='#22594C'
                ), 
                html.P('Clicks'),
                dcc.Loading(
                    id='loading-11',
                    children=[dcc.Graph(id='clicks-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),
    ]),
    html.Br()
])

@callback(
    Output('ga_sessions', 'figure'),
    Output('ga_visits', 'figure'),
    Output('ga_unique_users', 'figure'),
    Output('page_views-1', 'figure'),    
    Output('avg_session_duration-1', 'figure'),    
    Output('ga_evolution_chart', 'figure'),

    Output('conversion-kpi-1', 'figure'),
    Output('conversion-kpi-2', 'figure'),
    Output('conversion-kpi-3', 'figure'),

    # TELECLINIC --------------------------------------------------------------------
    Output('Sessions-2', 'figure'),
    Output('users-2', 'figure'),
    Output('new_users-1', 'figure'),

    # MARKETING CAMPAING ------------------------------------------------------------
    Output('spend-1', 'figure'),
    Output('cpm-1', 'figure'),
    Output('impressions-1', 'figure'),
    Output('ctr-1', 'figure'),
    Output('cost_per_click-1', 'figure'),
    Output('clicks-1', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_graph(start_date,end_date):

    engagement = main_1_engagement.update_main_sec1(start_date,end_date)
    conversion = main_2_conversion.update_main_sec2()

    teleclinic = main_3_teleclinic.get_teleclinic_ga_insigts(start_date,end_date)

    marketing = main_4_marketing.get_marketing_data(start_date,end_date)

    
    return [engagement[0],engagement[1],engagement[2],engagement[3],engagement[4],engagement[5],
        conversion[0],conversion[1],conversion[2],
        teleclinic[0],teleclinic[1],teleclinic[2],
        marketing[0],marketing[1],marketing[2],marketing[3],marketing[4],marketing[5]
    ]

