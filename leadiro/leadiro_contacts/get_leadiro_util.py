

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
#from leadiro_contacts.clean_leadiro import *

def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


def get_leadiro_remaining(emp_key='../../keys/cleaned_employers_key.csv',
						  leads_key='../../keys/leadiro_matched_key.csv',
						  join_key='company'):		

	emp_key_master = pd.read_csv(emp_key)
	leadiro_matched = pd.read_csv(leads_key)
	leadiro_remaining = anti_join(emp_key_master, leadiro_matched, join_key)
	

	leadiro_remaining.to_csv('leadiro_remaining_raw.csv', index=False)
	print(leadiro_remaining)
	return leadiro_remaining



#Calculate New Abm List
def update_abm(abm_master_df, leads_remaining_df, abm_col='company'):
	pass


#Run Remaining Against Leadiro

def ret_abm_start(emp_key='../../keys/cleaned_employers_key.csv',
				  abm_key='leadiro_master_abm.csv',
				  abm_col='company'
				  ):

	emp_key_master = pd.read_csv(emp_key)
	abm_master = pd.read_csv(abm_key)

	abm_start = pd.merge(emp_key_master, abm_master, how='left')

	#abm_start = abm_start[['company', 'raw_company']]
	abm_start = abm_start[[abm_col]]
	return abm_start
	#print(abm_start.shape)
	#print(abm_start.columns)


def update_abm(leadiro_remaining, abm_start, abm_col='company'):

	abm_remaining = pd.merge(leadiro_remaining, abm_start, how='left')
	abm_remaining = abm_remaining[[abm_col]]
	print(abm_remaining.shape)
	return abm_remaining

#df_abm_master = pd.read_csv('leadiro_master_abm.csv')
#print(df_abm_master.shape)

abm_start = ret_abm_start()

#TODO rerun the clean_leadiro matching against remaining to look for duplicates
leads_remaining = get_leadiro_remaining()


abm_updated = update_abm(leads_remaining, abm_start)




print(abm_updated)







