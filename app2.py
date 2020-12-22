# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8051/ in your web browser.
from readFiles import departmentQuery
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
###### reading csv data files ############
#Data from the first round of the 2012 french presidential elections
d121 = pd.read_csv('data/resultats_communes_T1_2012.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first round of the 1995 french presidential elections (row 0 to 36671)
d951 = pd.read_csv('data/elections_1995_par_ville.csv', nrows=36671, low_memory=False)
d952 = pd.read_csv('data/elections_1995_par_ville.csv', skiprows=36671, low_memory=False)
#removes disruptive characters from column names of csv files, lowers all characters
d121.columns = d121.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
d951.columns = d951.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')

seinestdenis121 = departmentQuery('93', d121) #d121.query("code_du_département == '93'")

fig = px.scatter(seinestdenis121, x=seinestdenis121['inscrits'], y=seinestdenis121['%_vot/ins'], hover_name="libellé_de_la_commune", height=300, title="2012")
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="LightSteelBlue",
)

app = dash.Dash(__name__, title="Analyse des données d'élections")#, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1(children='Elections présidentielles françaises depuis 1995'),
  
    html.P(children='''
        Dash: A web application framework for Python.
    '''),
    
    html.Div(
        className='drop-down-year',
        children=[ 
            dcc.Dropdown(
                options=[
                    {'label': '1995', 'value': '1995'},
                    {'label': '2002', 'value': '2002'},
                    {'label': '2007', 'value': '2007'},
                    {'label':'2012', 'value':'2012'},
                    {'label':'2017', 'value':'2017'}
                ],
                placeholder="Sélectionnez une année"
            ),
            dcc.Graph(
                id='life-exp-vs-gdp',
                figure=fig
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051 )
