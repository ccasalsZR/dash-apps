

# package imports
from dash import html
import dash_bootstrap_components as dbc

from datetime import date



footer = html.Div([
    dbc.CardFooter([
        dbc.Col([
            html.A([
                html.Img(
                    src='.\static\icon\docmorris_heart.png',
                    height="60px", 
                    style={'padding-top': '10px','padding-bottom':'5px'},
                )
            ], href='https://www.docmorris.de/')
        ],className = 'd-flex justify-content-center'),
        dbc.Col([
            html.P("© " + str(date.today().year), style={'color': '#90D5C5', 'font-size': 'small'})
        ],className = 'd-flex justify-content-center'),
    ])
],style={'background': '#22594c', 'height': '100px', 'padding-left': '5px', 'justify':'center'})