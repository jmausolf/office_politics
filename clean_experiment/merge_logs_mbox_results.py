import pandas as pd
import re


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

#Step 0: Load Data
mb = pd.read_csv("mbox_analysis.csv")
ex = pd.read_csv("cleaned_experimental_wave_results.csv")

print(mb.shape)
print(mb.columns)
print(ex.shape)
print(ex.columns)


#Step A: First Pass Merge
dfA = mb.merge(ex, how='left',
			  left_on=['profile', 'wave', 'mbox_email', 'from_email_clean'],
			  right_on=['profile', 'wave', 'gmail_user', 'contact_email'])



#Step B: User Merge 
#(same user, different full email, e.g.
# k.linda@jpmorganchase.com vs. k.linda@chase.com)
dfB = mb.merge(ex, how='left',
			  left_on=['profile', 'wave', 'mbox_email', 'from_user'],
			  right_on=['profile', 'wave', 'gmail_user', 'contact_user'])


#Step C: Domain Merge
dfC = mb.merge(ex, how='left',
			  left_on=['profile', 'wave', 'mbox_email', 'from_domain'],
			  right_on=['profile', 'wave', 'gmail_user', 'contact_domain'])



#Step D: Grasshopper appid, tbd

## Append the Results and Dedupe

df = pd.concat([dfA, dfB, dfC], axis=0).reset_index(drop=True)

#Drop Pure Duplicates
df = df.drop_duplicates()

#Separate Data Into Those with AppID and Those Still Missing
df_app = df.dropna(subset=['index_wave'])
print(df_app.shape)

df_app.to_csv('found_appid.csv', index=False)

#TODO
#antijoin df_app with mb to get mbox data still missing app id


print(df.shape)
#print(df.isna().sum())

df.to_csv('test.csv', index=False)

## Phase 2: Take MBOX Data Linked to App ID's and spread into new columns
##(for response type: direct, third-party reply, phone reply)




## Phase 3: Fill Out Links from Grasshopper Calls to App ID's


## Phase 4: Left Join Log File with Cleaned App-ID level mbox results
## Summarize Result Types, Analysis