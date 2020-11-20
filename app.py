# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Elections présidentielles françaises depuis 1995'),

    html.Div(children='''
        Dash: A web application framework for Python.
    ''')])


if __name__ == '__main__':
    app.run_server(debug=True)