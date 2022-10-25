from ctypes import sizeof
import warnings
warnings.filterwarnings("ignore")

import dash
# import dash_auth
from dash import html, dcc # dash-html
import dash_bootstrap_components as dbc

from components import footer, navbar


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                # use_pages=True
                 )
server = app.server



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        html.Br(),
        html.H1('Engagement'),
        html.Br(),
        html.H1('Conversion'),
        html.Br(),
        html.H1('Teleclinic Conv.'),
        # dash.page_container,
        html.Br(),
    ]),
    footer
], style={'background': '#f8fcfb'})


# # ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)