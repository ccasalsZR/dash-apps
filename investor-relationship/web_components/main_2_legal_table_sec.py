


from random import random
from datetime import datetime, timedelta
import pandas as pd

import datetime

import plotly.express as px
import plotly.graph_objects as go



def format_data_table(df):


    df = df[df['date_extract'] >= '2022-01-01']
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

    # print(dff.head(100))

    return dff.to_dict('records')