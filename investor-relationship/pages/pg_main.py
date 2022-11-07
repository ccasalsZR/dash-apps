

from random import random
from dash import html, callback, Output, Input, dcc

import os
# from dotenv import load_dotenv
# import snowflake.connector as snow


import dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta


# from web_sections import main_1_engagement, main_2_conversion, main_3_teleclinic, main_4_marketing


dash.register_page(
    __name__,
    path='/',
    title='Sandoz Hexal - DocMorris Analytics'
) # Home page

layout = html.Div([
    html.Br()
])