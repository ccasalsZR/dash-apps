

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



from dotenv import load_dotenv
load_dotenv()


import web_components as wc


dash.register_page(
    __name__,
    path='/backlog-monitor',
    title='Backlog Monitor'
) # Home page


DB_SNOW_PASS = os.getenv('DB_SNOW_PASS')
DB_SNOW_USER = os.getenv('DB_SNOW_USER')




    
layout = html.Div([
    dcc.Interval(
        id="load_interval", 
        n_intervals=0, 
        max_intervals=0, #<-- only run once
        interval=1
    ),
    dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H3('DCA Order Flow',className='h3-sub'),
            ]),
            dbc.Col([
                html.P(id='kpi_data_asof', children=[] )
            ], style= {'display':'flex', 'align-items':'right'}, className= 'flex-row-reverse')
        ]),
        html.Hr(),
        dbc.Row([
            # Created Today
            dbc.Col([
                html.P('Created Today', id='tt_created_today'),
                dcc.Loading(
                    children = [dcc.Graph(id='kpi_created_today',figure={})]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            # Backlog ERP
            dbc.Col([
                html.P('Backlog ERP', id='tt_backlog_erp'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_backlog_erp',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            #  Backlog EWM
            dbc.Col([
                html.P('Backlog EWM', id='tt_backlog_ewm'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_backlog_ewm',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            # Ready for logistics
            dbc.Col([
                html.P('Ready for Logistics', id='tt_ready_logistics'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_ready_logistics',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            # In Logistics
            dbc.Col([
                html.P('In Logistics', id='tt_IN_logistics'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_IN_logistics',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            # Sent today
            dbc.Col([
                html.P('Sent today', id='tt_sent_today'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_sent_today',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
        ]),        
        dbc.Tooltip(target="tt_created_today",      placement='auto',  children ="Orders created today."),
        dbc.Tooltip(target="tt_backlog_erp",        placement='auto',  children ="PTA clearance + Crossdock."),
        dbc.Tooltip(target="tt_backlog_ewm",        placement='auto',  children ="Orders in EWM where commission has not yet started."),
        dbc.Tooltip(target="tt_ready_logistics",    placement='auto',  children ="All orders ready for processing but not yet sent to WAMAS."),
        dbc.Tooltip(target="tt_IN_logistics",       placement='auto',  children ="All orders started in WAMAS where PEK is not yet finished."),
        dbc.Tooltip(target="tt_sent_today",         placement='auto',  children ="All orders where PEK was finished today."),
        dbc.Row([
            dbc.Col([
                html.P('Created Before Today', id='tt_created_before_today'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_created_before_today',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('In PTA aprroval', id='tt_pta_clearance'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_pta_clearance',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Crossdock starter', id='tt_crossdock_starter'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_crossdock_starter',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Tooltip(target="tt_created_before_today",   placement='auto',  children ="Orders created yesterday and before."),
        dbc.Tooltip(target="tt_pta_clearance",          placement='auto',  children ="Sum of all orders in PTA clearance."),
        dbc.Tooltip(target="tt_crossdock_starter",      placement='auto',  children ="All orders which have CD Starter Flag."),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Back Order', id='tt_backorder'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_backorder',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Failed', id='tt_amount_failed'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_amount_failed',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Tooltip(target="tt_backorder",      placement='auto',  children ="Orders waiting for goods in Crossdock."),
        dbc.Tooltip(target="tt_amount_failed",  placement='auto',  children ="How many orders are in the failed wave."),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Failed Orders'),
                dcc.Loading(
                    children = [
                        # dcc.Graph(id='kpi_created_today',figure=fig_failed_orders)
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col([
                html.P('Ready for WAMAS', id='tt_ready_WAMAS'),
                dcc.Loading(
                    children = [
                        dcc.Graph(id='kpi_ready_WAMAS',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        dbc.Tooltip(target="tt_ready_WAMAS",  placement='auto',  children ="All orders ready to be transferred to WAMAS."),
        dbc.Row([
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col([
                html.P('Not Processed'),
                dcc.Loading(
                    children = [
                        # dcc.Graph(id='kpi_created_today',figure=fig_not_processed)
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
            dbc.Col(class_name='grid_box_empty'),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H3('Open Orders',className='h3-sub'),
            ])
        ]),    
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    children = [
                        dcc.Graph(id='chart_open_orders_ageing',figure={})
                    ]
                    ,type='dot',color='#22594C'
                )
            ],class_name='grid_box')
        ]),
    ]),    
    html.Br(),
     # dcc.Store inside the user's current browser session
    dcc.Store(id='store_backlogEWM_crossdock', data=[], storage_type='memory'), # 'local' or 'session'
    dcc.Store(id='store_amount_failed', data=[], storage_type='memory'), # 'local' or 'session'
    dcc.Store(id='store_pta_clearance', data=[], storage_type='memory') # 'local' or 'session'
])


@callback(
    Output('kpi_created_today','figure'),
    Output('kpi_created_before_today','figure'),
    Output('chart_open_orders_ageing','figure'),

    Input('load_interval','n_intervals')
)
def update_open_orders(n_intervals):

    df = wc.execute_query('scripts/open_orders_created.sql')
    kpi_open_orders = df[df['backlog_day_cat'] == 'Day 0'] # Today
    fig = wc.kpi_template(kpi_open_orders['open_orders'].sum())
    
    kpi_open_orders = df[df['backlog_day_cat'] != 'Day 0'] # Before Today
    fig2 = wc.kpi_template(kpi_open_orders['open_orders'].sum())

    fig3 = wc.open_order_chart(df)

    return fig, fig2, fig3


@callback(
    Output('kpi_IN_logistics','figure'),
    Output('kpi_backlog_ewm','figure'),
    Output('kpi_sent_today','figure'),
    Output('kpi_crossdock_starter','figure'),
    Output('kpi_ready_logistics','figure'),
    Output('store_backlogEWM_crossdock', 'data'),

    Input('load_interval','n_intervals')
)
def update_backlog_EWM_logistics(n_intervals):

    df = wc.execute_query('scripts/backlog_EWM_logistics.sql')

    fig_in_logistics = wc.kpi_template(df['in_logistics'].sum())
    
    val_backlog_ewm = df['backlog_ewm'].sum()
    fig_backlog_ewm = wc.kpi_template(val_backlog_ewm)
    fig_sent_today = wc.kpi_template(df['sent_today'].sum())
    
    val_crossdock = df['crossdock_starter'].sum()
    fig_crossdock_starter = wc.kpi_template(val_crossdock)
    fig_ready_logistics = wc.kpi_template(df['ready_for_logistics'].sum())

    data = [val_backlog_ewm,val_crossdock]

    return [fig_in_logistics, fig_backlog_ewm, fig_sent_today, fig_crossdock_starter, fig_ready_logistics,
        # Store data
        data
    ]

@callback(
    Output('kpi_pta_clearance','figure'),
    Output('store_pta_clearance', 'data'),
    Input('load_interval','n_intervals')
)
def update_pta_clearance(n_intervals):
    df = wc.execute_query('scripts/pta_clearance.sql')
    val_pta_clearance = df['pta_clearance'].sum()
    return [wc.kpi_template(val_pta_clearance),
        # store data
        val_pta_clearance
    ]

@callback(
    Output('kpi_backorder','figure'),
    Input('load_interval','n_intervals')
)
def update_backorders(n_intervals):
    df = wc.execute_query('scripts/backorders.sql')
    return wc.kpi_template(df['backorder'].sum())

@callback(
    Output('kpi_amount_failed','figure'),
    Output('store_amount_failed', 'data'),
    Input('load_interval','n_intervals')
)
def update_amount_failed(n_intervals):
    df = wc.execute_query('scripts/amount_failed.sql')
    val_amount_failed = df['amount_failed'].sum()
    return [wc.kpi_template(val_amount_failed),
        # store data
        val_amount_failed
    ]

@callback(
    Output('kpi_ready_WAMAS','figure'),
    Output('kpi_backlog_erp','figure'),    
    Input('store_backlogEWM_crossdock', 'data'),
    Input('store_amount_failed', 'data'),
    Input('store_pta_clearance', 'data'),
)
def update_visual_store(backlogEWM_crossdock,amount_failed,pta_clearance):
    
    val_ready_WAMAS = backlogEWM_crossdock[0] - backlogEWM_crossdock[1] - amount_failed
    val_backlog_ERP = pta_clearance + backlogEWM_crossdock[1]

    return [wc.kpi_template(val_ready_WAMAS)
        ,wc.kpi_template(val_backlog_ERP)
    ]


@callback(
    Output('kpi_data_asof','children'),
    Input('load_interval','n_intervals')
)
def update_backorders(n_intervals):
    df = wc.execute_query('scripts/data_asof.sql')
    change_date = str(df['change'].min())
    return 'Data as of: ' + change_date

    