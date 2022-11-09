

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


dict_month_sel = {
    '2022-01-01':'Jan 2022',
    '2022-02-01':'Feb 2022',
    '2022-03-01':'Mar 2022',
    '2022-04-01':'Apr 2022',
    '2022-05-01':'May 2022',
    '2022-06-01':'Jun 2022',
    '2022-07-01':'Jul 2022',
    '2022-08-01':'Ago 2022',
    '2022-09-01':'Sep 2022'
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
                dcc.Dropdown(id="slct_month",
                                # options=[x for x in df_dropdown['SEGMENT'].unique()],
                                options=[value for value in dict_month_sel.values()],
                                multi=False,
                                # value='Group',
                                style={'width': '150px' }
                                ),
            ], style= {'display':'flex', 'align-items':'right'}, className= 'flex-row-reverse')
        ]),        
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
        html.Br(),  
        dbc.Row([
            dbc.Col([
                dbc.Button("Download CSV", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv"),
            ]),            
        ]), 
    ]), 
    html.Br(),   
])

@callback(
    Output('external_revenue', 'figure'),
    Output('ebitda_adjusted', 'figure'),

    Output('data_table_1', 'data'),

    Input('slct_segment', 'value'),   
    Input('slct_month', 'value'),   

)

def update_graph(option_segment,month_sel):

    month_map = None
    for key, value in dict_month_sel.items():  
        if value == month_sel:
            month_map = key

    dff = df.copy()
    dff = dff[dff['segment'] == option_segment]
    dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')
    
    mc = monthly_chart(dff)

    legal_view_table = format_data_table(dff,month_map)

    return (mc[0],mc[1],
        legal_view_table.to_dict('records')
    )

# A-SYNC call > so we don't trigger an event uppon refresh
@callback(
   
    Output("download-dataframe-csv", "data"),
    Input('slct_segment', 'value'),    
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)

def update_async(option_segment,n_clicks):

    if n_clicks is None:
        raise PreventUpdate
    else:
        dff = df.copy()
        dff = dff[dff['segment'] == option_segment]
        dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')

        legal_view_table = format_data_table(dff)
        download_csv = dcc.send_data_frame(legal_view_table.to_csv, "mydf.csv")
        return download_csv

    