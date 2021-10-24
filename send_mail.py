import sys
from modules.mail import send_mail
from modules.mail import mail_content
from modules.mail import crew_dates, records
from config.variables import user
import pandas as pd
from datetime import datetime as dt

def send(crew, crew_dates=crew_dates, records=records):
    print(f'Sending mail to {crew}: ', end='')
    if crew[0].isdigit():
        crew = crew.zfill(8)[-8:]
        df = crew_dates[crew_dates['cif']==crew].copy()
    else:
        crew = crew.upper()
        df = crew_dates[crew_dates['name']==crew].copy()

    if df.shape[0] == 1:
        name = df.name.values[0]
        address = df.email.values[0] + '@voegol.com.br'
        content = mail_content(name, crew_dates, records)
        send_mail(content, user['mail'], user['password'], [address])
        print(f'OK')
        # log successful
        with open('./logs/mail_sent.log', mode='a') as log:
            log.write(f'{name}; {dt.now().strftime("%Y-%m-%d %H:%M")}\n')
    
    else:
        print(f'FAIL (NOT FOUND)')
        # log fail
        with open('./logs/mail_fail.log', mode='a') as log:
            log.write(f'{crew}; {dt.now().strftime("%Y-%m-%d %H:%M")}\n')
        

if __name__ == "__main__":
    args = sys.argv

    if '--all' in args:
        for crew in crew_dates['name'].to_list():
            send(crew)

    elif '--list' in args:
        file = args[2]
        for crew in pd.read_csv(file , header=None)[0].to_list():
            send(crew)

    elif len(args) > 1:
        for crew in args[1:]:
            send(crew)

    else:
        print('Usage: python send_mail.py <crew_id>')
        print('Usage: python send_mail.py --list <file>')
        print('Usage: python send_mail.py --all')

