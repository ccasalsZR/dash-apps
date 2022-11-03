
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import FilterExpression


import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets.json'


# TESTING TO BE DELETED

def get_file_download(start_date,end_date):

    # """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="fileName")],
        metrics=[Metric(name="eventCount")
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="fileExtension",
                string_filter=Filter.StringFilter(value="pdf"),
            )
        ),
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"fileName": row.dimension_values[0].value,
            "eventCount": row.metric_values[0].value,
        })
    df = pd.DataFrame(output)

    # Casting the metrics from the API call
    df = df.astype({'fileName':'string',
        'eventCount':'int'
    })

    df = df[(df['fileName'] != '') & (df['fileName'] != '(other)')]

    fig1 = go.Figure(go.Indicator(
        mode="number",
        value=df['eventCount'].sum(),
        domain={"x": [0, 1], "y": [0, 1]},
        number={
            "font": {"size": 50, 'color': '#22594c'},
        },
    ))
    fig1.update_layout(
        height=100,
    )

    # return 

# get_file_download('2022-10-01','2022-10-10')



def get_url_link(start_date,end_date):

    # """Runs a simple report on a Google Analytics 4 property."""
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()
    property_id = '283963042'

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="videoUrl")],
        metrics=[Metric(name="eventCount")
            ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        # dimension_filter=FilterExpression(
        #     filter=Filter(
        #         field_name="fileExtension",
        #         string_filter=Filter.StringFilter(value="pdf"),
        #     )
        # ),
    )
    response = client.run_report(request)

    output = []
    for row in response.rows:
        output.append({"linkUrl": row.dimension_values[0].value,
            "eventCount": row.metric_values[0].value,
        })
    df = pd.DataFrame(output)

    # Casting the metrics from the API call
    df = df.astype({'linkUrl':'string',
        'eventCount':'int'
    })

    # df = df[(df['fileName'] != '') & (df['fileName'] != '(other)')]

    # df = df[df['linkUrl'].str.contains('teleclinic')]

    print(df.head(50))


    # return 

get_url_link('2022-10-01','2022-11-10')