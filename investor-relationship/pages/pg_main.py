

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
                                options=[value for value in dict_month_sel.values()],
                                multi=False,
                                style={'width': '150px' }
                                ),
            ], style= {'display':'flex', 'align-items':'right','float': 'right'}, className= 'flex-row-reverse')
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
                            dict(id = 'actual_month', name = 'Actual'),
                            dict(id = 'forecast_month', name = 'Forecast'),
                            dict(id = 'delta_actual_forecast', name = 'Δ'),
                            dict(id = 'delta%_actual_forecast', name = 'Δ(%)'),
                            dict(id = 'budget_month', name = 'Budget'),
                            dict(id = 'delta_actual_budget', name = 'Δ'),
                            dict(id = 'delta%_actual_budget', name = 'Δ(%)'),
                            dict(id = 'prev_year_month', name = 'Prev. Year'),                            
                            dict(id = 'delta_actual_prev_year', name = 'Δ'),
                            dict(id = 'delta%_actual_prev_year', name = 'Δ(%)'),
                        ],
                        style_as_list_view=True,
                        style_cell={'padding': '8px'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'borderBottom':'1.5px solid'
                        },
                        style_data_conditional=[
                            # {
                            #     'if': {'row_index': 'even'},
                            #     'backgroundColor': 'rgb(240, 240, 240)',
                            # },
                            {
                                'if': {
                                    'state': 'active'  # 'active' | 'selected'
                                },
                                'backgroundColor': 'rgba(34, 89, 76, 0.2)',
                                'border':'None'
                            },
                            {
                                'if': {
                                    'filter_query': '{income_statement} = "Gross profit" || {income_statement} = "EBITDA adjusted" || {income_statement} = "EBITDA reported"'
                                },
                                'borderBottom':'2px solid #38947F'
                            },
                            {
                                'if': {
                                    'column_id': 'actual_month'
                                },
                                'backgroundColor': 'rgba(56, 148, 127,0.17)',
                            },
                            {
                                'if': {
                                    'column_id': ['delta_actual_forecast','delta%_actual_forecast','delta_actual_budget','delta%_actual_budget','delta_actual_prev_year','delta%_actual_prev_year']
                                },
                                'backgroundColor': 'rgb(245, 245, 245)',
                            },  
                        ],
                        style_cell_conditional=[
                            {
                                'if': {
                                    'column_id': 'income_statement'
                                },
                                'textAlign': 'left',
                            },
                            
                        ],
                        style_table={'borderBottom':'3px solid #13322B'}
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
    # Output('dbc_table_1', 'children'),

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

    # Build the dbc table
    df_dbc = legal_view_table.copy()

    print(df_dbc.dtypes)

    df_dbc['actual_month'] = df_dbc['actual_month'].map('{:,.1f}'.format)
    df_dbc['forecast_month'] = df_dbc['forecast_month'].map('{:,.1f}'.format)
    df_dbc['delta_actual_forecast'] = df_dbc['delta_actual_forecast'].map('{:,.1f}'.format)
    df_dbc['delta%_actual_forecast'] = df_dbc['delta%_actual_forecast'].map('{:.1%}'.format)
    df_dbc['budget_month'] = df_dbc['budget_month'].map('{:,.1f}'.format)
    df_dbc['delta_actual_budget'] = df_dbc['delta_actual_budget'].map('{:,.1f}'.format)
    df_dbc['delta%_actual_budget'] = df_dbc['delta%_actual_budget'].map('{:.1%}'.format)
    df_dbc['prev_year_month'] = df_dbc['prev_year_month'].map('{:,.1f}'.format)
    df_dbc['delta_actual_prev_year'] = df_dbc['delta_actual_prev_year'].map('{:,.1f}'.format)
    df_dbc['delta%_actual_prev_year'] = df_dbc['delta%_actual_prev_year'].map('{:.1%}'.format)
    
    
    print(df_dbc)
    
    return (mc[0],mc[1],
        df_dbc.to_dict('records'),
    )

# A-SYNC call > so we don't trigger an event uppon refresh
@callback(
   
    Output("download-dataframe-csv", "data"),

    Input('slct_segment', 'value'),    
    Input('slct_month', 'value'),       
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)

def update_async(option_segment,month_sel,n_clicks):

    if n_clicks is None:
        raise PreventUpdate
    else:
        month_map = None
        for key, value in dict_month_sel.items():  
            if value == month_sel:
                month_map = key

        dff = df.copy()
        dff = dff[dff['segment'] == option_segment]
        dff['date_extract'] = pd.to_datetime(dff['date_extract'], format='%Y-%m-%d')

        legal_view_table = format_data_table(dff,month_map)
        download_csv = dcc.send_data_frame(legal_view_table.to_csv, "mydf.csv")
        return download_csv

    