# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8051/ in your web browser.

""" imports """
import dash
import dash_core_components as dcc
import dash_html_components as html
from numpy.lib.function_base import kaiser
import plotly.express as px
import pandas as pd
import requests
import io
import json
import numpy
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from urllib.request import urlopen
from appFunctions import normaliseNames
from appFunctions import departmentQuery
from appFunctions import commaToDot

""" Dictionnary with department codes as keys and names as values """
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

""" Dictionnary with department names as keys and department code arrays as values"""
region_names = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Guadeloupe': ['971'],
    'Guyane': ['973'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'La Réunion': ['974'],
    'Martinique': ['972'],
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
}

"""importing csv data files """
url1995=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_1995_par_ville.csv").content

url2002T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T1.csv").content
url2002T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T2.csv").content

url2007T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T1.csv").content
url2007T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T2.csv").content

url2012T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T1.csv").content
url2012T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T2.csv").content

url2017T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T1.csv").content
url2017T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T2.csv").content

urlChefLieux=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/code_cheflieux.csv").content

#read_1995=pd.read_excel (r'https://www.data.gouv.fr/fr/datasets/r/e44ed516-cd60-4c42-bb18-5a791c7431ec')
#read_1995.to_csv(r'data/1995.csv',index=None,header=True)
###### reading csv data files ############
#Data from the first and second rounds of the 1995 french presidential elections (round 1 : row 0 to 36671, round 2 : row X to Y)
d951 = pd.read_csv(io.StringIO(url1995.decode('utf-8')), nrows=36671, low_memory=False)
d952 = pd.read_csv(io.StringIO(url1995.decode('utf-8')), skiprows=36671, low_memory=False)
#d951 = pd.read_csv('data/1995.csv', nrows=36671, low_memory=False)
#d952 = pd.read_csv('data/1995.csv', skiprows=36671, low_memory=False)

