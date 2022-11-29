


from random import random
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

from datetime import datetime

from dash import dash_table
import plotly.express as px 
import plotly.graph_objects as go

def pivot_and_clean_table(df,type):

    df = pd.pivot_table(df, values= [type], index='income_statement',columns='date_extract_disp')
    df.columns = df.columns.map(' | '.join).str.strip(' | ')

    # df_pivot.columns = df_pivot.columns.droplevel(0) #remove amount
    df.columns.name = None               #remove categories
    df = df.reset_index()                #index to columns

    return df

def dynamic_data_table(df,start_range,end_range):


    df = df[(df['date_extract'] >= start_range) & (df['date_extract'] <= end_range)]  
   
    dff = df[['income_statement','date_extract','actual_month','forecast_month','budget_month','prev_year_month']]
    dff['date_extract_disp'] = pd.to_datetime(df['date_extract']).dt.strftime('%Y/%m')

    dff['AC'] = dff['actual_month'].round(1)
    dff['FC'] = dff['forecast_month'].round(1)
    dff['BG'] = dff['budget_month'].round(1)
    dff['PV'] = dff['prev_year_month'].round(1)



    # list to filter the legal view table
    value_list = {
        'Consolidated Revenues':1,
        'Gross profit':2,
        'Other operating income':3,
        'Personnel expenses':4,
        'Marketing expenses':5,
        'Distribution expenses':6,
        'Other operating expenses':7,
        'EBITDA adjusted':8,
        'Adjustments M&A':9,
        'Adjustments integration':10,
        'Adjustments Various / Reserve':11,
        'EBITDA reported':12,
        'EBIT':13,
        'EAT':14,
        'SITE_VISITS':15,
        'CUSTOMER_NEW_RX':16,
        'CUSTOMER_NEW_OTC':17,
        'CUSTOMER_REPEAT':18,
        'ACTIVE_CUSTOMER':19,
        'ACTIVE_CUSTOMER_1Y_ROLLING':20,
        'CUSTOMER_NEW':21,
        'CUSTOMER_REPEAT':22,
        'ACTIVE_CUSTOMER_RX':23,
        'ACTIVE_CUSTOMER_OTC':24,
        'NET_SALES_CUSTOMER_RX':25,
        'NET_SALES_CUSTOMER_OTC':26,
        'BASKET_AVG_RX':27,
        'BASKET_AVG_OTC':28,
        'NPS':29,
    }

    map_cognosKPI = {
        'SITE_VISITS':'Site Visits',
        'CUSTOMER_NEW_RX': 'Customers New Rx',
        'CUSTOMER_NEW_OTC': 'Customer New Otc',
        'CUSTOMER_REPEAT': 'Customer Repeat',
        'ACTIVE_CUSTOMER': 'Active Customer',
        'ACTIVE_CUSTOMER_1Y_ROLLING': 'Active Customer 1Year RollBack',
        'CUSTOMER_NEW': 'Customer New',
        'CUSTOMER_REPEAT': 'Customer Repeat',
        'ACTIVE_CUSTOMER_RX': 'Active Customer Rx',
        'ACTIVE_CUSTOMER_OTC': 'Active Customer Otc',
        'NET_SALES_CUSTOMER_RX': 'Net Sales Rx',
        'NET_SALES_CUSTOMER_OTC': 'Net Sales Otc',
        'BASKET_AVG_RX': 'Avg. Basket Rx',
        'BASKET_AVG_OTC': 'Avg. Basket Otc',
        'NPS': 'NPS',
    }


    dff = dff.groupby(by=['income_statement','date_extract','date_extract_disp']).sum()
    dff.reset_index(inplace=True)

    

    dff_AC = dff[dff['date_extract'] <= '2022-10-01']
    dff_FC = dff[dff['date_extract'] > '2022-10-01']


    df_pivot_AC = pivot_and_clean_table(dff_AC,'AC')
    df_pivot_FC = pivot_and_clean_table(dff_FC,'FC')

    df_pivot = pd.merge(df_pivot_AC, df_pivot_FC, how='outer', on = ['income_statement'])

    
    df_pivot['sort_id'] = df_pivot['income_statement'].map(value_list)
    df_pivot = df_pivot[df_pivot['sort_id'].notna()]
    df_pivot = df_pivot.sort_values(by='sort_id')


    # Map the clean names for Cognos KPI's
    df_pivot['cognos_kpi_clean'] = df_pivot['income_statement'].map(map_cognosKPI)
    df_pivot['income_statement'] = np.where(df_pivot['cognos_kpi_clean'].isnull(), df_pivot['income_statement'], df_pivot['cognos_kpi_clean'] )


    df_pivot.drop(columns={'sort_id','cognos_kpi_clean'}, inplace=True)

    

    # Get the columns from our dataset
    col = df_pivot.columns
    col_even = col[1::2] # Keep only every second column --> to color.


    # format columns with the metrics
    col_metrics = col[1::]
    for kpi in col_metrics:
        df_pivot[kpi] = df_pivot[kpi].map('{:,.1f}'.format)   


    dashT = dash_table.DataTable(
        data=df_pivot.to_dict('records'),        
        columns=[{"name": i, "id": i} for i in df_pivot.columns],
        # data=table_meta[1],
        # columns=table_meta[0],
        fixed_columns = {'headers':True, 'data':1},

        style_as_list_view=True,
        style_cell={'padding': '5px'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'borderBottom':'1.5px solid'
        },
        style_cell_conditional=[
            {
                'if': {
                    'column_id': 'income_statement'
                },
                'textAlign': 'left',
            },                      
        ],
        style_data_conditional=[
            {
                'if': {
                    'column_id': col_even
                },
                'backgroundColor': 'rgb(245, 245, 245)',
            },
            {
                'if': {
                    'filter_query': '{income_statement} = "Gross profit" || {income_statement} = "EBITDA adjusted" || {income_statement} = "EBITDA reported"'
                },
                'borderBottom':'2px solid #38947F'
            }, 
            {
                'if': {
                    'filter_query': '{income_statement} = "EAT"'
                },
                'borderBottom':'3px solid #000'
            },  
            {
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
                'backgroundColor': 'rgba(34, 89, 76, 0.2)',
                'border':'None'
            },
        ],
        style_table={'overflowX': 'scroll','minWidth': '100%'},
    )


    return dashT

