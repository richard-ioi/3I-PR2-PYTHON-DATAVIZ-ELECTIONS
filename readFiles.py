import pandas as pd

###### reading csv data files ############
#Data from the first round of the 2012 french presidential elections
d121 = pd.read_csv('data/resultats_communes_T1_2012.csv' ,error_bad_lines=False, sep=';', low_memory=False)
#Data from the first round of the 1995 french presidential elections (row 0 to 36671)
d951 = pd.read_csv('data/elections_1995_par_ville.csv', nrows=36671, low_memory=False)
d952 = pd.read_csv('data/elections_1995_par_ville.csv', skiprows=36671, low_memory=False)
#removes disruptive characters from column names of csv files, lowers all characters
def normaliseNames(name):
    return name.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')

def departmentQuery(code, name):
    return name.query("code_du_département == code")
