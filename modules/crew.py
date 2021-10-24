import pandas as pd
from util import funcs
from util.progress import step

map_columns = {
    'nome_guerra': 'name',
    'funcao': 'rank'
}

@step('crew: loading crew data')
def get_flight_crew():  
    df = pd.read_csv('./data/crew/crew.csv', sep=';')
    df = df.rename(map_columns, axis=1)
    df = df.drop(df[~df['rank'].isin(['CMT', 'COP'])].index)
    df['email'] = funcs.strip_email(df['email'])
    funcs.clean_id(df, ['cif'])
    return df

