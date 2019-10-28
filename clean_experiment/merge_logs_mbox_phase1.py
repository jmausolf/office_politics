import pandas as pd
import re
from qc_phase_1_manual_recoding import *
from df_app_col import df_app_cols


#################################################################
# Utility Functions
#################################################################

def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


def index_to_n(index_number, letter='n'):

	#Set to 1 index versus 0
	i = int(index_number)+1

	#Return as String
	if i < 10:
		return letter+'000'+str(i)
	elif i < 100:
		return letter+'00'+str(i)
	elif i < 1000:
		return letter+'0'+str(i)
	else:
		return letter+str(i)


def make_id(row, prefix):
	index = row['index']
	return index_to_n(index, prefix)



#################################################################
# Phase 1: Join MBOX Results to Applicant Wave ID's
#################################################################

###################################
# Step 0: Load Data Frames
###################################

#Step 0A: Load Main Data
mb = pd.read_csv("mbox_analysis.csv")
ex = pd.read_csv("cleaned_experimental_wave_results.csv")


#Step 0B: Load Bounce Linkages
df1B = pd.read_csv("extracted_bounce_emails.csv")
bf = df1B[['mb_id', 'extracted_email']]

#Step 0C: Load Missing Email Linkages
dfm = pd.read_csv("linked_missing_emails.csv")
me = dfm[['mb_id', 'missing_email']]

# Add MB Index
mb = mb.reset_index()
mb['mb_id'] = mb.apply(make_id, prefix='MB_', axis=1)
mb = mb.drop(columns=['wave'])

# Add MB Bounce Linkage Column and Merge with Ex Log
mb = mb.merge(bf, how='left')
mb = mb.merge(me, how='left')


###########################################
# Step 1: Join MBOX in Stepwise Methods
###########################################

#Load Converted XLS QC Link
mbqc = pd.read_csv("MASTER_qc_mb_index_wave_link.csv")
mbqc = mbqc[['mb_id', 'index_wave']]
mbp = mb.merge(mbqc, on='mb_id', how='left')


#Step 0A: Add Preemptive Mismatches
df0A = mbp.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'index_wave'],
			  right_on=['profile', 'gmail_user', 'index_wave'])
df0A['merge_match_type'] = 'bounce_email_match'
df0A['verified_link'] = None
df0A['linkage'] = df0A['extracted_email']
df0A = df0A.dropna(subset=['index_wave'])
mbp = mbp.drop(columns=['index_wave'])
mb_rem = anti_join(mbp, df0A, key='mb_id')
print("MB 0A: remaining:", mb_rem.shape, df0A.shape)


#Step 1A: Merge Bounced Emails
df1A = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'extracted_email'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
df1A['merge_match_type'] = 'bounce_email_match'
df1A['verified_link'] = None
df1A['linkage'] = df1A['extracted_email']
df1A = df1A.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, df1A, key='mb_id')
print("MB 1A: remaining:", mb_rem.shape, df1A.shape)



#Step 1B: First Pass Merge
df1B = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_email_clean'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
df1B['merge_match_type'] = 'full_email_match'
df1B['verified_link'] = None
df1B['linkage'] = df1B['from_email_clean']
df1B = df1B.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, df1B, key='mb_id')
print("MB 1B: remaining:", mb_rem.shape, df1B.shape)


#Step 1C: User Merge 
df1C = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_user'],
			  right_on=['profile', 'gmail_user', 'contact_user'])
df1C['merge_match_type'] = 'username_match'
df1C['verified_link'] = None
df1C['linkage'] = df1C['from_user']
df1C = df1C.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, df1C, key='mb_id')
print("MB 1C: remaining:", mb_rem.shape, df1C.shape)



#Step 1D: Domain Merge
df1D = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_domain'],
			  right_on=['profile', 'gmail_user', 'contact_domain'])
df1D['merge_match_type'] = 'domain_match'
df1D['verified_link'] = None
df1D['linkage'] = df1D['from_domain']
df1D = df1D.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, df1D, key='mb_id')
print("MB 1D: remaining:", mb_rem.shape, df1D.shape)


