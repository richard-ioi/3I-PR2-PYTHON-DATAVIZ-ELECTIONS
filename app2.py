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
d121.columns = normaliseNames(d121)
d951.columns = normaliseNames(d951)
seinestdenis121 = departmentQuery('78', d121) #d121.query("code_du_département == '93'")

#Year dataframe
year_data = [['1995', d951], ['2002', d021], ['2007', d071], ['2012',d121], ['2017', d171]] 
df_year = pd.DataFrame(year_data, columns = ['year', 'associated_df']) 
  

fig = px.scatter(seinestdenis121, x=seinestdenis121['inscrits'], y=seinestdenis121['votants'], hover_name="libellé_de_la_commune", height=300, title="2012")
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="LightSteelBlue",
)
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
