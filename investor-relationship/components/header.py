
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
                            html.Img(src='.\static\icon\Group_logo_green.svg', style={'width':'10%'} )
                        ],
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                    href='/'
                )
            ])            
        ]
    ),
    color='white',
    style={'height': '80px'}
)
