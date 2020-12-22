import dash_core_components as dcc

def createDepartment():
    dcc.Dropdown(
        options=[
            {'label': '1995', 'value': '1995'},
            {'label': '2002', 'value': '2002'},
            {'label': '2007', 'value': '2007'},
            {'label':'2012', 'value':'2012'},
            {'label':'2017', 'value':'2017'}
        ],
        placeholder="Sélectionnez une année"),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )