import pandas as pd
import pygal

#removes disruptive characters from column names of csv files, lowers all characters
def normaliseNames(name):
    return name.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
#enables string to float convertion
def commaToDot(name):
    convert = []
    for comma in name:
        temp = comma.replace(',', '.')
        convert.append(temp)   
    return convert

#selects a specific department 
def departmentQuery(code, name):
    return name.query(createQueryString(code))
#creates a string for queries
def createQueryString(code):
    return f'code_du_département == "{code}"'

    
    