def normalise_names(name):
    """ In column header names : replaces spaces by _ , lowers all the characters and removes any disruptive characters 

    Parameters:
    name (string): the name of the dataframe 

    Returns:
    dataframe:Modified dataframe 

   """
    return name.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_').str.replace('.', '')

def comma_to_dot(data):
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

def department_query(code, name):
    """Queries dataframe to create a sub-frame depending on the selected departement

    Parameters:
    code(string): the code of the required departement, a number between 1 ad 95
    name(dataframe): dataframe to be queried 

    Returns:
    dataframe: sub-frame holding data from the selected departement
    """
    return name.query(f'code_du_département == "{code}"')

def add_zeros_ewt(df, code):
    """Adds zeros to town codes in order to have a standard length."""
    zeros=''
    vCompteurCode=0
    for i in df['code']:
        if(len(str(i))==1):
            zeros='00'
        elif(len(str(i))==2):
            zeros='0'
        elif(len(str(i))==3):
            zeros=''
        df.loc[vCompteurCode,'code']=str(code+zeros+str(i))
        vCompteurCode=vCompteurCode+1

def reformat_department(department_code):
    if(len(department_code)<2):
        department_code = '0'+str(department_code)
    return department_code