

#Basic Process for Collecting Leadiro with GUI


#Upload ABM File and Apply Filters Online
#Manually Review Contacts in Shopping Cart, Download
#Once Downloaded, Run Clean Leadiro Matcher Against Employers Key
#Make Antijoin Function
#(Left join employers key and matched leads, select missing field, e.g. contact_email)
#Drop those with a contact email in the merged list, these are the ones still missing an employer
#Alternatively 

import pandas as pd
import numpy as np
import time
from leadiro_contacts.clean_leadiro import *


def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


def get_leadiro_remaining(emp_key='../keys/cleaned_employers_key.csv',
						  leads_key='../keys/leadiro_matched_key.csv',
						  join_key='company'):		

	emp_key_master = pd.read_csv(emp_key)
	leadiro_matched = pd.read_csv(leads_key)
	leadiro_remaining = anti_join(emp_key_master, leadiro_matched, join_key)
	

	leadiro_remaining.to_csv('lead_utils/leadiro_remaining_raw.csv', index=False)
	return leadiro_remaining



#Run Remaining Against Leadiro

def ret_abm_start(emp_key='../keys/cleaned_employers_key.csv',
				  abm_key='lead_utils/leadiro_master_abm.csv',
				  abm_col='company'
				  ):

	emp_key_master = pd.read_csv(emp_key)
	abm_master = pd.read_csv(abm_key)

	abm_start = pd.merge(emp_key_master, abm_master, how='left')
	abm_start = abm_start[[abm_col]]
	abm_start.to_csv('lead_utils/initial_abm.csv', index=False)
	return abm_start



def update_abm(leadiro_remaining, abm_start, abm_col='company'):

	abm_remaining = pd.merge(leadiro_remaining, abm_start, how='left')
	abm_remaining = abm_remaining[[abm_col]]
	abm_remaining.to_csv('lead_utils/updated_abm.csv', index=False)
	return abm_remaining



def status_bar(start_val, end_val, bar_length=20, form='progress'):

    #Core Progress
    progress = float(start_val) / end_val
    arrow = '-' * int(round(progress * bar_length-1)) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    bar = arrow + spaces

    if form == 'progress':
        #Progress
        completed = int(round(progress * 100))
        out = "\rPercent: [{0}] {1: >5}%".format(bar, completed)

    elif form == 'countdown':
        #Countdown
        remainder = int(round(end_val - start_val))
        out = "\rCountdown: [{0}] {1: >5} seconds".format(bar, remainder)

    #Updater
    sys.stdout.write(out)
    sys.stdout.flush()


def countdown(seconds):

    for i in range(seconds+1):
        time.sleep(1)
        status_bar(i, seconds, form='countdown')

    sys.stdout.write('\n')
    sys.stdout.flush()




