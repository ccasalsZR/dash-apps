from ctypes import sizeof
import warnings
warnings.filterwarnings("ignore")

import dash
import dash_auth
from dash import html, dcc # dash-html
import dash_bootstrap_components as dbc

from components import footer, navbar

import json

import os
from dotenv import load_dotenv

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = json.loads(open('secrets/user_access.json', 'r').read())

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/secrets.json'

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                use_pages=True,
                 )
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    navbar,
    dash.page_container,
    footer
], style={'background': '#f8fcfb'})


# # ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)