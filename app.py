# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('data/elections_2012_par_ville.csv' ,low_memory = False)
#Renommage de colonnes 
#code de département et libe
df.rename(columns={'Libellé du département': 'Libellé_du_département', 'Code du département':'Code_du_département', 'Code de la commune':'Code_de_la_commune'
                    , 'Libellé de la commune':'Libellé_de_la_commune', '% Abs/Ins':'%_Abs/Ins', '% Vot/Ins':'%_Vot/Ins', 'Blancs et nuls':'Blancs_et_nuls' }, inplace=True)
#Dictionnaire d'accès aux candidats
#joly, indice 16
mapping = {df.columns[16]:"NomJoly", df.columns[17]:"PrénomJoly", df.columns[18]:"VoixJoly", df.columns[19]:"Joly"}

inscrits = df['Inscrits']
votants = df['Votants']
departements = df['Libellé_du_département']
departement = 'SEINE SAINT-DENIS'
seinestdenis = df.query("Libellé_du_département == 'SEINE SAINT-DENIS'")

# fig = go.Scatter(
#     x=seinestdenis['Inscrits'],
#     y=seinestdenis['Votants'],
#     mode='markers',
# )
#, color="Code_du_département"
fig = px.scatter(df, x=seinestdenis['Inscrits'], y=seinestdenis['Votants'])
                 #size=seinestdenis['Abstentions'])
                 #log_x=True, size_max=60)



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div(children=[
#     html.H1(children='Elections présidentielles françaises depuis 1995'),

#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),
#     dcc.Graph(
#         id='votants_inscrits',
#         figure =trace
#     ),
#       html.Div(children=f'''
#                                 Le graphique ci-dessus montre le nombre de votants en fonction des 
#                                 Inscriptions aux elections presientielles de 2012 en 
#                                 Seine Saint-Denis.
#                             '''),
#     ]),
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
    app.run_server(debug=True)