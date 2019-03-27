from leadiro_contacts.clean_leadiro import *
from lead_utils.lead_utils import *
import os, sys, subprocess, time

n = 5

#Combine Leadiro Files, Clean, and Match
os.chdir('leadiro_contacts')
subprocess.call('python3 clean_leadiro.py', shell=True)
os.chdir('..')


#Calculate Remaining Leadiro Contacts
abm_start = ret_abm_start()
start_message = '[*] initial leadiro list: {}'.format(abm_start.shape[0])
print(start_message)
leads_remaining = get_leadiro_remaining()


#Rematch to look for dupes
'''
clean_leadiro_main(
	combined_leadiro_file='leadiro_contacts/leadiro_combined.csv',
	leadiro_col = 'company',
	emp_file = 'lead_utils/leadiro_remaining_raw.csv',
	emp_col = 'company',
	local_out = 'leadiro_matched.csv',
	matched_leadiro_key = 'lead_utils/leadiro_matched_key.csv',
	match_only=True
	)
'''


abm_updated = update_abm(leads_remaining, abm_start)
end_message = '[*] remaining leadiro firms: {}'.format(abm_updated.shape[0])
print(end_message)
print('[*] opening new abm list in {} seconds'.format(n))
countdown(n)
subprocess.call('open lead_utils/updated_abm.csv', shell=True)