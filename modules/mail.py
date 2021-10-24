import pandas as pd
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

    
def checks_html(df):
    
    df = df.copy()

    # keep only records that day offs are not ok
    df = df[df.atualizar==False]
    if df.shape[0] < 1:
        return ''

    df = df[['cif',
             'guerra',
             'funcao',
             'base',
             'checkTypeCode',
             'expiryDt', 
             'status', 
             'nota', 
             'data_conclusao',
             'code',
             'dep',
             'tempo_de_conclusao (dias)',
             'atualizar']]

    # set style
    df.to_csv('debug.csv', sep=';')
    data = df.to_dict('records')

    # load template
    with open('./templates/checks.html', 'r', encoding='utf-8') as file:
        template = file.readlines() 

    mail_template = Template(''.join(template))

    html = mail_template.render({
        'data': data
    })

    return html


def send_checks_mail(df, user, password, emails):
    # config server
    server = smtplib.SMTP('smtp.office365.com',587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.SentOnBehalfOfName = 'mensagensescala@voegol.com.br'
    server.ehlo()

    html = checks_html(df)

    # setup message
    msg = MIMEMultipart()
    msg['From'] = 'mensagensescala@voegol.com.br'
    msg['To'] = ', '.join(emails)
    msg['Subject'] = '[Alerta] Checks'

    msg.attach(MIMEText(html, 'html'))

    # send message
    if len(html) > 0:
        server.sendmail('mensagensescala@voegol.com.br', emails, msg.as_string())
    server.quit()

    
def checks_xq_html(df):
    
    df = df.copy()

    # keep only records that day offs are not ok
    df = df[df.atualizar==False]
    if df.shape[0] < 1:
        return ''

    df = df[['cif',
             'guerra',
             'funcao',
             'base',
             'checkTypeCode',
             'expiryDt', 
             'status', 
             'nota', 
             'data_conclusao',
             'ensino',
             'data_ensino',
             'xq',
             'data_xq',
             'atualizar']]

    # set style
    df.to_csv('debug.csv', sep=';')
    data = df.to_dict('records')

    # load template
    with open('./templates/checks_xq.html', 'r', encoding='utf-8') as file:
        template = file.readlines() 

    mail_template = Template(''.join(template))

    html = mail_template.render({
        'data': data
    })

    return html


def send_checks_xq_mail(df, user, password, emails):
    # config server
    server = smtplib.SMTP('smtp.office365.com',587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.SentOnBehalfOfName = 'mensagensescala@voegol.com.br'
    server.ehlo()

    html = checks_xq_html(df)

    # setup message
    msg = MIMEMultipart()
    msg['From'] = 'mensagensescala@voegol.com.br'
    msg['To'] = ', '.join(emails)
    msg['Subject'] = '[Alerta] Checks'

    msg.attach(MIMEText(html, 'html'))

    # send message
    if len(html) > 0:
        server.sendmail('mensagensescala@voegol.com.br', emails, msg.as_string())
    server.quit()