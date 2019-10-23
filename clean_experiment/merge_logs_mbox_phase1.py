import pandas as pd
import re
from qc_phase_1_manual_recoding import *



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
dfb = pd.read_csv("extracted_bounce_emails.csv")
bf = dfb[['mb_id', 'extracted_email']]

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

#Step 1A: Merge Bounced Emails
dfA = mb.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'extracted_email'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfA['merge_match_type'] = 'bounce_email_match'
dfA['verified_link'] = None
dfA['linkage'] = dfA['extracted_email']
dfA = dfA.dropna(subset=['index_wave'])
mb_rem = anti_join(mb, dfA, key='mb_id')
print("MB A: remaining:", mb_rem.shape, dfA.shape)


#Step 1B: First Pass Merge
dfB = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_email_clean'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfB['merge_match_type'] = 'full_email_match'
dfB['verified_link'] = None
dfB['linkage'] = dfB['from_email_clean']
dfB = dfB.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfB, key='mb_id')
print("MB B: remaining:", mb_rem.shape, dfB.shape)


#Step 1C: User Merge 
#(same user, different full email, e.g.
# k.linda@jpmorganchase.com vs. k.linda@chase.com)
dfC = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_user'],
			  right_on=['profile', 'gmail_user', 'contact_user'])
dfC['merge_match_type'] = 'username_match'
dfC['verified_link'] = None
dfC['linkage'] = dfC['from_user']
dfC = dfC.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfC, key='mb_id')
print("MB C: remaining:", mb_rem.shape, dfC.shape)



#Step 1D: Domain Merge
dfD = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_domain'],
			  right_on=['profile', 'gmail_user', 'contact_domain'])
dfD['merge_match_type'] = 'domain_match'
dfD['verified_link'] = None
dfD['linkage'] = dfD['from_domain']
dfD = dfD.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfD, key='mb_id')
print("MB D: remaining:", mb_rem.shape, dfD.shape)


#Step 1E: Remaining Missing Attempt
dfE = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'missing_email'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfE['merge_match_type'] = 'missing_email_extraction_full_match'
dfE = dfE.dropna(subset=['index_wave'])
dfE['verified_link'] = None
dfE['linkage'] = dfE['missing_email']
mb_rem = anti_join(mb_rem, dfE, key='mb_id')
print("MB E: remaining:", mb_rem.shape, dfE.shape)


#Step 1F0: Joining Verified Links Post Manual Search

#Load Converted XLS Missing Verified Links
lf = pd.read_csv("MASTER_linked_missing_emails.csv")
lf = lf[['mb_id', 'verified_linkage']]

#Merge Verified Links with Missing Emails
mb_rem = mb_rem.merge(lf, how='left', on='mb_id')

#Drop Invalid Verifed Links
mb_rem = mb_rem.loc[mb_rem['verified_linkage'] != 'INVALID']

#Load Experiment Data
ex = pd.read_csv("cleaned_experimental_wave_results.csv")


#Step 1F1: Merge Missing Link Emails
dfF = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'verified_linkage'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfF['merge_match_type'] = 'verified_linkage_full_email_match'
dfF = dfF.dropna(subset=['index_wave'])

dfF['verified_link'] = dfF['verified_linkage']
dfF['linkage'] = dfF['verified_linkage']
dfF = dfF.drop(columns=['verified_linkage'])
mb_rem = anti_join(mb_rem, dfF, key='mb_id')
mb_rem = mb_rem.drop(columns=['verified_linkage'])
print("MB F: remaining:", mb_rem.shape, dfF.shape)


## Step 1Z: Append the Results and Dedupe
df = pd.concat([dfA, dfB, dfC, dfD, dfE, dfF], axis=0).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates()


##############################################################
#Step 2: Isolate Linked Data, Dupes, and Missing
##############################################################

df_app = df.dropna(subset=['index_wave'])
df_app = df_app.sort_values(by=['index_wave'])
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

#Add Recodings from QC Review
df_app = recode_outcomes(df_app)

#Save Final Version - Phase 1
df_app.to_csv('found_appid_deduped.csv', index=False)


#TODO
#QC corrections of outcome coding - pre-phase-2



