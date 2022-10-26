
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest



def update_main_sec1(start_date,end_date):

     
    # """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="activeUsers") # distinct users
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"Date": row.dimension_values[0].value,
            "Sessions": row.metric_values[0].value,
            "New Users": row.metric_values[1].value,
            "Active Users": row.metric_values[2].value,
        })
    df = pd.DataFrame(output)

    # Casting the metrics from the API call
    df = df.astype({'Sessions':'int',
        'New Users':'int',
        'Active Users':'int'
    })

    # sort dataframe
    df = df.sort_values(by=['Date'])


    # GENERATION OF THE VISUAL ------------------------------------------------------
    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=df['Sessions'].sum(),
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
        value=df['New Users'].sum(),
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
        value=df['Active Users'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig3.update_layout(
        height=100,
    )

    # Line chart for the evolution of the metrics above

    fig_line1 = px.line(
        df,
        x='Date',
        y=df.columns[1:4],
        color_discrete_sequence=['#22594C', '#38947F', '#90D5C5'],
        # labels={
        #     'MONTH':'Month',
        #     'ACTIVE_CUSTOMER_1Y_ROLLING': 'Active Customers',
        #     'YEAR_CHART': 'Year'
        # },
        markers=True
    )
    fig_line1.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-0.5, xanchor='left', x=0, title=None),
    #     yaxis={'title': None},
    #     xaxis={'title': None},
        plot_bgcolor='#fff',
    #     # height=350,
    #     margin=dict(l=10, r=10, t=20, b=0)
    )

    return [fig1,fig2,fig3,fig_line1]


