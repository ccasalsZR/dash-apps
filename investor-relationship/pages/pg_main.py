

from random import random
from dash import html, callback, Output, Input, dcc

import os
# from dotenv import load_dotenv
# import snowflake.connector as snow


import dash, dash_table
from dash.dash_table.Format import Format, Scheme, Trim
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

from dotenv import load_dotenv
load_dotenv()

from web_components import monthly_chart,format_data_table

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

df = pd.read_csv('legal_view_extract.csv')
# df.fillna(0,inplace=True)
# print(df.head(10))


d = {'SEGMENT':['Group','CH','DE','EU','Corp.']}
df_dropdown = pd.DataFrame(data=d)

dash.register_page(
    __name__,
    path='/',
    title='Sandoz Hexal - DocMorris Analytics'
) # Home page




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
        html.H3('Legal View',className='h3-sub'),
        dbc.Row([
            dcc.Loading(
                id='loading-1',
                children=[
                    dash_table.DataTable(
                        id='data_table_1',
                        data=[],
                        columns=[
                            dict(id = 'income_statement', name = ''),
                            dict(id = 'actual_month', name = 'Actual', type='numeric', format=Format(precision=1, scheme=Scheme.fixed)),
                            dict(id = 'forecast_month', name = 'Forecast', type='numeric', format=Format(precision=1, scheme=Scheme.fixed)),
                            dict(id = 'budget_month', name = 'Budget', type='numeric', format=Format(precision=1, scheme=Scheme.fixed)),
                            dict(id = 'prev_year_month', name = 'Prev. Year', type='numeric', format=Format(precision=1, scheme=Scheme.fixed)),
                        ],
                        style_as_list_view=True,
                        style_cell={'padding': '5px'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['income_statement']
                        ],
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

    Output('data_table_1', 'data'),

    Input('slct_segment', 'value')
)

def update_graph(option_segment):

    dff = df.copy()
    dff = dff[dff['segment'] == option_segment]
    dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')
    
    mc = monthly_chart(dff)

    legal_view_table = format_data_table(dff)
    

    return (mc[0],mc[1],
        legal_view_table
    )
