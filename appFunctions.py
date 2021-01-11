def normaliseNames(name):
    """ In column header names : replaces spaces by _ , lowers all the characters and removes any disruptive characters 

    Parameters:
    name (string): the name of the dataframe 

    Returns:
    object:Modified dataframe 

   """
    return name.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_').str.replace('.', '_')

def commaToDot(data):
    """ Replaces commas by dots to enable string to float conversions. Use only on columns holding numbers and not letters
    
    Parameters:
    data(string): the list holding data from a dataframe column

    Returns:
    float:List holding the data converted to float
    """
    convert = []
    for comma in data:
        temp = comma.replace(',', '.')
        convert.append(temp)   
    return convert

#selects a specific department 
def departmentQuery(code, name):
    """Queries dataframe to create a sub-frame depending on the selected departement

    Parameters:
    code(string): the code of the required departement, a number between 1 ad 95
    name(object): dataframe to be queried 

    Returns:
    object: sub-frame holding data from the selected departement
    """
    return name.query(f'code_du_département == "{code}"')

def candidateData(data_frame, name):
    """Gathers all the columns relating to the chosen candidate
    """
    return data_frame.columns.replace('.', name)
