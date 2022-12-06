
from ctypes import sizeof
import warnings
warnings.filterwarnings("ignore")

import dash
# import dash_auth
from dash import html, dcc # dash-html
import dash_bootstrap_components as dbc

import json

import datetime

from components import footer, navbar

# Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = json.loads(open('secrets/user_access.json', 'r').read())

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                use_pages=True,
                title='Logistics s',
                 )
server = app.server

# auth = dash_auth.BasicAuth(
#    app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([
    navbar,
    dash.page_container,
    # dbc.Container([
    #     html.Iframe(src='https://dub01.online.tableau.com/t/uap/views/LogisticsDashboardDEV/Dashboard?:toolbar=no&:embed=true', 
    #         width='100%', 
    #         height='827'
    #     ),
    # ]),
    footer
], style={'background': '#f8fcfb'})

# # ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)

