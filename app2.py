# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit localhost:8051/ in your web browser.

############ imports ###########
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import io
import json
from dash.dependencies import Input, Output
from urllib.request import urlopen
from readFiles import normaliseNames
from readFiles import departmentQuery
#pd.options.mode.chained_assignment = None  # default='warn'

#Department and region names
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

###### importing csv data files ############
url1995=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_1995_par_ville.csv").content

url2002T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T1.csv").content
url2002T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2002_T2.csv").content

url2007T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T1.csv").content
url2007T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2007_T2.csv").content

url2012T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T1.csv").content
url2012T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2012_T2.csv").content

url2017T1=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T1.csv").content
url2017T2=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T2.csv").content

urlChefLieux=requests.get("https://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/election_2017_T2.csv").content

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

d951 = d951.assign(year = "1995")
d021 = d021.assign(year = "2002")
d071 = d071.assign(year = "2007")
d121 = d121.assign(year = "2012")
d171 = d171.assign(year = "2017")


def trouve_chef_lieu(code):
    #vD=dChefLieux.query(f'code== "{code}"')
    #vD=dChefLieux.query(f'code == "60"')
    #return vD.loc['geom_x_y']
    return '49.4365523321,2.08616123661'

def calcul_taux_participation_departement(dYear):
    dT={}
    vCompteur=0
    for i in department_names.keys():
        vCompteur+=1
        vD=departmentQuery(i,dYear)
        moyenne=0
        vS=''
        for j in (vD['%_vot/ins']):
            vS=j
            vS=vS.replace(',','.')
            moyenne+=float(vS)

        moyenne=moyenne/vD['%_vot/ins'].size

        if (vCompteur<10):
            i='0'+i
        dT[i]=[moyenne]

    dTaux=pd.DataFrame.from_dict(dT,orient='index',columns=['taux_de_participation'])
    dTaux=dTaux.reset_index()
    dTaux=dTaux.rename(columns={'index':'code'})
    return dTaux
############# map drawing ##########
def draw_map(dYear,type,code='60'):
    print("Load de la map...")
    vLat=47.5
    vLon=2.6
    vZoom=4.4
    vCode="code"
    vColor='taux_de_participation'
    if(type=='départements'):
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            geojson = json.load(response)
            dTauxFinal=calcul_taux_participation_departement(dYear)
    elif(type=='communes'):
        #dt={}
        with urlopen('http://perso.esiee.fr/~fouquoir/E3/Python_Projet/data/communes/communes-'+code+'.geojson') as response:
            geojson = json.load(response)
            vCoordinates=trouve_chef_lieu(code)
            vLat=float(vCoordinates[:12])
            vLon=float(vCoordinates[14:])
            vZoom=7
            dTauxFinal=departmentQuery(code,dYear)
            #dTauxFinal.applymap(str)
            dTauxFinal['code_de_la_commune']=dTauxFinal['code_de_la_commune'].astype(str)
            dTauxFinal=dTauxFinal.rename(columns={'code_de_la_commune':'code'})
            dTauxFinal=dTauxFinal.reset_index()
            zeros=''
            vCompteur=0
            for j in (dTauxFinal['code']):
                if(len(str(j))==1):
                    zeros='00'
                elif(len(str(j))==2):
                    zeros='0'
                elif(len(str(j))==3):
                    zeros=''
                #j=int(code+zeros+str(j))
                dTauxFinal.loc[vCompteur,'code']=str(code+zeros+str(j))
                #print(j)
                vCompteur=vCompteur+1
            vColor='%_vot/ins'
            #dTauxFinal=dTauxFinal.astype(str)
            dTauxFinal.to_csv('test.csv')
        
    print("Traçage de la map...")
    global map
    map = px.choropleth_mapbox(dTauxFinal, geojson=geojson, color=vColor,
                        locations="code", featureidkey="properties.code",
                        center={"lat": vLat, "lon": vLon},
                        mapbox_style="carto-positron", zoom=vZoom
                    )
    map.update_geos(fitbounds="locations", visible=False)
    map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    width=800, height=400)
    map.show()
    print("Map finie")

#draw_map(d171,'départements')
draw_map(d171,'communes')

###### Moyenne des voix 2012###########
# joly = d121['%_voix/ins_joly']

# voixJoly = [voix for voix in joly]
# voixJoly = commaToDot(voixJoly)
# #voixJoly = stringToFloat(voixJoly)
# print(voixJoly[:15])
# floatJoly=[]
# for i in range (1, len(voixJoly)):
#     i = float(i)
#     floatJoly.append(i)
# moyenneJoly = mean(floatJoly)
# print(moyenneJoly)
year_name = {
    1995 : [d951, d952],
    2002 : [d021, d022],
    2007 : [d071, d072],
    2012 : [d121, d122],
    2017 : [d171, d172]
}
############## dash app ############
app = dash.Dash(__name__, title="Analyse des données d'élections")
app.layout = html.Div([
    html.H1(children='Elections présidentielles françaises de 1995 à 2017'),
  
    html.P(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div(
        children=[
            #dcc.Graph(figure=fig)
        ]
    ),
    html.Div(
        className='drop-down-year',
        children=[
            dcc.Dropdown(
                id='departements',
                options=[
                    {'label': str(i)+" - "+j, 'value': i} for i, j in department_names.items()
                ],
                placeholder="Départements"
            )
        ]
    ),
    html.Div(
        children=[
            dcc.Dropdown(
                id='round-select',
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
            dcc.Graph(figure=map), 
            html.Br(),
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
   Input('departements', 'value'),
   Input('year-slider', 'value'),
   Input('round-select', 'value'),
)
def update_figure(selected_departement, selected_year, selected_round): 
    global filtered_df
    draw_map(d171,'communes')
    for i,j  in year_name.items():
        if(i == selected_year[0]):
            if(selected_round == 'T1'):
                filtered_df = departmentQuery(selected_departement, j[0])
            elif(selected_round == 'T2'):
                filtered_df = departmentQuery(selected_departement, j[1])
            #map.update_layout(center={"lat": 47.5, "lon": 2.0}, zoom=7)

    fig = px.scatter(filtered_df, x='inscrits', y='votants', hover_name="libellé_de_la_commune", height=300, title="Votants en fonction des inscrits dans le "+str(selected_departement)+" en "+str(selected_year[0]))
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="LightSteelBlue",
    )

    return fig

if __name__ == '__main__':
    print("Chargement des données...")
    print("Rendez-vous sur localhost:8051 pour finir le chargement des données (recharger la page si erreur)")
    app.run_server(debug=True, port=8051)