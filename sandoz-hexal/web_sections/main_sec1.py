
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest


def update_main_sec1(start_date,end_date):

    
    
    """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

    request = RunReportRequest(
        property=f"properties/{property_id}",
        # dimensions=[Dimension(name="month"),Dimension(name="sessionDefaultChannelGrouping")],
        metrics=[Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="activeUsers") # distinct users
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"Sessions": row.metric_values[0].value,
            "New Users": row.metric_values[1].value,
            "Active Users": row.metric_values[2].value,
        })
    df = pd.DataFrame(output)
    
    # GENERATION OF THE VISUAL ------------------------------------------------------
    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=int(df['Sessions'].min()),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig1.update_layout(
        height=100,
    )

    fig2 = go.Figure(go.Indicator(
        mode="number",
        value=int(df['New Users'].min()),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig2.update_layout(
        height=100,
    )
    fig3 = go.Figure(go.Indicator(
        mode="number",
        value=int(df['Active Users'].min()),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=100,
    )

    return [fig1,fig2,fig3]