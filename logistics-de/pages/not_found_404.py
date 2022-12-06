from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container([
    html.Br(),
    html.H1("Error 404 Page not found"),
    html.Br(),
])