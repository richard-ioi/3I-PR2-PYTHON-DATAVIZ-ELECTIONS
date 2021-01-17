# -*- coding: utf-8 -*-

# Run this app with `python main.py` and
# visit localhost:8051/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import io
import json
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from urllib.request import urlopen
from appFunctions import normalise_names
from appFunctions import department_query
from appFunctions import comma_to_dot
from appFunctions import add_zeros_ewt
from appFunctions import reformat_department

print("Chargement des données...")

# The following section is used to import and read the csv files used in the program
#Dataframe from the first and second rounds of the 1995 french presidential elections (round 1 : row 0 to 36671, round 2 : row X to Y)
df_951 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_1995_par_ville.csv").content.decode('utf-8')), nrows=36671, low_memory=False)
df_952 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_1995_par_ville.csv").content.decode('utf-8')), skiprows=36671, low_memory=False)
#Dataframe from the first and second rounds of the 2002 french presidential elections 
df_021 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T1.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
df_022 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T2.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Dataframe from the first and second rounds of the 2007 french presidential elections 
df_071 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T1.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
df_072 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T2.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Dataframe from the first round of the 2012 french presidential elections
df_121 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T1.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
df_122 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T2.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Dataframe from the first and second rounds of the 2017 french presidential elections 
df_171 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T1.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
df_172 = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T2.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Dataframe providing information such as the coordinates for all the main towns of France
df_main_town = pd.read_csv(io.StringIO(requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/code_cheflieux.csv").content.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#removes disruptive characters from column names of dataframes lowers all characters
df_951.columns = normalise_names(df_951)
df_952.columns = normalise_names(df_952)
df_021.columns = normalise_names(df_021)
df_022.columns = normalise_names(df_022)
df_071.columns = normalise_names(df_071)
df_072.columns = normalise_names(df_072)
df_121.columns = normalise_names(df_121)
df_122.columns = normalise_names(df_122)
df_171.columns = normalise_names(df_171)
df_172.columns = normalise_names(df_172)

# Dictionnary with department codes as keys and names as values 
department_names = {
    '1': 'Ain', '2': 'Aisne', '3': 'Allier', '4': 'Alpes-de-Haute-Provence', '5': 'Hautes-Alpes','6': 'Alpes-Maritimes', 
    '7': 'Ardèche', '8': 'Ardennes', '9': 'Ariège', '10': 'Aube', '11': 'Aude','12': 'Aveyron', '13': 'Bouches-du-Rhône', 
    '14': 'Calvados', '15': 'Cantal', '16': 'Charente', '17': 'Charente-Maritime', '18': 'Cher', '19': 'Corrèze', '2A': 'Corse-du-Sud', 
    '2B': 'Haute-Corse', '21': 'Côte-d\'Or', '22': 'Côtes-d\'Armor', '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs', '26': 'Drôme',
    '27': 'Eure', '28': 'Eure-et-Loir', '29': 'Finistère', '30': 'Gard', '31': 'Haute-Garonne', '32': 'Gers','33': 'Gironde', '34': 'Hérault', 
    '35': 'Ille-et-Vilaine', '36': 'Indre', '37': 'Indre-et-Loire','38': 'Isère', '39': 'Jura', '40': 'Landes', '41': 'Loir-et-Cher', 
    '42': 'Loire', '43': 'Haute-Loire','44': 'Loire-Atlantique', '45': 'Loiret', '46': 'Lot', '47': 'Lot-et-Garonne', '48': 'Lozère',
    '49': 'Maine-et-Loire', '50': 'Manche', '51': 'Marne', '52': 'Haute-Marne', '53': 'Mayenne','54': 'Meurthe-et-Moselle', '55': 'Meuse', 
    '56': 'Morbihan', '57': 'Moselle', '58': 'Nièvre', '59': 'Nord','60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais', '63': 'Puy-de-Dôme', 
    '64': 'Pyrénées-Atlantiques','65': 'Hautes-Pyrénées', '66': 'Pyrénées-Orientales', '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône',
    '70': 'Haute-Saône', '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie', '74': 'Haute-Savoie','75': 'Paris', '76': 'Seine-Maritime', 
    '77': 'Seine-et-Marne', '78': 'Yvelines', '79': 'Deux-Sèvres','80': 'Somme', '81': 'Tarn', '82': 'Tarn-et-Garonne', 
    '83': 'Var', '84': 'Vaucluse', '85': 'Vendée','86': 'Vienne', '87': 'Haute-Vienne', '88': 'Vosges', '89': 'Yonne', '90': 'Territoire de Belfort',
    '91': 'Essonne', '92': 'Hauts-de-Seine', '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne', '95': 'Val-d\'Oise',
}
#Dictionnary with years as keys and an array of the associated dataframes as values
year_name = {
    1995 : [df_951, df_952],
    2002 : [df_021, df_022],
    2007 : [df_071, df_072],
    2012 : [df_121, df_122],
    2017 : [df_171, df_172]
}

def main_town(code):
    """Queries df_main_town to create a sub-frame depending on the selected departement.

    Parameters:
    code(string): the code of the required departement, a number between 1 ad 95.

    Returns:
    dataframe: Sub-frame holding data from the selected departement.
    """
    return df_main_town.query(f'code== "{code}"')['geom_x_y'].iloc[0]

def participation_rate_department(dYear):
    """Calculates the average participation rate in  each department in order to create a dataframe containing the following columns : 
    code, taux_de_participation, dep_names. This method is used in the choropleth map.

    Parameters:
    dYear(dataframe) : Chosen election year.

    Returns:
    dataframe: New dataframe with 3 columns.
    """
    dT={}
    department_list=[]
    for i in department_names.keys():
        department_list.append(department_names.get(i))
        vD=department_query(i,dYear)
        average=0
        for j in (vD['%_vot/ins']):
            vS=j
            vS=vS.replace(',','.')
            average+=float(vS)
        i=reformat_department(str(i))
        dT[i]=[average/vD['%_vot/ins'].size]

    df_rate=pd.DataFrame.from_dict(dT,orient='index',columns=['taux_de_participation'])
    df_rate=df_rate.reset_index()
    df_rate=df_rate.rename(columns={'index':'code'})
    d_department_series=pd.Series(department_list,name='dep_names')
    df_rate=pd.concat([df_rate,d_department_series], axis=1)
    return df_rate

def participation_rate_town(dYear,code):
    """Calculates the participation rate for each town in a given department in order to create a dataframe containing the following columns:
    code, %_vot/ins.

    Parameters:
    dYear(dataframe): Chosen election year.
    code(str): Chosen department

    Returns:
    dataframe: New dataframe with 2 columns.
    """
    dep=code
    if(code[0]=='0'):
        dep=code[1]
    df_rate=department_query(dep,dYear)
    df_rate=df_rate.rename(columns={'code_de_la_commune':'code'})
    df_rate=df_rate.reset_index()
    add_zeros_ewt(df_rate, code)
    for i in range (df_rate['%_vot/ins'].size):
        df_rate.loc[i,'%_vot/ins']=float(df_rate.loc[i,'%_vot/ins'].replace(',','.'))
    df_rate['code']=df_rate['code'].astype(str)
    df_rate['%_vot/ins']=df_rate['%_vot/ins'].astype(float)
    return df_rate

def election_winner_town(dYear,code):
    """Finds the winner of the election for each town in a given department in order to create a dataframe containing the following columns:
    code, gagnant, voix, libellé_de_la_commune.

    Parameters:
    dYear(dataframe): Chosen election year.
    code(str): Chosen department

    Returns:
    dataframe: New dataframe with 4 columns.
    """
    dT={}
    dMax=[]
    dep=code
    if(code[0]=='0'):
        dep=code[1]
    dCand=department_query(dep,dYear)
    dCand=dCand.rename(columns={'code_de_la_commune':'code'})
    dCand['code']=dCand['code'].astype(str)
    dCand=dCand.reset_index()
    add_zeros_ewt(dCand, code)
    vCompt=0
    dVille=[]
    for x in dCand['code']:
        vC=''
        vCint=0
        max=0
        winner=''
        while('%_voix/exp'+vC in dCand):
            if(float((str(dCand.loc[vCompt]['%_voix/exp'+str(vC)])).replace(',','.'))>max):
                max=float((dCand.loc[vCompt]['%_voix/exp'+str(vC)]).replace(',','.'))
                winner=str(dCand.loc[vCompt]['nom'+str(vC)])+' '+str(dCand.loc[vCompt]['prénom'+str(vC)])
            vCint=vCint+1
            vC=str(vCint)
        dT[x]=winner
        dMax.append(max)
        dVille.append(dCand.loc[vCompt]['libellé_de_la_commune'])
        vCompt=vCompt+1
    dFinal=pd.DataFrame.from_dict(dT,orient='index',columns=['gagnant'])
    dFinal=dFinal.reset_index()
    dFinal=dFinal.rename(columns={'index':'code'})
    dMaxSeries=pd.Series(dMax,name='voix')
    dVilleSeries=pd.Series(dVille,name='libellé_de_la_commune')
    dFinal=pd.concat([dFinal,dMaxSeries,dVilleSeries], axis=1)
    return dFinal

def election_winner_department(dYear):
    """Finds the winner of the election for each department in order to create a dataframe containing the following columns:
    code, gagnant, dep_names.

    Parameters:
    dYear(dataframe): Chosen election year.

    Returns:
    dataframe: New dataframe with 3 columns.
    """
    dT={}
    department_list=[]
    for i in department_names.keys():
        department_list.append(department_names.get(i))
        vD=election_winner_town(dYear,i)
        df_candidates={}
        for j in vD['gagnant']:
            if(j not in df_candidates):
                df_candidates[j]=1
            else:
                df_candidates[j]=df_candidates[j]+1
        max=0
        winner=''
        for k in df_candidates.keys():
            if(int(df_candidates.get(k))>max):
                max=int(df_candidates.get(k))
                winner=k
        i=reformat_department(str(i))
        dT[i]=winner

    dFinal=pd.DataFrame.from_dict(dT,orient='index',columns=['gagnant'])
    dFinal=dFinal.reset_index()
    dFinal=dFinal.rename(columns={'index':'code'})
    dDepartmentSeries=pd.Series(department_list,name='dep_names')
    dFinal=pd.concat([dFinal,dDepartmentSeries], axis=1)
    return dFinal

def dict_selection(selected_year,selected_round):
    if(selected_round == 'T1'):
        return year_name.get(selected_year[0])[0]
    elif(selected_round == 'T2'):
        return year_name.get(selected_year[0])[1]

############## dash app ############
app = dash.Dash(__name__, title="Elections Présidentielles")
app.layout = html.Div([
    html.Div( className='app-header',
            children=[
                html.H1(children='Elections présidentielles françaises'),
                html.H2(children='de 1995 à 2017'),
            
                html.P(children='''
                    Cette application a été conçue dans le but d'analyser 
                    les résultats des élections présidentielles en France métropolitaine.
                '''),
                html.P(children='''
                    Grâce aux diverses options, vous pourez mettre en évidence les disparités 
                    des votes et l'orientation politique des citoyens à échelle nationale ou départementale au cours des 5 dernières élections.
                '''),
                html.P(children='''
                    Projet E3FI par Richard FOUQUOIRE & Emily RENARD
                    '''),
                html.P(children='''
                    Tracés des départements et villes par Grégoire David, traduits du format SHP fourni par l'IGN vers le format GeoJSON:  https://github.com/gregoiredavid/france-geojson
                '''),
                html.P(children='''
                    Données des élections fournies par le site data.gouv.fr
                ''')
            ]
    ),
    
    html.Div(className='inline-graph',
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[
                                html.H4(children="Département"),
                                dcc.Dropdown(
                                    id='departments',
                                    options=[
                                        {'label': str(i)+" - "+j, 'value': i} for i, j in department_names.items()
                                    ],
                                    value='1',
                                    clearable=False
                                ),
                                html.H4(children="Tour"),
                                dcc.Dropdown(
                                    id='round-select',
                                    options=[
                                        {'label': 'Premier tour', 'value': 'T1'},
                                        {'label': 'Second tour', 'value': 'T2'}
                                    ],
                                    value="T1",
                                    clearable=False
                                ),
                                html.H4(children="Election"),
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
                            ]),
                            html.Div(className='map-options', children=[
                                html.H3(children='Options de carte'), 
                                html.H4(children='Echelle'),
                                dcc.RadioItems(
                                    id="map-scale",
                                    options=[
                                        {'label': 'Nationale', 'value': 'fr'},
                                        {'label': 'Départementale', 'value': 'dep'}
                                    ],
                                    value='fr'
                                ),
                                html.H4(children='Données'),
                                dcc.RadioItems(
                                    id="map-format",
                                    options=[
                                        {'label': 'Taux de participation', 'value': 'participation'},
                                        {'label': 'Candidats', 'value': 'candidat'}
                                    ],
                                    value='participation'
                                )
                            ])   
                        ]
                    ),
            
            html.Div([
                dcc.Graph(id='map-box')
            ]),
            html.Div(className='chart-alignment', children=[
                html.Div(className="align-elements", children=[
                    html.Div([
                        dcc.Dropdown(
                            id='axis-categories1',
                            options=[
                                {'label': 'Inscrits', 'value': 'inscrits'},
                                {'label': 'Abstentions', 'value': 'abstentions'},
                                {'label': 'Votants', 'value': 'votants'},
                                {'label': '% Votes par inscrits', 'value':'%_vot/ins'},
                                {'label' : '% Votes Blancs et Nuls par votes', 'value': '%_blnuls/ins'}
                            ],
                            value="inscrits",
                                        clearable=False
                                    )
                                ]),
                    html.Div([
                        dcc.Dropdown(
                            id='axis-categories2',
                            options=[
                                {'label': 'Inscrits', 'value': 'inscrits'},
                                {'label': 'Abstentions', 'value': 'abstentions'},
                                {'label': 'Votants', 'value': 'votants'},
                                {'label': '% Votes par inscrits', 'value':'%_vot/ins'},
                                {'label' : '% Votes Blancs et Nuls par votes', 'value': '%_blnuls/ins'}
                            ],
                            value="votants",
                            clearable=False
                        )
                    ])
                ]),
                html.Div([
                    dcc.Graph(id='scatter-graph')
                ]), 
                html.Div(className='align-elements', children=[
                    html.Div([
                        dcc.Graph(id='histogram'),
                    ]),        
                    html.Div([
                        dcc.Graph(id='candidats-piechart')
                    ])    
                 ])
            ])
                
        ]
    )
])
@app.callback(
   Output('scatter-graph', 'figure'),
   Input('departments', 'value'),
   Input('year-slider', 'value'),
   Input('round-select', 'value'),
   Input('axis-categories1', 'value'),
   Input('axis-categories2', 'value')
)
def update_figure(selected_departement, selected_year, selected_round, selected_c1, selected_c2):
    """Callback function used to update the scatter graph of the app.

    Parameters:
    selected_department(str): Value of selected the department from the dropdown.
    selected_year(int): Value of selected the election year from the slider.
    selected_round(str): Value of selected the election round from the dropdown.
    selected_c1(str): Value of selected data to be show on x-axis from the dropdown.
    selected_c2(str): Value of selected data to be show on y-axis from the dropdown.

    Returns:
    figure : Scatter graph.
    """
    global filtered_df
    filtered_df=department_query(selected_departement,dict_selection(selected_year,selected_round))

    fig1 = px.scatter(filtered_df, x=selected_c1, y=selected_c2, hover_name="libellé_de_la_commune", title=""+str(selected_c2)+" en fonction des "+ str(selected_c1) +" dans le "+str(selected_departement)+" en "+str(selected_year[0]))
    fig1.update_layout(
        margin=dict(l=2, r=2, t=30, b=2),
        height=200, width=600,
        font=dict(size=10),
        title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig1
@app.callback(
    Output('histogram', 'figure'),
    Input('departments', 'value'),
    Input('round-select', 'value')
)
def update_historgram(selected_departement, selected_round):
    """Callback function that renders a histogram showing the participation rate over the past 5 elections.
    The histogram contains 5 overlaid traces, 4 of which are masked upon launching the app.

    Parameters:
    selected_department(str): Value of selected the department from the dropdown.
    selected_round(str): Value of selected the election round from the dropdown.

    Returns:
    figure: Histogram.
    """
    global x0, x1, x2, x3, x4
    if(selected_round == 'T1'):
            x0 = department_query(selected_departement, df_951)
            x1 = department_query(selected_departement, df_021)
            x2 = department_query(selected_departement, df_071)
            x3 = department_query(selected_departement, df_121)
            x4 = department_query(selected_departement, df_171)
    elif(selected_round == 'T2'):
            x0 = department_query(selected_departement, df_952)
            x1 = department_query(selected_departement, df_022)
            x2 = department_query(selected_departement, df_072)
            x3 = department_query(selected_departement, df_122)
            x4 = department_query(selected_departement, df_172)    

    fig= go.Figure()
    fig.add_trace(go.Histogram(name='1995', x = comma_to_dot(x0['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2002', visible='legendonly', x = comma_to_dot(x1['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2007', visible='legendonly', x = comma_to_dot(x2['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2012', visible='legendonly', x = comma_to_dot(x3['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2017', visible='legendonly', x = comma_to_dot(x4['%_vot/ins'])))
    fig.update_layout(barmode='overlay',
                        margin=dict(l=0, r=0, t=40, b=0),
                        font=dict(
                            size=10),
                        title={
                            'text': "Taux de participation dans le <br>"+str(selected_departement)+" entre 1995 et 2017",
                            'y':0.95,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'bottom'
                        },
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01),
                        width=300, height=300)
    fig.update_traces(opacity=0.50)
    return fig

@app.callback(
    Output('map-box', 'figure'),
    Input('year-slider', 'value'),
    Input('round-select', 'value'),
    Input('map-scale', 'value'),
    Input('map-format', 'value'),
    Input('departments', 'value')
)
def update_map(selected_year, selected_round, selected_scale, selected_format, selected_departement):
    """ Callback function that renders the map of France showing the participation rate or the winning candidate
    of each department or town depending on the chosen scale and the chosen data.

    Parameters:
    selected_year(int): Value of selected the election year from the slider.
    selected_round(str): Value of selected the election round from the dropdown.
    selected_scale(str): Value of the selected scale, either 'fr' or 'dep'.
    selected_format(str): Value of the selected format which determines the data to be shown, either 'participation' or 'candidat'.
    selected_department(str): Value of selected the department from the dropdown.

    Returns:
    figure: Choropleth map of France.
    """
    global map

    depart=reformat_department(selected_departement)
    df_selection=dict_selection(selected_year,selected_round)

    # Opening geojson file for national scale and setting the view to the center for France. 
    if(selected_scale =='fr'):
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            geo = json.load(response)
        vLat=47.5
        vLon=2.6
        vZoom=4.4
        vHoverLoc='Libellé du département'
    # Opening geojson file for department scale and setting the center of the view to the coordinates of the main town of the department     
    elif(selected_scale =='dep'):
        with urlopen('http://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/communes/communes-'+depart+'.geojson') as response:
            geo = json.load(response)
        vCoordinates=main_town(depart)
        vLat=float(vCoordinates[:12])
        vLon=float(vCoordinates[14:])
        vZoom=7
        vHoverLoc='Libellé de la commune'

    # The following lines set the map dataframe depending on the selected inputs
    if(selected_format=='participation'):
        vColor='Taux de participation (%)'
        if(selected_scale=='fr'):
            df_final=participation_rate_department(df_selection)
            df_final.rename(columns={'taux_de_participation':'Taux de participation (%)','dep_names':'Libellé du département'},inplace=True)
        elif(selected_scale=='dep'):
            df_final=participation_rate_town(df_selection,depart)
            df_final.rename(columns={'%_vot/ins':'Taux de participation (%)','libellé_de_la_commune':'Libellé de la commune'},inplace=True)

    elif(selected_format=='candidat'):
        vColor='Candidat gagnant'
        if(selected_scale=='fr'):
            df_final=election_winner_department(df_selection)
            df_final.rename(columns={'dep_names':'Libellé du département','gagnant':'Candidat gagnant'},inplace=True)
        elif(selected_scale=='dep'):
            df_final=election_winner_town(df_selection,depart)
            df_final.rename(columns={'libellé_de_la_commune':'Libellé de la commune','gagnant':'Candidat gagnant'},inplace=True)

    # Map configuration
    map = px.choropleth_mapbox(df_final, geojson=geo, color=vColor,
                            locations="code", featureidkey="properties.code",
                            center={"lat": vLat, "lon": vLon},
                            mapbox_style="carto-positron", zoom=vZoom,
                            hover_data={vHoverLoc}
                        )
    map.update_geos(fitbounds="locations", visible=False)
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    width=550, height=650,
                    font=dict(size=10)
    )
    if(selected_format=='participation'):
        map.update_layout(coloraxis_colorscale='RdBu')
    return map

@app.callback(
    Output('candidats-piechart', 'figure'),
    Input('year-slider', 'value'),
    Input('round-select', 'value'),
    Input('map-scale', 'value'),
    Input('departments', 'value')
)
def update_piechart(selected_year, selected_round, selected_format, selected_departement):
    """ Callback function that renders a piechart showing the popularity of each candidate in a given department.

    Parameters:
    selected_year(int): Value of selected the election year from the slider.
    selected_round(str): Value of selected the election round from the dropdown.
    selected_format(str): Value of the selected format which determines the data to be shown, either 'participation' or 'candidat'.
    selected_department(str): Value of selected the department from the dropdown.

    Returns:
    figure: Piechart.
    """
    global filtered_df

    depart=reformat_department(selected_departement)

    filtered_df=election_winner_town(dict_selection(selected_year,selected_round),depart)

    fig1 = px.pie(filtered_df, values='voix', names='gagnant', title='Répartition des voix',color_discrete_sequence=px.colors.sequential.ice)
    fig1.update_layout(
        margin=dict(l=50, r=0, t=50, b=0),
        height=350, width=400,
        legend=dict( yanchor="top",
                    y=-0.54,
                    xanchor="left",
                    x=0.01),
        font=dict(size=10),
        title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig1

if __name__ == '__main__':
    print("Rendez-vous sur localhost:8051 pour finir le chargement des données (recharger la page si erreur)")
    print("....................................")
    app.run_server(debug=False, port=8051)