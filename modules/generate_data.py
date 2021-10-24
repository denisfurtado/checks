from gol_apis import RosterActivitiesService
from gol_apis import RosterTagService
from gol_apis import CheckScheduleService
from gol_apis import CrewMemberInfoService
import api_tools
from api_tools.setup import setup_crew_info_dataframe
from api_tools.setup import setup_checks_dataframe
from api_tools.setup import setup_tag_dataframe
from api_tools.setup import setup_activities_dataframe

from gol_logger import Logger
import pandas as pd
import multiprocessing as mp
import requests, time
from datetime import datetime as dt
from datetime import timedelta as td
from utils import funcs
from utils.progress import step
from utils.progress import BAR
from itertools import chain

import sys
from config.variables import user

@step('check schedule: loading checks schedule data')
def get_checks(user, log_info=False, active=True):
    logger = Logger()
    logger.print_setting['INFO'] = log_info
    
    # start a query service
    cs = CheckScheduleService(user=user['name'], logger=logger)
    cs.authenticate(password=user['password'])

    # run query and create a checks dataframe   
    data = cs.run_query(active=active)
    df = setup_checks_dataframe(data)
    
    #save to cache
    df.to_csv('./data/checks/check_schedule.csv', index=False, encoding='utf-8-sig', sep=';')

    return df


@step('crew info: loading crew info data')
def get_crew_info(user, log_info=False, date=dt.now()):
    logger = Logger()
    logger.print_setting['INFO'] = log_info
    
    # start a query service
    ci = CrewMemberInfoService(user=user['name'], logger=logger)
    ci.authenticate(password=user['password'])

    # run query and create a checks dataframe   
    data = ci.run_query(date=date)
    df = setup_crew_info_dataframe(data)
    
    #save to cache
    df.to_csv('./data/crew/crew_info.csv', index=False, encoding='utf-8-sig', sep=';')

    return df


@step('roster tag: loading roster tag data')
def get_roster_tag(user, log_info=False, period=dt.now(), tag_type='', all_period=False):
    logger = Logger()
    logger.print_setting['INFO'] = log_info
    
    # start a query service
    rt = RosterTagService(user=user['name'], logger=logger)
    rt.authenticate(password=user['password'])
    
    y = int(period.year)
    m = int(period.month)
    
    if all_period:
        for month in range(1, m+1):
            begin = dt(y, month, 1, 3) + pd.offsets.MonthBegin(0)
            end = dt(y, month, 1, 2, 59) + pd.offsets.MonthBegin(1)
            
            BAR.do_step(f'roster tag: loading data: chunck {y}-{str(month).zfill(2)}')
            data = rt.run_query(begin=begin, end=end, tagType=tag_type)
            df = setup_tag_dataframe(data)
            
            df.to_csv(f'./data/roster_tags/{y}-{str(month).zfill(2)}.csv', index=False, encoding='utf-8-sig', sep=';')
        
    
    # set query parameters
    begin = dt(y, m, 1, 3) + pd.offsets.MonthBegin(0)
    end = dt(y, m, 1, 2, 59) + pd.offsets.MonthBegin(1)
    
    # run query and create a checks dataframe   
    data = rt.run_query(begin=begin, end=end, tagType=tag_type)
    df = setup_tag_dataframe(data)
    
    #save to cache
    df.to_csv(f'./data/roster_tags/{y}-{str(m).zfill(2)}.csv', index=False, encoding='utf-8-sig', sep=';')

    return df


@step('rosters: loading rosters activities data')
def get_rosters(user, log_info=False, period=dt.now(), all_period=False):
    logger = Logger()
    logger.print_setting['INFO'] = log_info
    
    # start a query service
    ra = RosterActivitiesService(user=user['name'], logger=logger)
    ra.authenticate(password=user['password'])
    
    y = int(period.year)
    m = int(period.month)
    
    if all_period:
        for month in range(1, m+1):
            begin = dt(y, month, 1, 3) + pd.offsets.MonthBegin(0)
            end = dt(y, month, 1, 2, 59) + pd.offsets.MonthBegin(1)
            
            BAR.do_step(f'rosters activities: loading data: chunck {y}-{str(month).zfill(2)}')
            data = ra.run_query(begin=begin, end=end)
            df = setup_activities_dataframe(data)
            
            df.to_csv(f'./data/rosters/{y}-{str(month).zfill(2)}.csv', index=False, encoding='utf-8-sig', sep=';')
        
    
    # set query parameters
    begin = dt(y, m, 1, 3) + pd.offsets.MonthBegin(0)
    end = dt(y, m, 1, 2, 59) + pd.offsets.MonthBegin(1)
    
    # run query and create a checks dataframe
    BAR.do_step(f'rosters activities: loading data: chunck {y}-{str(m).zfill(2)}')
    data = ra.run_query(begin=begin, end=end)
    df = setup_activities_dataframe(data)
    
    #save to cache
    df.to_csv(f'./data/rosters/{y}-{str(m).zfill(2)}.csv', index=False, encoding='utf-8-sig', sep=';')

    return df

