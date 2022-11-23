
# package imports
from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Col([
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            html.Img(src='.\static\icon\docmorris-apotheke-logo-vector.svg', style={'width':'15%'} )
                        ],
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                    href='/'
                )
            ]),
            html.Img(src='.\static\icon\Logo_Hexal.svg', style={'width':'8%'}),
            html.Img(src='.\static\icon\Logo_1_A_Pharma.png', style={'width':'5%'})
        ]
    ),
    color='white',
    style={'height': '80px'}
)
