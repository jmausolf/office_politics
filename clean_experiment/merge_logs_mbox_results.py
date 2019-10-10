import pandas as pd
import re

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


#No response will be those that were sent (in log)
#but did not have any result (direct, domain, or call in mbox)

## Phase 0:
## rm the ones that never sent from log (blocked pre-send gmail)
## rm bounces (never reached target, ergo, irrelevant)
## rm sent emails


## Phase 1: Left Joins on MBOX to link log app id's to mbox results
## - direct replies
## - domain replies (cc, third party)
## - grasshopper

#Step 0A: Load Main Data
mb = pd.read_csv("mbox_analysis.csv")
ex = pd.read_csv("cleaned_experimental_wave_results.csv")

print(mb.shape)
#print(mb.columns)
#print(mb)
print(ex.shape)
#print(ex.columns)

#Step 0B: Load Bounce Linkages
dfb = pd.read_csv("extracted_bounce_emails.csv")
bf = dfb[['mb_id', 'extracted_email']]
#print(bf)


# Add MB Index
mb = mb.reset_index()
mb['mb_id'] = mb.apply(make_id, prefix='MB_', axis=1)
mb = mb.drop(columns=['wave'])

# Add MB Bounce Linkage Column and Merge with Ex Log
mb = mb.merge(bf, how='left')

#Step A: Merge Bounced Emails
dfA = mb.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'extracted_email'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfA['merge_match_type'] = 'bounce_email_match'
dfA = dfA.dropna(subset=['index_wave'])
mb_rem = anti_join(mb, dfA, key='mb_id')
print("MB A: remaining:", mb_rem.shape)


#Remove Bounces
#mb = mb.loc[mb['outcome'] != 'Bounce']


#print(mb.shape)
#print(mb.columns)
#print(mb)
#print(ex.shape)
#print(ex.columns)

#TODO add match type cols

#Step B: First Pass Merge
dfB = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_email_clean'],
			  right_on=['profile', 'gmail_user', 'contact_email'])
dfB['merge_match_type'] = 'full_email_match'
dfB = dfB.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfB, key='mb_id')
print("MB B: remaining:", mb_rem.shape)


#Step C: User Merge 
#(same user, different full email, e.g.
# k.linda@jpmorganchase.com vs. k.linda@chase.com)
dfC = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_user'],
			  right_on=['profile', 'gmail_user', 'contact_user'])
dfC['merge_match_type'] = 'username_match'
dfC = dfC.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfC, key='mb_id')
print("MB C: remaining:", mb_rem.shape)



#Step D: Domain Merge
dfD = mb_rem.merge(ex, how='left',
			  left_on=['profile', 'mbox_email', 'from_domain'],
			  right_on=['profile', 'gmail_user', 'contact_domain'])
dfD['merge_match_type'] = 'domain_match'
dfD = dfD.dropna(subset=['index_wave'])
mb_rem = anti_join(mb_rem, dfD, key='mb_id')
print("MB D: remaining:", mb_rem.shape)




#Other Types:
'''
#A. both domain and user are different
	e.g.	mb: michael_berube@uhg.com
			ex: monica_hamling@uhc.com

			Email from michael_berube@uhg.com 
			mentions 'Monica Hamling'
			need a 'full name' column in ex
			then a match based on the gmail/mbox user and the full name
			being found in the message


#B			Email from Betsy Makwinski	notification@jobvite.com
			mentions in subject line company Benefitfocus

			company Benefitfocus in company col in experiment

#C 			Mbox waves are incorrect, problematic, causing issues
			TL;DR, don't merge on wave, drop wave from mbox df



'''

#Step D: Grasshopper appid, tbd

## Append the Results and Dedupe

df = pd.concat([dfA, dfB, dfC, dfD], axis=0).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates()

#Separate Data Into Those with AppID and Those Still Missing
df_app = df.dropna(subset=['index_wave'])
df_app = df_app.sort_values(by=['index_wave'])
print(df_app.shape)
df_app.to_csv('found_appid.csv', index=False)

df_app_dupes = df_app
df_app_dupes = df_app_dupes.drop_duplicates(subset=['mb_id', 'index_wave'])
df_app_dupes['dupe_mb'] = df_app_dupes.duplicated(subset=['mb_id'], keep=False)
df_app_dupes = df_app_dupes.loc[df_app_dupes['dupe_mb'] == True]
print(df_app_dupes.shape)




#df_app_dupes = df_app
#df_app_dupes['dupe_appid'] = df_app_dupes.duplicated(subset=['index_wave'], keep=False)
#df_app_dupes = df_app_dupes.loc[df_app_dupes['dupe_appid'] == True]
#print(df_app_dupes)
df_app_dupes.to_csv('dupes_to_review.csv', index=False)


#TODO
#antijoin df_app with mb to get mbox data still missing app id
#found_
missing_emails = anti_join(mb, df_app, 'mb_id')
#print(missing_emails)
print(missing_emails.shape)
missing_emails.to_csv('missing_emails.csv', index=False)

#missing, was 270
#found app was 705

#missing post rm wave = 135
#found post rm wave = 901

#Current missing is manageable, some dupes and lots of grasshopper
#TODO prog a method to incorporate manual keep, reject and app key


#Also #TODO
#currently all bounces are dropped, but will need bounces later
#because I need to mark all ones that sent but did not bounce as 
#no-replies. I don't want to label bounces no-replies, just drop from analysis

#Also TODO, need a pair ID. For example, I want to ensure I end up with complete pairs
#not partial pairs if one half bounced and the other did not
#rm if count (post spread) for pair is != 2


#print(df.shape)
#print(df.columns)
#print(df.isna().sum())

#print(df.shape)
#print(df_app.shape[0]+missing_emails.shape[0])

#df.to_csv('test.csv', index=False)

## Phase 2: Take MBOX Data Linked to App ID's and spread into new columns
##(for response type: direct, third-party reply, phone reply)




## Phase 3: Fill Out Links from Grasshopper Calls to App ID's


## Phase 4: Left Join Log File with Cleaned App-ID level mbox results
## Summarize Result Types, Analysis