#Step 1E: Remaining Missing Attempt
df1E = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'missing_email'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
df1E['merge_match_type'] = 'missing_email_extraction_full_match'
df1E = df1E.dropna(subset=['index_wave'])
df1E['verified_link'] = None
df1E['linkage'] = df1E['missing_email']
mb_rem = anti_join(mb_rem, df1E, key='mb_id')
print("MB 1E: remaining:", mb_rem.shape, df1E.shape)


#Step 1F0: Joining Verified Links Post Manual Search

#Load Converted XLS Missing Verified Links
lf = pd.read_csv("MASTER_linked_missing_emails.csv")
lf = lf[['mb_id', 'verified_linkage']]

#Merge Verified Links with Missing Emails
mb_rem = mb_rem.merge(lf, how='left', on='mb_id')

#Drop Invalid Verifed Links
mb_rem = mb_rem.loc[mb_rem['verified_linkage'] != 'INVALID']

#Step 1F1: Merge Missing Link Emails
df1F = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'verified_linkage'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
df1F['merge_match_type'] = 'verified_linkage_full_email_match'
df1F = df1F.dropna(subset=['index_wave'])

df1F['verified_link'] = df1F['verified_linkage']
df1F['linkage'] = df1F['verified_linkage']
df1F = df1F.drop(columns=['verified_linkage'])
#df1F.columns = df_app_cols
mb_rem = anti_join(mb_rem, df1F, key='mb_id')
mb_rem = mb_rem.drop(columns=['verified_linkage'])
print("MB 1F: remaining:", mb_rem.shape, df1F.shape)


## Step 1Z: Append the Results and Dedupe
df = pd.concat([df0A, df1A, df1B, df1C, df1D, df1E, df1F], 
				axis=0, sort=True).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates()


##############################################################
#Step 2: Isolate Linked Data, Dupes, and Missing
##############################################################

df_app = df.dropna(subset=['index_wave'])
df_app = df_app.sort_values(by=['index_wave'])
#df_app.columns = df_app_cols
df_app.to_csv('found_appid.csv', index=False)

#Identify Duplicates Domain Matches for Review
df_app_dupes = df_app
df_app_dupes['dupe_mb'] = df_app_dupes.duplicated(subset=['mb_id'], keep=False)
df_app_dupes = df_app_dupes.loc[df_app_dupes['dupe_mb'] == True]
df_app_dupes.to_csv('dupes_to_review.csv', index=False)

#Load/Merge Manual Verfified Valid/Invalid Dupes
du = pd.read_csv("MASTER_dupes_to_review.csv")
du = du[['mb_id', 'index_wave', 'valid_dupe']]
df_app = df_app.merge(du, how='left', on=['mb_id', 'index_wave'])
#df_app.columns = df_app_cols
df_app = df_app.loc[df_app['valid_dupe'] != 'INVALID']
df_app = df_app.drop(columns=['dupe_mb', 'valid_dupe'])


#Evaluate Missing Emails
missing_emails = anti_join(mb, df_app, 'mb_id')
missing_emails = missing_emails.sort_values(by=['mbox_email', 'from_domain'])

#Ignore If Verfied Link if Invalid
me = missing_emails
me = me.merge(lf, how='left', on='mb_id')
me = me.loc[me['verified_linkage'] != 'INVALID']

#Also Ignore If Outome is Other (Blocked)
me = me.loc[me['outcome'] != 'Other']
print("Missing Emails: remaining:", me.shape)
me.to_csv('missing_emails.csv', index=False)


#Add Outcome Recodings from QC Review
df_app = recode_outcomes(df_app)
df_app = df_app[df_app_cols]

#Save Final Version - Phase 1
df_app.to_csv('found_appid_deduped.csv', index=False)
print("Final DF App: ", df_app.shape)

#TODO
#QC corrections of outcome coding - pre-phase-2