@step('neolude: loading neolude data')
def get_data_neolude(user, log_info=False, training_id=''):
    logger = Logger()
    logger.print_setting['INFO'] = log_info
    
    TRAININGS = {
        14140 : 'ARP',
        6071  : 'Artigos Perigosos - Categoria 10 Inicial',
        6167  : 'CFI',
        6063  : 'CFI Inicial',
        16766 : 'EQP',
        18180 : 'EMG',
        25250 : 'EMG_presencial',
        14241 : 'SGSO TRIPULANTES',
        17877 : 'OPT',
        11211 : 'RBAC',
        26361 : 'aproximacoes_estabilizadas_e_nao_estabilizadas',
        19897 : 'experiencia_recente',
        6069  : 'CRM',
        6162  : 'TEM',
        6066  : 'SEC_inicial',
        14951 : 'ARP_tripulacao_comercial',
        14547 : 'PERIODICO II - REVALIDAÇÃO - RVB - MÓDULO EAD',
        25352 : 'PERIODICO II - REVALIDACAO - RVB - MÓDULO PRÁTICO',
        14646 : 'PERIODICO I - RECICLAGEM - RCL - MÓDULO EAD',
        26463 : 'PERIODICO I - RECICLAGEM - RCL - MÓDULO PRÁTICO',
        14951 : 'DGR - CHAVE 11 - PERIODICO - EAD',
        27775 : 'DGR - CHAVE 11 - INICIAL (Artigos Perigosos - chave 11 - Inicial)',
        20301 : 'CPEX - Curso Periódico de Examinador - EAD',
        20907 : 'CPIR - Curso Periodico de Instrutor de Voo - EAD',
        31310 : 'Treinamento Anticorrupção V. 2021',
        2425  : 'O Terrorismo na Aviação Civil',
        6066  : 'AVSEC PARA TRIPULANTES - FORMAÇÃO RBAC 110',
        6173  : 'AVSEC PARA TRIPULANTES - ATUALIZAÇÃO RBAC 110'

    }
    
    training = TRAININGS.get(training_id)
    
    login_url = 'http://portaldoconhecimentogol-account.neolude.com.br/Account/Login'
    
    return_url = 'https://portaldoconhecimentogol-account.neolude.com.br'
    show_captcha = 'false'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'}

    payload = {'Login': user['name'],
               'Password': user['password'],
               'ReturnUrl': return_url,
               'ShowCaptcha':show_captcha}
    
    with requests.Session() as session:
        BAR.do_step(f'neolude data: loading data: chunck {training}')
        response = session.post(login_url, data=payload, headers=headers)
        time.sleep(10)
        
        url = f"https://portaldoconhecimentogol.neolude.com.br/api/reports/course/itemizedClass/?pageIndex=1&pageSize=25000&sortBy=UserName&order=desc&startDate=&endDate=&courseModeID=&courseIDs={training_id}&occupationAreaIDs=&withChildNodes=true&userIDs=&courseUserStatusIdentifiers=&showSingleUsers=true&onlyActiveUsers=false&categoryIDs=&TrackIDs=&tagIDs=&startAdmissionDate=&endAdmissionDate=&EnrollableIDs=&Login=&rootBusinessUnitID=&businessUnitID=&hotData=true&coursePermissionLevelIdentifier=&startConclusionDate=&endConclusionDate="
        r = session.get(url=url)
        
        data = r.json()
        
        df = data['Results']
        df = pd.DataFrame(df)
        df.to_csv(f'./data/neolude/{training}.csv', index=False, encoding='utf-8-sig', sep=';') 

    return df
