


from random import random
from datetime import datetime, timedelta
import pandas as pd

import datetime

import plotly.express as px
import plotly.graph_objects as go


def monthly_chart (df):

    df = df[['date_extract','income_statement','prev_year_month','actual_month','budget_month','forecast_month']]

    # INCOME STATEMENT ---------------------------------
    dff = df[(df['income_statement'] == 'External Revenues') & (df['date_extract'] >= '2022-01-01')]
    dff = dff.sort_values(by='date_extract')
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=dff['date_extract'],y=dff['prev_year_month'],
                        mode='lines+markers',
                        name='Prev. Year',
                        line=dict(color='#757575')
                    ))
    fig1.add_trace(go.Scatter(x=dff['date_extract'],y=dff['budget_month'],
                        mode='lines+markers',
                        name='Budget',
                        line=dict(color='#90D5C5')
                    ))
    fig1.add_trace(go.Bar(x=dff['date_extract'],y=dff['actual_month'],
                        name='Actual',
                        marker_color='#22594c',                        
                    ))
    fig1.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-
                    0.5, xanchor='left', x=0, title=None),
        plot_bgcolor='#fff',        
        margin=dict(l=20, r=20, t=80, b=10)
    )


    # EBITDA ADJUSTED -----------------------------------
    dff = df[(df['income_statement'] == 'EBITDA adjusted') & (df['date_extract'] >= '2022-01-01')]
    dff = dff.sort_values(by='date_extract')

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=dff['date_extract'],y=dff['prev_year_month'],
                        mode='lines+markers',
                        name='Prev. Year',
                        line=dict(color='#757575')
                    ))
    fig2.add_trace(go.Scatter(x=dff['date_extract'],y=dff['budget_month'],
                        mode='lines+markers',
                        name='Budget',
                        line=dict(color='#90D5C5')
                    ))
    fig2.add_trace(go.Scatter(x=dff['date_extract'],y=dff['forecast_month'],
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='#F0b92d')                   
                    ))
    fig2.add_trace(go.Bar(x=dff['date_extract'],y=dff['actual_month'],
                        name='Actual',
                        marker_color='#22594c',                        
                    ))
    fig2.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-
                    0.5, xanchor='left', x=0, title=None),
        plot_bgcolor='#fff',        
        margin=dict(l=20, r=20, t=80, b=10)
    )

    return fig1,fig2