#Data from the first and second rounds of the 2002 french presidential elections 
d021 = pd.read_csv(io.StringIO(url2002T1.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
d022 = pd.read_csv(io.StringIO(url2002T2.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first and second rounds of the 2007 french presidential elections 
d071 = pd.read_csv(io.StringIO(url2007T1.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
d072 = pd.read_csv(io.StringIO(url2007T2.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first round of the 2012 french presidential elections
d121 = pd.read_csv(io.StringIO(url2012T1.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
d122 = pd.read_csv(io.StringIO(url2012T2.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first and second rounds of the 2017 french presidential elections 
d171 = pd.read_csv(io.StringIO(url2017T1.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
d172 = pd.read_csv(io.StringIO(url2017T2.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)

dChefLieux = pd.read_csv(io.StringIO(urlChefLieux.decode('utf-8')) ,error_bad_lines=False, sep=';', low_memory=False)
#dChefLieux.to_csv(r'data/chefLieux.csv',index=None,header=True)
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
"""Dictionnary with years as keys and an array of the associated dataframes as values"""
year_name = {
    1995 : [d951, d952],
    2002 : [d021, d022],
    2007 : [d071, d072],
    2012 : [d121, d122],
    2017 : [d171, d172]
}
year_can = {
    1995 : [d951, d952],
    2002 : [d021, d022],
    2007 : [d071, d072],
    2012 : [d121, d122]
}
"""Dictonnary with order in csv as keys and names of candidates as values for 1995"""
candidats_1995 = {'':'Philippe de Villier',
            '1' : 'Jean-Marie Lepen',
            '2' : 'Jacques Chirac',
            '3' : 'Arlette Laguiller',
            '4' : 'Jacques Cheminade',
            '5' : 'Lionel Jospin',
            '6' : 'Dominique Voynet',
            '7' : 'Edourd Balladur',
            '8' : 'Robert Hue'
}
"""Dictonnary with order in csv as keys and names of candidates as values for 2002"""
candidats_2002 = { '' : 'Bruno Megret',
                    '1' : 'Corrine Lepage',
                    '2' : 'Daniel Gluckstein',
                    '3' : 'François Bayrou',
                    '4' : 'Jacques Chirac',
                    '5' : 'Jean-Marie Lepen',
                    '6' : 'Christiane Taubira',
                    '7' : 'Jean Saint-Josse',
                    '8' : 'Noel Mamere',
                    '9' : 'Lionel Jospin',
                    '10' : 'Christine Boutin',
                    '11' : 'Robert Hue',
                    '12' : 'Jean-Pierre Chevenement',
                    '13' : 'Alain Madelin',
                    '14' : 'Arlette Laguiller',
                    '15' : 'Olivier Besancenot'
}
"""Dictonnary with order in csv as keys and names of candidates as values for 2007"""
candidats_2007 = {'' : 'Olivier Besancenot',
                '1' : 'Marie-George Buffet',
                '2' : 'Gérard Schivardi',
                '3' : 'François Bayrou',
                '4' : 'José Bové',
                '5' : 'Dominique Voynet',
                '7' : 'Phillipe de Villiers',
                '8' : 'Ségolène Royal',
                '9' : 'Frédéric Nihous',
                '10' : 'Jean-Marie Lepen',
                '11' : 'Arlette Laguiller',
                '12' : 'Nicolas Sarkozy'
}
"""Dictonnary with order in csv as keys and names of candidates as values for 2012"""
candidats_2012 = {'' : 'Eva Joly',
                '1' : 'Marine Lepen',
                '2' : 'Nicolas Sarkozy',
                '3' : 'Jean-Luc Mélanchon',
                '4' : 'Philippe Poutou',
                '5' : 'Nathalie Arthaud',
                '6' : 'Jacques Cheminade',
                '7' : 'François Bayrou',
                '8' :'Nicolas Dupont-Aignan',
                '9' : 'François Hollande'
}
"""Dictonnary with order in csv as keys and names of candidates as values for 2017"""

def candidat_dep(df, dep, candidats):
    """Calculates the mean of the vote for each candidate, in each department

    Parameters:
    df(object) : the dataframe corresponding to the election we're intrested in
    dep(int) : the department 
    candidats(dict) : the dictionnary holding the list of candidates in the chosen data frame. ATTENTION you need 
                        to manually make sure you're using the correct associations (e.g. d951 -> candidats_1995)
    
    Returns:
    (dict) Dictionnary with names of candidates as Keys and their department means as values
    """
    d_dep = departmentQuery(dep,df)
    moyenne = {}
    moyenneVote = 0
    for j, k in candidats.items():
        votes = [voix for voix in d_dep['voix'+j]]
        floatVote=[]
        for i in range (1, len(votes)):
            floatVote.append(float(votes[i]))
            moyenneVote = numpy.mean(floatVote)
        moyenne[k] = moyenneVote
   
    return moyenne 
def mean_dataframe(candidats, selected_year):
    """Create the dataframe holding all the candidates and their means for a specific year. The columns are : 
        'year, departement, candidat, moyenne'.
        TODO add 2017, merge all the years together

    Parameters:
    candidats(dict)
    selected_year(string)

    Returns:
    Dataframe

    """
    rows = []
    candidats=candidats_1995
    for key, value in year_can.items():
        for dep in range (1,96):
            ave = candidat_dep(value[0], dep, candidats)
            for i,j  in ave.items():
                rows.append(['1995', dep, i, j])    
    mean = pd.DataFrame(rows, columns=[selected_year, "departement", "candidat", "moyenne"])

    return mean

def trouve_chef_lieu(code):
    """Queries dChefLieux to create a sub-frame depending on the selected departement

    Parameters:
    code(string): the code of the required departement, a number between 1 ad 95

    Returns:
    object: sub-frame holding data from the selected departement
    """
    return dChefLieux.query(f'code== "{code}"')['geom_x_y'].iloc[0]

def calcul_taux_participation_departement(dYear):
    dT={}
    dDepartmentList=[]
    for i in department_names.keys():
        dDepartmentList.append(department_names.get(i))
        vD=departmentQuery(i,dYear)
        moyenne=0
        for j in (vD['%_vot/ins']):
            vS=j
            vS=vS.replace(',','.')
            moyenne+=float(vS)
        if (len(i)==1):
            i='0'+i

        dT[i]=[moyenne/vD['%_vot/ins'].size]

    dTaux=pd.DataFrame.from_dict(dT,orient='index',columns=['taux_de_participation'])
    dTaux=dTaux.reset_index()
    dTaux=dTaux.rename(columns={'index':'code'})
    dDepartmentSeries=pd.Series(dDepartmentList,name='dep_names')
    dTaux=pd.concat([dTaux,dDepartmentSeries], axis=1)
    return dTaux

def calcul_taux_participation_commune(dYear,code):
    dep=code
    if(code[0]=='0'):
        dep=code[1]
    print("DEPARTEMENT SELECTIONNE "+dep)
    dTaux=departmentQuery(dep,dYear)
    dTaux=dTaux.rename(columns={'code_de_la_commune':'code'})
    dTaux=dTaux.reset_index()#SI ERREUR PEUT ETRE ICI !!!!!
    zeros=''
    vCompteur=0
    for j in (dTaux['code']):
        if(len(str(j))==1):
            zeros='00'
        elif(len(str(j))==2):
            zeros='0'
        elif(len(str(j))==3):
            zeros=''
        dTaux.loc[vCompteur,'code']=str(code+zeros+str(j))
        dTaux.loc[vCompteur,'%_vot/ins']=float(dTaux.loc[vCompteur,'%_vot/ins'].replace(',','.'))
        vCompteur=vCompteur+1
    dTaux['code']=dTaux['code'].astype(str)
    dTaux['%_vot/ins']=dTaux['%_vot/ins'].astype(float)
    return dTaux

def candidat_gagnant_commune(dYear,code):
    dT={}
    dMax=[]
    dep=code
    if(code[0]=='0'):
        dep=code[1]
    zeros=''
    dCand=departmentQuery(dep,dYear)
    dCand=dCand.rename(columns={'code_de_la_commune':'code'})
    dCand['code']=dCand['code'].astype(str)
    dCand=dCand.reset_index()
    vCompteurCode=0
    for i in dCand['code']:
        if(len(str(i))==1):
            zeros='00'
        elif(len(str(i))==2):
            zeros='0'
        elif(len(str(i))==3):
            zeros=''
        dCand.loc[vCompteurCode,'code']=str(code+zeros+str(i))
        vCompteurCode=vCompteurCode+1
    vCompt=0
    dVille=[]
    for x in dCand['code']:
        vC=''
        vCint=0
        max=0
        gagnant=''
        while('%_voix/exp'+vC in dCand):
            if(float((str(dCand.loc[vCompt]['%_voix/exp'+str(vC)])).replace(',','.'))>max):
                max=float((dCand.loc[vCompt]['%_voix/exp'+str(vC)]).replace(',','.'))
                gagnant=str(dCand.loc[vCompt]['nom'+str(vC)])+' '+str(dCand.loc[vCompt]['prénom'+str(vC)])
            vCint=vCint+1
            vC=str(vCint)
        dT[x]=gagnant
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

def candidat_gagnant_departement(dYear):
    dT={}
    dDepartmentList=[]
    for i in department_names.keys():
        dDepartmentList.append(department_names.get(i))
        vD=candidat_gagnant_commune(dYear,i)
        dCandidats={}
        for j in vD['gagnant']:
            if(j not in dCandidats):
                dCandidats[j]=1
            else:
                dCandidats[j]=dCandidats[j]+1
        max=0
        gagnant=''
        for k in dCandidats.keys():
            if(int(dCandidats.get(k))>max):
                max=int(dCandidats.get(k))
                gagnant=k
        if (len(i)==1):
            i='0'+i
        dT[i]=gagnant

    dFinal=pd.DataFrame.from_dict(dT,orient='index',columns=['gagnant'])
    dFinal=dFinal.reset_index()
    dFinal=dFinal.rename(columns={'index':'code'})
    dDepartmentSeries=pd.Series(dDepartmentList,name='dep_names')
    dFinal=pd.concat([dFinal,dDepartmentSeries], axis=1)
    return dFinal

############# map drawing ##########
def draw_map(dYear,type,code='60',format='participation'):
    print("Load de la map...")
    if(type=='départements'):
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            geojson = json.load(response)
        vLat=47.5
        vLon=2.6
        vZoom=4.4
    elif(type=='communes'):
        with urlopen('http://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/communes/communes-'+code+'.geojson') as response:
            geojson = json.load(response)
        vCoordinates=trouve_chef_lieu(code)
        vLat=float(vCoordinates[:12])
        vLon=float(vCoordinates[14:])
        vZoom=7

    if(format=='participation'):
        if(type=='départements'):
            vColor='taux_de_participation'
            dTauxFinal=calcul_taux_participation_departement(dYear)
            vHoverLoc='dep_names'
        elif(type=='communes'):
            vColor='%_vot/ins'
            dTauxFinal=calcul_taux_participation_commune(dYear,code)
            vHoverLoc='libellé_de_la_commune'

    elif(format=='candidat'):
        if(type=='départements'):
            dTauxFinal=candidat_gagnant_departement(dYear)
            vColor='gagnant'
            vHoverLoc='dep_names'
        elif(type=='communes'):
            dTauxFinal=candidat_gagnant_commune(dYear,code)
            vColor='gagnant'
            vHoverLoc='libellé_de_la_commune'
    
    print("Traçage de la map...")
    global map
    map = px.choropleth_mapbox(dTauxFinal, geojson=geojson, color=vColor,
                        locations="code", featureidkey="properties.code",
                        center={"lat": vLat, "lon": vLon},
                        mapbox_style="carto-positron", zoom=vZoom,
                        hover_data={vHoverLoc}
                    )
    map.update_geos(fitbounds="locations", visible=False)
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    width=800, height=400)
    #map.show()
    print("Map finie")
#draw_map(d171,'départements','60',format='candidat')

c1995 = mean_dataframe(candidats_1995, '1995')
c2002 = mean_dataframe(candidats_2002, '2002')
c2007 = mean_dataframe(candidats_2007, '2007')
c2012 = mean_dataframe(candidats_2012, '2012')

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
                    Grâce aux divers menus, vous pourez mettre en évidence les disparités 
                    des votes à échelle nationale ou départementale au cours des 5 dernières élections.
                ''')
            ]
    ),
    
    html.Div(className='inline-graph',
                children=[
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id='departements',
                                options=[
                                    {'label': str(i)+" - "+j, 'value': i} for i, j in department_names.items()
                                ],
                                placeholder="Départements",
                                value='1',
                                clearable=False
                            ),
                            dcc.Dropdown(
                                id='round-select',
                                options=[
                                    {'label': 'Premier tour', 'value': 'T1'},
                                    {'label': 'Second tour', 'value': 'T2'}
                                ],
                                value="T1",
                                clearable=False
                            ),
                            html.P(children='''
                                    Echelle
                            '''),
                            dcc.RadioItems(
                                id="map-scale",
                                options=[
                                    {'label': 'Nationale', 'value': 'fr'},
                                    {'label': 'Départementale', 'value': 'dep'}
                                ],
                                value='fr'
                            ),
                            dcc.RadioItems(
                                id="map-format",
                                options=[
                                    {'label': 'Taux de participation', 'value': 'participation'},
                                    {'label': 'Candidats', 'value': 'candidat'}
                                ],
                                value='participation'
                            )  ,
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
                    ),
            
            html.Div([
                dcc.Graph(id='map-box')
            ]),
            html.Div([
                dcc.Graph(id='test-graph'),
                dcc.Graph(id='histogram')
            ])  
        ]
    )
])
@app.callback(
   Output('test-graph', 'figure'),
   Input('departements', 'value'),
   Input('year-slider', 'value'),
   Input('round-select', 'value'),
)
def update_figure(selected_departement, selected_year, selected_round): 
    global filtered_df
    for i,j  in year_name.items():
        if(i == selected_year[0]):
            if(selected_round == 'T1'):
                filtered_df = departmentQuery(selected_departement, j[0])
            elif(selected_round == 'T2'):
                filtered_df = departmentQuery(selected_departement, j[1])

    fig1 = px.scatter(filtered_df, x='inscrits', y='votants', hover_name="libellé_de_la_commune", height=300, title="Votants en fonction des inscrits dans le "+str(selected_departement)+" en "+str(selected_year[0]))
    fig1.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=200,
        paper_bgcolor="LightSteelBlue",
    )
    return fig1
@app.callback(
    Output('histogram', 'figure'),
    Input('departements', 'value'),
    Input('round-select', 'value')
)
def update_historgram(selected_departement, selected_round):
    """Renders a histogram showing the participation rate over the past 5 elections
    Parameters:
    selected_departement(string): the value of the department selected from the 'departements' dropdown menu
    selected_round(string): the value of the round selected from the 'round-select' dropdown menu

    Returns:
    Figure containing 5 overlaid histograms, 4 of which are masked upon launching the app
    """
    global x0, x1, x2, x3, x4
    #for i,j  in year_name.items():
    if(selected_round == 'T1'):
            x0 = departmentQuery(selected_departement, d951)
            x1 = departmentQuery(selected_departement, d021)
            x2 = departmentQuery(selected_departement, d071)
            x3 = departmentQuery(selected_departement, d121)
            x4 = departmentQuery(selected_departement, d171)
    elif(selected_round == 'T2'):
            x0 = departmentQuery(selected_departement, d952)
            x1 = departmentQuery(selected_departement, d022)
            x2 = departmentQuery(selected_departement, d072)
            x3 = departmentQuery(selected_departement, d122)
            x4 = departmentQuery(selected_departement, d172)    

    fig= go.Figure()
    fig.add_trace(go.Histogram(name='1995', x = commaToDot(x0['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2002', visible='legendonly', x = commaToDot(x1['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2007', visible='legendonly', x = commaToDot(x2['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2012', visible='legendonly', x = commaToDot(x3['%_vot/ins'])))
    fig.add_trace(go.Histogram(name='2017', visible='legendonly', x = commaToDot(x4['%_vot/ins'])))
    fig.update_layout(barmode='overlay',
                        title={
                            'text': "Taux de participation dans le "+str(selected_departement)+" entre 1995 et 2017",
                            'y':0.85,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01))
    fig.update_traces(opacity=0.50)
    return fig

@app.callback(
    Output('map-box', 'figure'),
    Input('year-slider', 'value'),
    Input('round-select', 'value'),
    Input('map-scale', 'value'),
    Input('map-format', 'value'),
    Input('departements', 'value')
)
def update_map(selected_year, selected_round, selected_scale, selected_format, selected_departement):
    """ Renders the map of France showing the participation rate of each department or town depending on the chosen scale

    Parameters:
    selected_year(): 
    selected_round()
    selected_scale()
    selected_format()
    selected_departement()

    Returns 
    Figure holding the Choropleth map of France
    """
    global map
    global geo
    ########### REPRESENTATION ECHELLE NATIONALE ######################
    if(selected_scale =='fr'):
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            geo = json.load(response)
            vLat=47.5
            vLon=2.6
            vZoom=4.4
    ############# REPRESNETATION DEPARTEMENTALE ############################    
    elif(selected_scale =='dep'):
        depart = selected_departement
        for i in range(1, 10):
            if(depart == str(i)):
                depart = '0'+str(i)
                print("le dep selec est mtn :" + str(depart))
        with urlopen('http://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/communes/communes-'+depart+'.geojson') as response:
            geo = json.load(response)
            vCoordinates=trouve_chef_lieu(depart)
            print(depart)
            vLat=float(vCoordinates[:12])
            vLon=float(vCoordinates[14:])
            vZoom=7
    if(selected_format=='participation'):
        if(selected_scale=='fr'):
            vColor='taux_de_participation'
            vHoverLoc='dep_names'
            for i,j  in year_name.items():
                if(i == selected_year[0]):
                    if(selected_round == 'T1'):
                        dTauxFinal=calcul_taux_participation_departement(j[0])
                    elif(selected_round == 'T2'):
                        dTauxFinal=calcul_taux_participation_departement(j[1])
        elif(selected_scale=='dep'):
            vColor='%_vot/ins'
            vHoverLoc='libellé_de_la_commune'
            for i,j  in year_name.items():
                if(i == selected_year[0]):
                    if(selected_round == 'T1'):
                        dTauxFinal=calcul_taux_participation_commune(j[0],selected_departement)
                    elif(selected_round == 'T2'):
                        dTauxFinal=calcul_taux_participation_commune(j[1], selected_departement)

    elif(selected_format=='candidat'):
        if(selected_scale=='fr'):
            for i,j  in year_name.items():
                if(i == selected_year[0]):
                    if(selected_round == 'T1'):
                        dTauxFinal=candidat_gagnant_departement(j[0])
                    elif(selected_round == 'T2'):
                        dTauxFinal=candidat_gagnant_departement(j[1])
            vColor='gagnant'
            vHoverLoc='dep_names'
        elif(selected_scale=='dep'):
            for i,j  in year_name.items():
                if(i == selected_year[0]):
                    if(selected_round == 'T1'):
                        dTauxFinal=candidat_gagnant_commune(j[0],selected_departement)
                    elif(selected_round == 'T2'):
                        dTauxFinal=candidat_gagnant_departement(j[1],selected_departement)
            vColor='gagnant'
            vHoverLoc='libellé_de_la_commune'

    ################ TRACAGE DE LA MAP ###########################
    map = px.choropleth_mapbox(dTauxFinal, geojson=geo, color=vColor,
                        locations="code", featureidkey="properties.code",
                        center={"lat": vLat, "lon": vLon},
                        mapbox_style="carto-positron", zoom=vZoom, 
                        color_discrete_sequence=px.colors.diverging.Earth,
                        hover_data={vHoverLoc}
                    )
    map.update_geos(fitbounds="locations", visible=False)
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    width=600, height=700)
    #map.show()
    return map

if __name__ == '__main__':
    print("Chargement des données...")
    print("Rendez-vous sur localhost:8051 pour finir le chargement des données (recharger la page si erreur)")
    print("..**.")
    app.run_server(debug=True, port=8051)