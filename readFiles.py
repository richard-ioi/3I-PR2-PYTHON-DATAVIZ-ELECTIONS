import pandas as pd


#removes disruptive characters from column names of csv files, lowers all characters
def normaliseNames(name):
    return name.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
#selects a specific department 
def departmentQuery(code, name):
    return name.query("code_du_département == '93'")
