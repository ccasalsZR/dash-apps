
# package imports
from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        html.Img(src='.\static\icon\docmorris-apotheke-logo-vector.svg', style={'width':'60%'} )
                    ],
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            )
        ]
    ),
    color='white',
    style={'height': '80px'}
)
