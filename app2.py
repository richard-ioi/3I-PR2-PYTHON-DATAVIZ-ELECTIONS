# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8051/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('data/resultats_communes_T1_2012.csv' ,error_bad_lines=False, sep=';')#, low_memory=False)
#removes disruptive characters from column names 
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
print(df.columns)
seinestdenis = df.query("libellé_du_département == 'SEINE SAINT-DENIS'")

fig = px.scatter(df, x=seinestdenis['inscrits'], y=seinestdenis['votants'])


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Elections présidentielles françaises depuis 1995'),
  
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051 )