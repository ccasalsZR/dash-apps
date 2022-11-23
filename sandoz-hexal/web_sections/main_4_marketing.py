import plotly.express as px
import plotly.graph_objects as go


from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

import pandas as pd
import json

import os
from dotenv import load_dotenv

load_dotenv()

my_app_id = os.getenv('my_app_id')
my_app_secret = os.getenv('my_app_secret')
my_access_token = os.getenv('my_access_token')

def get_marketing_data(start_date,end_date):

    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
    
    params = {
        'level': 'campaign',
        'time_range': {
            'since':start_date,
            'until':end_date
        },
        'filtering':[
            {
                'field':'campaign.id',
                'operator': 'EQUAL',
                'value':23851836028670506,
            },
        ],
    }   

    fields = [
        'campaign_name',
        'adset_name',
        'spend',
        'cpm', # The average cost for 1,000 impressions.
        'cpc', # The average cost for each click (all).
        'ctr', # The percentage of times people saw your ad and performed a click (all).
        'clicks', # The number of clicks on your ads.
        'impressions',  
        # 'outbound_clicks', #The number of clicks on links that take people off Facebook-owned properties.
    ]

    # print(fields)

    rawdata = AdAccount('act_1416513921734975').get_insights(
        params = params,
        fields = fields,
    )
    rawdata = [x for x in rawdata]

    df = pd.DataFrame(rawdata)

    
    # Cast the extract
    df = df.astype({
        'clicks':'int',
        'cpc':'float32',
        'cpm':'float32',
        'ctr':'float32',
        'impressions':'int',
        'spend':'float32',
    })

    # SPEND -------------------------------------------------------------------
    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=df['spend'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat':',.1f',
            'suffix':'€',
        },
    ))
    fig1.update_layout(
        height=200,
    )

    # CPM ---------------------------------------------------------------------
    fig2 = go.Figure(go.Indicator(
        mode="number",
        value=df['spend'].sum()/(df['impressions'].sum()/1000),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'}, 
            'valueformat':',.1f',
            'suffix':'€',
        },
    ))
    fig2.update_layout(
        height=100,
    )

    # IMPRESSIONS --------------------------------------------------------------
    fig3 = go.Figure(go.Indicator(
        mode="number",
        value=df['impressions'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat':',.0f',
        },
    ))
    fig3.update_layout(
        height=100,
    )

    # CTR ---------------------------------------------------------------------
    fig4 = go.Figure(go.Indicator(
        mode="number",
        value=df['clicks'].sum()/df['impressions'].sum()*100,
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat':',.2f',
            'suffix':'%'
        },
    ))
    fig4.update_layout(
        height=200,
    )

    # Cost per Click -----------------------------------------------------------
    fig5 = go.Figure(go.Indicator(
        mode="number",
        value=df['spend'].sum()/df['clicks'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat':',.2f',
            'suffix':'€'    
        },
    ))
    fig5.update_layout(
        height=100,
    )

    fig6 = go.Figure(go.Indicator(
        mode="number",
        value=df['clicks'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat':',.0f',
        },
    ))
    fig6.update_layout(
        height=100,
    )


    return [fig1,fig2,fig3,fig4,fig5,fig6]