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


#Step 1: First Pass Merge
df = mb.merge(ex, how='left',
			  left_on=['mbox_email', 'from_email_clean'],
			  right_on=['gmail_user', 'contact_email'])
print(df)

df.to_csv('test.csv', index=False)

#Step 2: Domain Merge

#Step 3: Grasshopper appid, tbd


## Phase 2: Take MBOX Data Linked to App ID's and spread into new columns
##(for response type: direct, third-party reply, phone reply)




## Phase 3: Fill Out Links from Grasshopper Calls to App ID's


## Phase 4: Left Join Log File with Cleaned App-ID level mbox results
## Summarize Result Types, Analysis