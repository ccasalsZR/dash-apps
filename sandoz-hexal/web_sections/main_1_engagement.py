
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

import datetime

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression


     
# """Runs a simple report on a Google Analytics 4 property."""
# Using a default constructor instructs the client to use the credentials
# specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
client = BetaAnalyticsDataClient()
property_id = '283963042'


def api_call_date_level(start_date,end_date,value_filter):
    # Documentation for Dims and Metrics:
    # https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="activeUsers"), # distinct users
            Metric(name='screenPageViews'), # The number of app screens or web pages your users viewed
            Metric(name='averageSessionDuration'), # The average duration (in seconds) of users' sessions.
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter = FilterExpression (
            filter = Filter (
                field_name = 'pagePath',
                string_filter = Filter.StringFilter(
                    value = value_filter,
                    match_type = Filter.StringFilter.MatchType(2), # 2 == BEGINS_WITH
                ),
            )
        )
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"Date": row.dimension_values[0].value,
            "Sessions": row.metric_values[0].value,
            "New Users": row.metric_values[1].value,
            "Active Users": row.metric_values[2].value,
            "Page Views": row.metric_values[3].value,
            "Avg. Session Duration": row.metric_values[4].value,
        })
    df = pd.DataFrame(output)


    # Casting the metrics from the API call
    df = df.astype({'Sessions':'int',
        'New Users':'int',
        'Active Users':'int',
        'Page Views':'int',
        'Avg. Session Duration':'float32',
    })
    
    # sort dataframe
    df = df.sort_values(by=['Date'])

    return df



def update_main_sec1(start_date,end_date,treatment):


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
        # dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions"),
            Metric(name="newUsers"),
            Metric(name="activeUsers"), # distinct users
            Metric(name='screenPageViews'), # The number of app screens or web pages your users viewed
            Metric(name='averageSessionDuration'), # The average duration (in seconds) of users' sessions.
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter = FilterExpression (
            filter = Filter (
                field_name = 'pagePath',
                string_filter = Filter.StringFilter(
                    value = value_filter,
                    match_type = Filter.StringFilter.MatchType(2), # 2 == BEGINS_WITH
                ),
            )
        )
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({ # "Date": row.dimension_values[0].value,
            "Sessions": row.metric_values[0].value,
            "New Users": row.metric_values[1].value,
            "Active Users": row.metric_values[2].value,
            "Page Views": row.metric_values[3].value,
            "Avg. Session Duration": row.metric_values[4].value,
        })
    df = pd.DataFrame(output)


    # Casting the metrics from the API call
    df = df.astype({'Sessions':'int',
        'New Users':'int',
        'Active Users':'int',
        'Page Views':'int',
        'Avg. Session Duration':'float32',
    })

    # # sort dataframe
    # df = df.sort_values(by=['Date'])


    # GENERATION OF THE VISUAL ------------------------------------------------------
    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=df['Sessions'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat': ",.0f",
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
            'valueformat': ",.0f",
        },
    ))
    fig3.update_layout(
        height=100,
    )

    fig4 = go.Figure(go.Indicator(
        mode="number",
        value=df['Page Views'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'valueformat': ",.0f",
        },
    ))
    fig4.update_layout(
        height=100,
    )

    fig5 = go.Figure(go.Indicator(
        mode="number",
        value=df['Avg. Session Duration'].mean(), # datetime.timedelta(seconds=df['Avg. Session Duration'].sum()),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
            'suffix':'s',
        },
    ))
    fig5.update_layout(
        height=100,
    )

    # Line chart for the evolution of the metrics above

    dff = api_call_date_level(start_date,end_date,value_filter)

    fig_line1 = px.line(
        dff,
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


    # DONUT visual

    df_donut = df.copy()

    df_donut = df_donut[['Active Users','New Users']]
    df_donut['Repeat Users'] = df_donut['Active Users'] - df_donut['New Users']
    df_donut.drop(columns=['Active Users'],inplace=True)

    df_donut = df_donut.sum(axis=0)


    fig_donut = px.pie(
        values=df_donut,
        names=['New Users','Repeat Users'],
        color_discrete_sequence = ['#38947F', '#90D5C5'],
        hole = .5
    )
    fig_donut.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-0.5, xanchor='left', x=0, title=None),
    )

    # reusable purposes we bring back this KPI
    act_users = df['Active Users'].sum()

    return [fig1,fig2,fig3,fig4,fig5,fig_line1,fig_donut,act_users]





