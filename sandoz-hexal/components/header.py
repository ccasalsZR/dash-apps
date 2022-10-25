
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
                        dbc.Col(
                            html.Img(src='.\static\icon\docmorris-apotheke-logo-vector.svg', height="200px"))
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            )
        ]
    ),
    color='white',
    style={'height': '80px'}
)
