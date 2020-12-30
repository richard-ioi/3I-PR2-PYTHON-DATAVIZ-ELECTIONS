# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8051/ in your web browser.

############ imports ###########
#from readFiles import departmentQuery
from readFiles import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from statistics import mean
from dash.dependencies import Input, Output


###### reading csv data files ############
#Data from the first and second rounds of the 1995 french presidential elections (round 1 : row 0 to 36671, round 2 : row X to Y)
d951 = pd.read_csv('data/election_1995_par_ville.csv', nrows=36671, low_memory=False)
d952 = pd.read_csv('data/election_1995_par_ville.csv', skiprows=36671, low_memory=False)
#Data from the first and second rounds of the 2002 french presidential elections 
d021 = pd.read_csv('data/election_2002_T1.csv' ,error_bad_lines=False, sep=';', low_memory=False)
d022 = pd.read_csv('data/election_2002_T2.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first and second rounds of the 2007 french presidential elections 
d071 = pd.read_csv('data/election_2007_T1.csv' ,error_bad_lines=False, sep=';', low_memory=False)
d072 = pd.read_csv('data/election_2007_T2.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first round of the 2012 french presidential elections
d121 = pd.read_csv('data/election_2012_T1.csv' ,error_bad_lines=False, sep=';', low_memory=False)
d122 = pd.read_csv('data/election_2012_T2.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first and second rounds of the 2017 french presidential elections 
d171 = pd.read_csv('data/election_2017_T1.csv' ,error_bad_lines=False, sep=';', low_memory=False)
d172 = pd.read_csv('data/election_2017_T2.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#removes disruptive characters from column names of csv files, lowers all characters
d951.columns = normaliseNames(d951)
d952.columns = normaliseNames(d952)
d021.columns = normaliseNames(d021)
d022.columns = normaliseNames(d022)
d071.columns = normaliseNames(d071)
d072.columns = normaliseNames(d072)
d121.columns = normaliseNames(d121)
d122.columns = normaliseNames(d122)
d171.columns = normaliseNames(d171)
d172.columns = normaliseNames(d172)

#Sub-dataframe
seinestdenis951 = departmentQuery('93', d951) 
seinestdenis021 = departmentQuery('93', d021)
seinestdenis071 = departmentQuery('93', d071)
seinestdenis121 = departmentQuery('93', d121) 
seinestdenis171 = departmentQuery('93', d171)
#Year dataframe
year_data = [['1995', d951], ['2002', d021], ['2007', d071], ['2012',d121], ['2017', d171]] 
df_year = pd.DataFrame(year_data, columns = ['year', 'associated_df']) 
  
#Figure test 
# fig = px.scatter(seinestdenis121, x=seinestdenis121['inscrits'], y=seinestdenis121['votants'], hover_name="libellé_de_la_commune", height=300, title="2012")
# fig.update_layout(
#     margin=dict(l=20, r=20, t=30, b=20),
#     paper_bgcolor="LightSteelBlue",
# )

############# map drawing ##########
# mapEurope = go.Figure(go.Scattergeo())
# mapEurope.update_geos(
#     visible=True, resolution=110, scope="europe",
#     fitbounds="locations",
#     showcountries=True, countrycolor="Black",
#     showsubunits=True, subunitcolor="Blue"
# )
# mapEurope.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
# mapEurope.show()

###### Moyenne des voix 2012###########
joly = d121['%_voix/ins_joly']

voixJoly = [voix for voix in joly]
voixJoly = commaToDot(voixJoly)
#voixJoly = stringToFloat(voixJoly)
print(voixJoly[:15])
floatJoly=[]
for i in range (1, len(voixJoly)):
    i = float(i)
    floatJoly.append(i)
moyenneJoly = mean(floatJoly)
print(moyenneJoly)
############## dash app ############
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
                    {'label': 'Premier tour', 'value': 'T1'},
                    {'label': 'Second tour', 'value': 'T2'}
                ],
                value="T1"
            )
        ]
    ),
    html.Div(
        children=[
            dcc.Dropdown(
                id='test-dropdown',
                options=[
                    {'label': 'Premier tour', 'value': 'T1'},
                    {'label': 'Second tour', 'value': 'T2'}
                ],
                value="T1"
             )#,
            # dcc.Graph(
            #     id='test-graph',
            #     figure=fig
            # )
        ]
    ), 
    html.Div(
        children=[
            dcc.Graph(id='test-graph'),
            html.P("Selectionner l'année"),
            dcc.RangeSlider(
                id='year-slider',
                min=1995,
                max=2017,
                step=None,
                marks={
                    1995: '1995',
                    2002: '2002',
                    2007: '2007',
                    2012: '2012',
                    2017: '2017'
                },
                value=[1995]
            )  
        ]
    )
])
@app.callback(
    Output('test-graph', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year): 
    print(selected_year)
    
    param_name = seinestdenis021

    if(selected_year == 1995):
        print("this works")
        df_selected_year = d951
        param_name = seinestdenis951
    elif(selected_year == 2002):
        df_selected_year = d021
        param_name = seinestdenis021
    elif(selected_year == 2007):
        df_selected_year = d071
        param_name = seinestdenis071
    elif(selected_year == 2012):
        df_selected_year = d121
        param_name = seinestdenis121
    elif(selected_year == 2017):
        df_selected_year = d171
        param_name = seinestdenis171
    fig = px.scatter(df_selected_year, x=param_name['inscrits'], y=param_name['votants'],
                      hover_name=param_name['libellé_de_la_commune'], height=300, title="selected_year")
    fig.update_layout(transition_duration=500, margin=dict(l=20, r=20, t=30, b=20))
    print(df_selected_year['inscrits'][0])
    return fig
if __name__ == '__main__':
    app.run_server(debug=True, port=8051 )

