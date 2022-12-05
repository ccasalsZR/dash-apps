
from random import random
from dash import html, callback, Output, Input, dcc

import os
from dotenv import load_dotenv
import snowflake.connector as snow


import dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta


# from web_sections import , main_2_conversion, main_3_teleclinic, main_4_marketing
import web_sections as ws


dash.register_page(
    __name__,
    path='/',
    title='Sandoz Hexal - DocMorris Analytics'
) # Home page


# The layout it's inside a function so everytime it load the page we load 
# again the layout so we can have dynamic values for the time-picker element
def layout(): 
    return html.Div([
    html.Br(),
    dbc.Container([
        
        # MARKETING CAMPAING ------------------------------------------------------------
        dbc.Row([
            dbc.Col([
                html.H1("Marketing Campaign"),
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
            # dbc.Col([
            #     html.P('Spend'),
            #     dcc.Loading(
            #         id='loading-6',
            #         children=[dcc.Graph(id='spend-1',figure={})],
            #         type='dot',color='#22594C'
            #     ), 
            # ],class_name='grid_box'),
            dbc.Col([
                # html.P('CPM'),
                # dcc.Loading(
                #     id='loading-7',
                #     children=[dcc.Graph(id='cpm-1',figure={})],
                #     type='dot',color='#22594C'
                # ), 
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
                # html.P('Cost per Click'),
                # dcc.Loading(
                #     id='loading-10',
                #     children=[dcc.Graph(id='cost_per_click-1',figure={})],
                #     type='dot',color='#22594C'
                # ), 
                html.P('Clicks'),
                dcc.Loading(
                    id='loading-11',
                    children=[dcc.Graph(id='clicks-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),

        html.Br(),
        # ENGAGEMENT SECTION --------------------------------------------------------------
        dbc.Row([
            dbc.Col([
                html.H1('Engagement')
            ]),
            dbc.Col([
                dcc.Dropdown(
                    id='my-multi-dropdown-campaign',
                    options=['ED', 'Thyroids'],
                    value=['ED', 'Thyroids'],
                    multi=True
                , style= {'hight':'200px', 'width':'300px','margin-right':'10px'}),
            ], style= {'display':'flex', 'align-items':'right'}, className= 'flex-row-reverse')
        ]),

        dbc.Row([
            dbc.Col([
                html.P('Sessions',id='tt_sessions'),
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='ga_sessions',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box'),            
            dbc.Col([                
                html.P('Active Users',id='tt_activeUsers'),
                dcc.Loading(
                    id='loading-3',
                    children=[dcc.Graph(id='ga_unique_users',figure={})],
                    type='dot',color='#22594C'
                ),                 
            ],class_name='grid_box'),
            dbc.Col([           
                html.P('New Users',id='tt_newUsers'),
                dcc.Loading(
                    id='loading-2',
                    children=[dcc.Graph(id='ga_newUsers',figure={})],
                    type='dot',color='#22594C'
                ),                
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Page Views',id='tt_page_View'),
                dcc.Loading(
                    id='loading-15',
                    children=[dcc.Graph(id='page_views-1',figure={})],
                    type='dot',color='#22594C'
                ),                
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Avg. Session Duration',id='tt_avgSessionDuration'),
                dcc.Loading(
                    id='loading-16',
                    children=[dcc.Graph(id='avg_session_duration-1',figure={})],
                    type='dot',color='#22594C'
                ),                
            ],class_name='grid_box'),
        ]),
        dbc.Tooltip(
            "The number of sessions that began on your site or app.",
            target="tt_sessions",
            placement='auto',
        ),
        dbc.Tooltip(
            "The number of users who interacted with your site or launched your app for the first time.",
            target="tt_newUsers",
            placement='auto',        
        ),
        dbc.Tooltip(
            "The number of distinct users who visited your site or app.",
            target="tt_activeUsers",
            placement='auto',        
        ),
        dbc.Tooltip(
            "The number of app screens or web pages your users viewed. Repeated views of a single page or screen are counted.",
            target="tt_page_View",
            placement='auto',        
        ),
        dbc.Tooltip(
            "The average duration (in seconds) of users' sessions.",            
            target="tt_avgSessionDuration",
            placement='auto',        
        ),
        dbc.Row([
            dbc.Col([
                html.P('Evolution of activity'),
                dcc.Loading(
                    id='loading-4',
                    children=[dcc.Graph(id='ga_evolution_chart',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box',width=8),
            dbc.Col([
                html.P('Share of users'),
                dcc.Loading(
                    id='loading-41',
                    children=[dcc.Graph(id='ga_users_donut',figure={})],
                    type='dot',color='#22594C'
                ),
            ],class_name='grid_box')
        ]),
        html.Br(),
        # CONVERSION --------------------------------------------------------------------
        html.H1('Conversion'),
        dbc.Row([
            dbc.Col([
                dbc.Col([
                    html.P('Clickouts to TC',style={'padding-left':'4px'}),
                    dcc.Loading(
                        id='loading-5',
                        children=[dcc.Graph(id='conversion-kpi-1',figure={})],
                        type='dot',color='#22594C'
                    ), 
                ],class_name='grid_box'),
                dbc.Col([
                    html.P('Clickouts to "116117"',style={'padding-left':'4px'}),
                    dcc.Loading(
                        id='loading-6',
                        children=[dcc.Graph(id='conversion-kpi-2',figure={})],
                        type='dot',color='#22594C'
                    ), 
                ],class_name='grid_box'),
            ], width= 3, style={'padding':'0px'}),
            dbc.Col([
                html.P('Questionnaire'),
                dcc.Loading(
                    id='loading-7',
                    children=[dcc.Graph(id='barchart_questionnaire',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                dbc.Col([
                    html.P('Downloads',style={'padding-left':'4px'}),
                    dcc.Loading(
                        id='loading-5',
                        children=[dcc.Graph(id='donwload_pdf',figure={})],
                        type='dot',color='#22594C'
                    ), 
                ],class_name='grid_box'),
                dbc.Col([
                    html.P('Video plays',style={'padding-left':'4px'}),
                    dcc.Loading(
                        id='loading-6',
                        children=[dcc.Graph(id='video_start',figure={})],
                        type='dot',color='#22594C'
                    ), 
                ],class_name='grid_box'),
            ], width= 3, style={'padding':'0px'}),
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
                html.P('Active Users'),
                dcc.Loading(
                    id='loading-13',
                    children=[dcc.Graph(id='users-2',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('New Users'),
                dcc.Loading(
                    id='loading-14',
                    children=[dcc.Graph(id='new_users-1',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),
        
        
    ]),
    html.Br()
])



@callback(
    # GA4 ENGAGEMENT + CONVERSION
    Output('ga_sessions', 'figure'),
    Output('ga_newUsers', 'figure'),
    Output('ga_unique_users', 'figure'),
    Output('page_views-1', 'figure'),    
    Output('avg_session_duration-1', 'figure'),    
    Output('ga_evolution_chart', 'figure'),
    Output('ga_users_donut', 'figure'),
    

    Output('conversion-kpi-1', 'figure'),
    Output('conversion-kpi-2', 'figure'),
    Output('donwload_pdf', 'figure'),
    Output('video_start', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('my-multi-dropdown-campaign', 'value')
    
    )

def update_engagement_conversion(start_date,end_date,value):

    engagement = ws.update_main_sec1(start_date,end_date,value)

    # Extract the stored value
    act_users = engagement[7] 
    conversion = ws.update_main_sec2(start_date,end_date,act_users,value)
    
    
    return [engagement[0],engagement[1],engagement[2],engagement[3],engagement[4],engagement[5],engagement[6],
        conversion[0],conversion[1], conversion[2], conversion[3]
    ]


@callback (
    
    Output('barchart_questionnaire', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('my-multi-dropdown-campaign', 'value')
)

def update_questionnaire(start_date,end_date,value):
    return ws.questionnare(start_date,end_date,value)

@callback (
    # MARKETING CAMPAING ------------------------------------------------------------
    # Output('spend-1', 'figure'),
    # Output('cpm-1', 'figure'),
    Output('impressions-1', 'figure'),
    Output('ctr-1', 'figure'),
    # Output('cost_per_click-1', 'figure'),
    Output('clicks-1', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),

)
def update_marketing(start_date,end_date):

    marketing = ws.get_marketing_data(start_date,end_date)


    return [ # marketing[0],
        # marketing[1],
        marketing[2],
        marketing[3],
        # marketing[4],
        marketing[5]
    ]

@callback (
    # TELECLINIC --------------------------------------------------------------------
    Output('Sessions-2', 'figure'),
    Output('users-2', 'figure'),
    Output('new_users-1', 'figure'),

    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('my-multi-dropdown-campaign', 'value')
    
)

def update_multi_sel(start_date,end_date,value):
    
    teleclinic = ws.get_teleclinic_ga_insigts(start_date,end_date,value)

    return teleclinic[0],teleclinic[1],teleclinic[2],
