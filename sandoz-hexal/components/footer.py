

# package imports
from dash import html

footer = html.Footer([
        html.Img(src='.\static\icon\Group_logo_white.svg',
                 height="50px", style={'padding-top': '10px'}),
        html.P("© 2022", style={'color': 'white', 'font-size': 'small'})
    ], style={'background': '#22594c', 'height': '100px', 'padding-left': '5px'}
    )