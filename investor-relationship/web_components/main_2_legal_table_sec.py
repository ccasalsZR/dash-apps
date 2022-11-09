


from random import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

import datetime

import plotly.express as px
import plotly.graph_objects as go



def format_data_table(df,month_map):

    if month_map != None:
        df = df[df['date_extract'] <= month_map]  
    else:
        df
   
    dff = df[['income_statement','actual_month','forecast_month','budget_month','prev_year_month']]

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
        'EAT':14
    }


    dff = dff.groupby(by='income_statement').sum()
    dff.reset_index(inplace=True)

    dff['sort_id'] = dff.income_statement.map(value_list)
    dff = dff[dff['sort_id'].notna()]
    dff = dff.sort_values(by='sort_id')

    dff['delta_actual_forecast'] = dff['actual_month'] - dff['forecast_month']
    dff['delta%_actual_forecast'] = np.where(dff['forecast_month'] == 0, 0, dff['delta_actual_forecast'] / dff['forecast_month'] )

    dff['delta_actual_budget'] = dff['actual_month'] - dff['budget_month']
    dff['delta%_actual_budget'] = np.where(dff['budget_month'] == 0, 0, dff['delta_actual_budget'] / dff['budget_month'] )
    
    dff['delta_actual_prev_year'] = dff['actual_month'] - dff['prev_year_month']
    dff['delta%_actual_prev_year'] = np.where(dff['prev_year_month'] == 0, 0, dff['delta_actual_prev_year'] / dff['prev_year_month'] )


    return dff