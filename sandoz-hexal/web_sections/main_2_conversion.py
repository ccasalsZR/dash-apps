

import plotly.express as px
import plotly.graph_objects as go

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList


import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets.json'

# """Runs a simple report on a Google Analytics 4 property."""
# Using a default constructor instructs the client to use the credentials
# specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
client = BetaAnalyticsDataClient()
property_id = '283963042'

def update_main_sec2(start_date,end_date,act_users,treatment):

    if len(treatment) == 2 or len(treatment) == 0:
        value_filter = '/care'
    elif treatment[0] == 'ED':
        value_filter = '/care/erektionsstoerungen'
    elif treatment[0] == 'Thyroids':
        value_filter = '/care/schilddruese'
    


    # Documentation for Dims and Metrics:
    # https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="eventName"),
            Dimension(name="customEvent:eventCategory"),
            Dimension(name="customEvent:eventLabel"),
            Dimension(name="customEvent:eventAction"),
            ],
        metrics=[Metric(name="eventCount"),
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],

        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    match_type='CONTAINS',
                    value=value_filter
                )
            )
        )

    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"eventName": row.dimension_values[0].value,
            "eventCategory": row.dimension_values[1].value,
            "eventLabel": row.dimension_values[2].value,
            "eventAction": row.dimension_values[3].value,
            "eventCount": row.metric_values[0].value,
        })

    df = pd.DataFrame(output)

    # Casting the metrics from the API call
    df = df.astype({'eventCount':'int',
    })

    

    
    df_donwload_video = df.copy()
    df = df[(df['eventCategory'] == 'docmorriscare') & ~df['eventAction'].isin(['(not set)',''])]    
 

    
    # TELECLINIC CLICKOUTS ------------------------------------------------------------------------

    df_teleclinic = df.copy()
    df_teleclinic = df_teleclinic[df_teleclinic['eventAction'].str.contains('teleclinic')]

    value_disp = df_teleclinic['eventCount'].sum()
    reference_disp = value_disp/((value_disp/act_users)+1) # adapting the reference value to change the behaviour of "delta"

    fig1 = go.Figure(go.Indicator(
        mode="number+delta",
        value = value_disp,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {
            'reference': reference_disp, 
            'relative': True, 
            'position' : "right", 
            'valueformat': ".2%",
            'increasing' : {
                'color' : '#22594c',
                'symbol' : ''
            }
        },        
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat': ",.0f"
        },
    ))
    fig1.update_layout(
        height=120,
    )

    # CLICKOUTS TO 116117 ----------------------------------------------------------------------------

    df_116117 = df.copy()
    df_116117 = df_116117[df_116117['eventAction'].str.contains('116117.de')]

    value_disp = df_116117['eventCount'].sum()
    reference_disp = value_disp/((value_disp/act_users)+1)  # adapting the reference value to change the behaviour of "delta"

    fig2 = go.Figure(go.Indicator(
        mode="number+delta",
        value= value_disp,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {
            'reference': reference_disp, 
            'relative': True, 
            'position' : "right", 
            'valueformat': ".2%",
            'increasing' : {
                'color' : '#22594c',
                'symbol' : ''
            }
        }, 
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig2.update_layout(
        height=120,
    )

    
    # BRING THE DOWNLOAD AND START VIDEO 
    #  THIS HAS A SLIGHTLY DIFFERENT FILTER THAT'S WHY IT'S IN A DIFFERENT BLOCK


    df_donwload_video = df_donwload_video[
            (df_donwload_video['eventCategory'] == 'docmorriscare') 
            & df_donwload_video['eventLabel'].isin(['Hier herunterladen','Hier herunterladen\n','Video abspielen','Video abspielen\n'])
        ] 


    #  VIDEO PLAYS ----------------------------------------------------------------------------------------
    df_download = df_donwload_video[
            df_donwload_video['eventLabel'].isin(['Hier herunterladen','Hier herunterladen\n'])
        ] 
    value_disp = df_download['eventCount'].sum()    
    reference_disp = value_disp/((value_disp/act_users)+1)  # adapting the reference value to change the behaviour of "delta"

    fig3 = go.Figure(go.Indicator(
        mode="number+delta",
        value= value_disp,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {
            'reference': reference_disp, 
            'relative': True, 
            'position' : "right", 
            'valueformat': ".2%",
            'increasing' : {
                'color' : '#22594c',
                'symbol' : ''
            }
        }, 
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=120,
    )
    
    #  VIDEO PLAYS ----------------------------------------------------------------------------------------
    df_video = df_donwload_video[
            df_donwload_video['eventLabel'].isin(['Video abspielen','Video abspielen\n'])
        ] 
    value_disp = df_video['eventCount'].sum()
    reference_disp = value_disp/((value_disp/act_users)+1)  # adapting the reference value to change the behaviour of "delta"

    fig4 = go.Figure(go.Indicator(
        mode="number+delta",
        value= value_disp,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {
            'reference': reference_disp, 
            'relative': True, 
            'position' : "right", 
            'valueformat': ".2%",
            'increasing' : {
                'color' : '#22594c',
                'symbol' : ''
            }
        }, 
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig4.update_layout(
        height=120,
    )

    return fig1, fig2, fig3, fig4

# update_main_sec2('2022-10-25','2022-11-24',100)




def questionnare(start_date,end_date,treatment):


    value_filter = []
    if len(treatment) == 0:
        value_filter.append('/care/erektionsstoerungen/symptomcheck')
        value_filter.append('/care/schilddruese/symptomcheck')
    else:
        for i in treatment:
            if i == 'ED':
                value_filter.append('/care/erektionsstoerungen/symptomcheck')
            elif i == 'Thyroids':
                value_filter.append('/care/schilddruese/symptomcheck')


    # Documentation for Dims and Metrics:
    # https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath"),
            ],
        metrics=[Metric(name="sessions"),
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],

        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                in_list_filter = Filter.InListFilter(
                    values=value_filter
                )
            )
        )

    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"pagePath": row.dimension_values[0].value,
            "sessions": row.metric_values[0].value,
        })

    df = pd.DataFrame(output)
    # df = df[(df['eventCategory'] == 'docmorriscare') & ~df['eventAction'].isin(['(not set)',''])]    

    # Casting the metrics from the API call
    df = df.astype({'sessions':'int',
    })

    # MAP the URL to actual DIMs

    map_url_start = {
        '/care/schilddruese/symptomcheck':'Thyroids',
        '/care/erektionsstoerungen/symptomcheck':'ED'
    }

    df['treatment'] = df['pagePath'].map(map_url_start)
    df['type'] = 'did not convert'


    # LET'S GET THE CONVERSION AT THE END OF THE QUESTIONNAIRE --------------------------------------------------------------

    value_filter = [s + '/ergebnis1' for s in value_filter ]
    

    # Documentation for Dims and Metrics:
    # https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath"),
                Dimension(name="eventName"),
                Dimension(name="customEvent:eventCategory"),
                Dimension(name="customEvent:eventLabel"),
                Dimension(name="customEvent:eventAction"),
            ],
        metrics=[Metric(name="sessions"),
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],

        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePath",
                in_list_filter = Filter.InListFilter(
                    values=value_filter
                )
            )
        )

    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"pagePath": row.dimension_values[0].value,
            "eventName": row.dimension_values[1].value,
            "eventCategory": row.dimension_values[2].value,
            "eventLabel": row.dimension_values[3].value,
            "eventAction": row.dimension_values[4].value,
            "sessions": row.metric_values[0].value,
        })

    df_end_of_Q = pd.DataFrame(output)

    # Casting the metrics from the API call
    df_end_of_Q = df_end_of_Q.astype({'sessions':'int',
    })

    df_end_of_Q = df_end_of_Q[(df_end_of_Q['eventCategory'] == 'docmorriscare') & ~df_end_of_Q['eventAction'].isin(['(not set)',''])]    

    map_url_end = {
        '/care/schilddruese/symptomcheck/ergebnis1':'Thyroids',
        '/care/erektionsstoerungen/symptomcheck/ergebnis1':'ED'
    }
    df_end_of_Q['treatment'] = df_end_of_Q['pagePath'].map(map_url_end)

    # Logic to create cat. for the different Conversion types.
    df_end_of_Q['type'] = np.where(
            df_end_of_Q['eventAction'].str.contains('116117'), 
            '116117', 
            np.where(
                df_end_of_Q['eventAction'].str.contains('teleclinic'),
                'Teleclinic',
                ''
            )
        ) 

    # Filter dataset
    df_end_of_Q = df_end_of_Q[df_end_of_Q['type'] != '']

    # Aggregation of the conversion dataset
    # to substract from the total volume of sessions that have started the questionnaire
    df_agg = df_end_of_Q.copy()
    df_agg = df_agg[['treatment','sessions']]

    df_agg = df_agg.groupby(by=['treatment']).sum()
    df_agg.reset_index(inplace=True)

    
    df_agg.columns = ['treatment','sessions_conv']

    # Subset to bring all the data together
    dff = df.copy()

    dff = dff[['treatment','type','sessions']].merge(df_agg, how='left', on='treatment')
    dff.fillna(0,inplace=True)
    dff['sessions_start'] = dff['sessions'] - dff['sessions_conv']

    # Renaming and concatenation of dataset for the visual
    dff = dff[['treatment','type','sessions_start']]
    dff.rename(columns={'sessions_start':'sessions'},inplace=True)

    dffe = df_end_of_Q[['treatment','type','sessions']]
    dffe = dffe.groupby(by=['treatment','type']).sum()
    dffe.reset_index(inplace=True)

    dfff = pd.concat([dff,dffe], ignore_index=True)
    
    # # QUESTIONNAIRE -----------------------------------------------------------------------------------
  
    fig = px.bar(
            dfff, 
            x="treatment", 
            y='sessions',
            color="type", 
            color_discrete_map = {
                'did not convert':'#38947F',
                'Teleclinic':'#F0b92d',
                '116117':'#C3900E'
            }, 
            text = 'sessions',
        )
    fig.update_layout(
        # legend=dict(orientation='h', yanchor='bottom', y=-0.5, xanchor='left', x=0, title=None),
        plot_bgcolor='#fff',
        height=240,
        margin=dict(l=10, r=10, t=20, b=0)
    )


    return fig

