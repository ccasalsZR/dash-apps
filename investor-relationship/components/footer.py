

# package imports
from dash import html
import dash_bootstrap_components as dbc

from datetime import date



footer = html.Div([
    dbc.CardFooter([
        dbc.Col([
            html.A([
                html.Img(
                    src='.\static\icon\Group_logo_white.svg',
                    height="60px", 
                    style={'padding-top': '10px','padding-bottom':'5px'},
                )
            ], href='https://zurrosegroup.com/en/')
        ]),
        dbc.Col([
            html.P("© " + str(date.today().year), style={'color': '#90D5C5', 'font-size': 'small'})
        ],
        ),        
    ])
],style={'background': '#22594c'})   