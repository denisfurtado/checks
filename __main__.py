import sys
from datetime import datetime as dt
from config.variables import user
from modules.generate_data import get_checks
from modules.generate_data import get_crew_info
from modules.generate_data import get_roster_tag
from modules.generate_data import get_rosters
from modules.generate_data import get_data_neolude

args = sys.argv
#use_cached = not ('--dont-use-cache' in args)
#days = int(args[1]) if '--days' in args else 180

#-------------------------------------------------------------------
# get all data 
checks = get_checks(user, log_info=False, active=True)
crew_info = get_crew_info(user, log_info=False, date=dt.now())
roster_tag = get_roster_tag(user, log_info=False, period=dt.now(), tag_type='', all_period=True)
rosters = get_rosters(user, log_info=False, period=dt.now(), all_period=True)
arp = get_data_neolude(user, log_info=False, training_id=14140)
eqp = get_data_neolude(user, log_info=False, training_id=16766)
emg = get_data_neolude(user, log_info=False, training_id=18180)
emg_presencial = get_data_neolude(user, log_info=False, training_id=25250)
sec = get_data_neolude(user, log_info=False, training_id=6173)
sgso = get_data_neolude(user, log_info=False, training_id=14241)
cfi = get_data_neolude(user, log_info=False, training_id=6167)

#-------------------------------------------------------------------

#-------------------------------------------------------------------
# final report
print(' ' * 60)
print('done')