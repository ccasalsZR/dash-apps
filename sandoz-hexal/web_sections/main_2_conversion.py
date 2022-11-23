

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


def update_main_sec2(start_date,end_date,act_users):

    # """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

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
                    value='/care'
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
    df = df[(df['eventCategory'] == 'docmorriscare') & ~df['eventAction'].isin(['(not set)',''])]    

    # Casting the metrics from the API call
    df = df.astype({'eventCount':'int',
    })



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

    # QUESTIONNAIRE -----------------------------------------------------------------------------------
    fig3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=0,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 19000, 'relative': True, 'position' : "right", "valueformat": ".2%"},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=120,
    )

    return fig1, fig2, fig3
