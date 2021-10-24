import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td
import calendar
import os.path


def generate_data(path):
    out = []
    for root, dir, files in os.walk(path):
        for file in files:
            print(f'importing: {file.split(".")[0]}...')
            df = pd.read_csv(os.path.join(root,file), sep=';', index_col=False, encoding='utf-8-sig', low_memory=False)
            out.append(df)
    df = pd.concat(out)
    return df

def training_filter(check):
    #listas de cursos
    arp   = ['C-ENS-ARP', 'C-ARP-ON']
    cht   = ['C-RVB-A', 'C-RVB-ON']
    cma   = ['RVL-CMA']
    cpiv  = ['C-PIV']
    crm   = ['C-CRMCORP']
    emg   = ['C-EMG-ON']
    emg_p = ['C-ENS-EMG']
    excr  = ['C-FIN', 'C-FEX', 'C-PEX', 'C-PIR-ON', 'C-PIV', 'C-PIV-ON']
    eqp   = ['C-737-ON', 'C-ENS-737', 'XQ-SIMU']
    ifr   = ['C-737-ON', 'C-ENS-737', 'XQ-SIMU']
    loft  = ['T-LOFT']
    rcl   = ['C-RCL', 'C-RCL-ON']
    sec   = ['C-ENS-SEC', 'C-SEC-ON']
    sgso  = ['C-SGSO', 'C-SGSO-ON']
    tem   = ['C-TEM']
    tce   = ['C-ENS-TCE']
    xq    = ['XQ-ROTA']
    
    
    if check == 'ARP':
        return arp
    elif check == 'CHT':
        return cht
    elif check == 'CMA':
        return cma
    elif check == 'CPIV':
        return cpiv
    elif check == 'CRM':
        return crm
    elif check == 'EMG':
        return emg
    elif check == 'EMG_presencial':
        return emg_p   
    elif check == 'EXCR':
        return excr
    elif check == 'EQP':
        return eqp
    elif check == 'IFR':
        return ifr
    elif check == 'LOFT':
        return loft
    elif check == 'RCL':
        return rcl
    elif check == 'SEC':
        return sec
    elif check == 'SGSO':
        return sgso
    elif check == 'TEM':
        return tem
    elif check == 'TCE':
        return tce
    elif check == 'XQ':
        return xq


def to_datetime(df, columns, dayfirst=False):
    for col in columns:
        df[col] = pd.to_datetime(df[col], dayfirst=dayfirst)

def clean_id(df, columns):
    @np.vectorize
    def __clean_id(id):
        id = id.strip()
        if id == '':
            return 'INVALID'
        for ch in id:
            if not ch.isdigit():
                return 'INVALID'
        return id.zfill(8)[-8:]

    for col in columns:
        df[col] = __clean_id(df[col].astype(str))
    

def clean_roster_activities(df):
    df = df.drop(df[~df['flt'].str.startswith('G3')].index)
    df['flt'] = df['flt'].str.replace('G3 ', '').str.strip()
    return df

@np.vectorize
def strip_email(email):
    return email.split('@')[0]