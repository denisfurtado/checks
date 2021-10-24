import pandas as pd
from datetime import datetime as dt
from util.progress import step

@step('netline: generating netline import file')
def to_import_file(df):
    origin = df
    df = df.copy()
    df = df.reset_index().rename({'index': 'cif'}, axis=1)
    df = df.drop(df[df['rex_90'] < pd.Timestamp.now()].index)
    df = df.drop(df[df['rex_90']==df['nl']].index)
    df['__issue'] = pd.to_datetime(dt.today()).floor('D')
    
    for c in df.columns:
        if df[c].dtype == 'datetime64[ns]':
            df[c] = df[c].astype(str)
    
    # fill table
    df['update'] = 'U'
    df['id'] = df['cif'].astype(str).str.zfill(8)
    df['type'] = 'REX'
    df['issue'] = df.__issue.str.replace('-', '') + '0000'
    df['rex_90'] = df['rex_90'].str.replace('-', '')  + '0000'
    df['ext'] = df['rex_90'].str.replace('-', '')
    df['failed'] = 'N'
    df['do_not_plan_before'] = df['rex_90'].str.replace('-', '')
    df['zero'] = '0'
    df['remark'] = ''
    df['check_comment'] = ''
    df['confirmed'] = 'Y'
    df['paper_recieved'] = 'Y'

    # remove fields from original file
    cols = [
        'update',
        'cif',
        'type',
        'issue',
        'rex_90',
        'ext',
        'failed',
        'do_not_plan_before',
        'zero',
        'remark',
        'check_comment',
        'confirmed',
        'paper_recieved'  
    ]
    df = df[cols].copy()
    df.to_csv('./data/output/crm_import.dat', sep='|', header=None, index=False)