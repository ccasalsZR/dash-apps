

import plotly.express as px
import plotly.graph_objects as go

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression


import pandas as pd


def update_main_sec2():

    # """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

    # Documentation for Dims and Metrics:
    # https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="linkUrl")],
        metrics=[Metric(name="eventCount"),
            ],
        date_ranges=[DateRange(start_date='2022-11-01', end_date='2022-11-07')],
        dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="linkUrl",
                    string_filter=Filter.StringFilter(
                        match_type='CONTAINS',
                        value='teleclinic'
                    )
                )
            ),
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"linkUrl": row.dimension_values[0].value,
            "eventCount": row.metric_values[0].value,
        })
    df = pd.DataFrame(output)


    # Casting the metrics from the API call
    df = df.astype({'eventCount':'int',
    })


    # TELECLINIC CLICKOUTS ------------------------------------------------------------------------

    fig1 = go.Figure(go.Indicator(
        mode="number+delta",
        value=df['eventCount'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 22000, 'relative': True, 'position' : "right", "valueformat": ".2%"},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig1.update_layout(
        height=120,
    )

    # CLICKOUTS TO 116117 ----------------------------------------------------------------------------
    fig2 = go.Figure(go.Indicator(
        mode="number+delta",
        value=0,
        domain={"x": [0, 1], "y": [0, 1]},
        delta = {'reference': 20030, 'relative': True, 'position' : "right", "valueformat": ".2%"},
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