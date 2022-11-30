

from random import random
from dash import html, callback, Output, Input, dcc
import dash_daq as daq

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

# MAIN EXTRACT TO WORK WITH THE LOCAL FILES ------------------

# DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')
# DB_SNOW_USER = os.getenv('DB_SNOW_USER')

# engine = create_engine(URL(
#         account = 'jt36375.eu-central-1',
#         user = DB_SNOW_USER,
#         password = DB_SNOW_PASS,
#         database = 'DATAHUB',
#         # schema = 'public',
#         warehouse = 'X_SMALL_WH',
#         # role='myrole',
#     ))
# try:
#     connection = engine.connect()
#     query = open('scripts/legal_view.sql', 'r').read()
#     df = pd.read_sql_query(query, engine)

# finally:
#     connection.close()
#     engine.dispose()


# df.to_csv('legal_view_extract.csv')

# ----------------------------------------------------------------

# df = pd.read_csv('legal_view_extract.csv')
df = pd.read_csv('legal_kpi.csv')

# print(df)


dict_month_sel = {
    '2022-01-01':'Jan 2022',
    '2022-02-01':'Feb 2022',
    '2022-03-01':'Mar 2022',
    '2022-04-01':'Apr 2022',
    '2022-05-01':'May 2022',
    '2022-06-01':'Jun 2022',
    '2022-07-01':'Jul 2022',
    '2022-08-01':'Ago 2022',
    '2022-09-01':'Sep 2022',
    '2022-10-01':'Oct 2022'
}

d = {'SEGMENT':['Group','CH','DE','EU','Corp.']}
df_dropdown = pd.DataFrame(data=d)

dash.register_page(
    __name__,
    path='/',
    title='Investors Relations'
) # Home page


global last_segment_sel
last_segment_sel = 'not_working'

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3('Monthly View',className='h3-sub'),
            ]),            
            dbc.Col([
                dcc.Dropdown(id="slct_segment",
                                options=[x for x in df_dropdown['SEGMENT'].unique()],
                                multi=False,
                                value='Group',
                                style={'width': '150px' }
                                ),
            ], style= {'display':'flex', 'align-items':'right'}, className= 'flex-row-reverse')
        ],style={'margin-top':'10px'}),
        dbc.Row([
            dbc.Col([
                html.P('External Revenue'),
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='external_revenue',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
            dbc.Col([
                html.P('EBITDA Adjusted'),
                dcc.Loading(
                    id='loading-1',
                    children=[dcc.Graph(id='ebitda_adjusted',figure={})],
                    type='dot',color='#22594C'
                ), 
            ],class_name='grid_box'),
        ]),       
        html.Br(),  
        dbc.Row([
            dbc.Col([
                html.H3('Legal View',className='h3-sub'),
            ]),
            dbc.Col([
                html.P('Monthly', style={'padding-right':'5px'}),
                daq.BooleanSwitch(
                    id='boolean_switch',
                    on=True,
                    color="#22594C",
                ),
                html.P('Cumulative',style={'padding-left':'5px'}),
            ], class_name="d-flex justify-content-end")
        ]),        
        html.Br(),   
        dbc.Row([
            dcc.RangeSlider(
                id= 'range_slider_1',
                min=0,
                max=16,
                step=None,
                marks = {
                    0: 'Sep 21',
                    1: 'Oct 21',
                    2: 'Nov 21',
                    3: 'Dec 21',
                    4: 'Jan 22',
                    5: 'Feb 22',
                    6: 'Mar 22',
                    7: 'Apr 22',
                    8: 'May 22',
                    9: 'Jun 22',
                    10: 'Jul 22',
                    11: 'Aug 22',
                    12: 'Sep 22',
                    13: 'Oct 22',
                    14: 'Nov 22',
                    15: 'Dec 22',
                },
                value=[4, 12],
            ),
        ],style={'padding-bottom':'25px'}),
        dbc.Row([
            dcc.Loading(
                id='loading-1',
                children=[
                    html.Div(id = 'div_table_2',
                        children = [],
                    ),
                ],
                type='dot',color='#22594C'
            ),
        ]),
    ]), 
    html.Br(), 
])

@callback(
    Output('external_revenue', 'figure'),
    Output('ebitda_adjusted', 'figure'),

    Output('div_table_2', 'children'),

    Input('slct_segment', 'value'),       
    Input('boolean_switch', 'on'),   
    Input('range_slider_1', 'value'),   

)

def update_graph(option_segment,switch,month_slide):

    range_month = []
    for n in month_slide:
        if n < 4: # is 2021
            range_month.append('2021-'+ str("{:02d}".format(n+9)) +'-01')
        elif n < (4+12): # is 2022
            range_month.append('2022-'+ str("{:02d}".format(n-3)) +'-01')



    dff = df.copy()
    dff = dff[dff['segment'] == option_segment]
    dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')
    

    mc = wc.monthly_chart(dff)

    
    dashT = wc.dynamic_data_table(dff,range_month[0],range_month[1],switch)
   
    return (mc[0],mc[1],
        dashT
    )

# # A-SYNC call > so we don't trigger an event uppon refresh
# @callback(
   
#     Output("download-dataframe-csv", "data"),

#     Input('slct_segment', 'value'),    
#     Input('slct_month', 'value'),       
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )

# def update_async(option_segment,month_sel,n_clicks):

#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         month_map = None
#         for key, value in dict_month_sel.items():  
#             if value == month_sel:
#                 month_map = key

#         dff = df.copy()
#         dff = dff[dff['segment'] == option_segment]
#         dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')

#         legal_view_table = wc.format_data_table(dff,month_map)
#         download_csv = dcc.send_data_frame(legal_view_table.to_csv, "mydf.csv")
#         return download_csv

    