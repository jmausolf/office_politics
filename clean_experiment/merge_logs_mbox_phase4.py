import pandas as pd
import numpy as np

#################################################################
## Phase 4: Merge FEC CID Data
#################################################################



#################################################################
## Step 1: Load Data and Join
#################################################################

#Load Data
#mb = pd.read_csv('appid_level_mbox_results.csv')
#ex = pd.read_csv("cleaned_experimental_wave_results.csv")
#le = pd.read_csv("full_leadiro_master_abm.csv")
#print(mb.shape, ex.shape, le.shape)


#Load Fortune 1000-List, Add List_ID Col
fk = pd.read_csv("fortune1000-list.csv")
fk['index'] = fk.index
fk['index'] = fk['index'].apply(lambda x: str(x))
fk['list_id'] = 'f1000_'+fk['index']
fk = fk[['company', 'list_id']]
fk.columns = ['fec_company', 'list_id']
 
fkb = pd.DataFrame({'fec_company':['Berkshire Hathaway'],
				    'list_id':['f1000_01']})
fk = fk.append(fkb, ignore_index=False)

print(fk)
#print(fk.columns)


#Load FEC Analysis Data, Join FK
fec = pd.read_csv("company_party_polarization.csv")
fec = fec.merge(fk, how='left', 
					left_on=['cid_master'],
					right_on=['fec_company'])


#Add FEC Indicator Variable
fec['found_fec'] = True

#Join On All Cycles to Maximize Matches
#fec = fec.loc[fec['cycle'] == 2016]
print(fec)
print(fec.columns)

#Load Experiment Data, Join with FEC
ex = pd.read_csv("experiment_results_with_bounces_errors.csv")
print(ex)

#Join Data and Fill NA with Zero
df1A = ex.merge(fec, how='left', on='list_id')

#Identify Max Cycle by Company and Keep Max
df1A['cycle_max'] = df1A.groupby(['company'])['cycle'].transform(max)
df1A = df1A.loc[ (df1A['cycle'] == df1A['cycle_max']) |
			 (df1A['found_fec'].isna()) ]

print(df1A)
print(df1A.isna().sum())


#TODO
#See if you can get more matches by company name
#or doing fec analysis for more companies or other sources
#Drop NA, Antijoin, Remerge Method 2


df = df1A



#################################################################
## Step 3: Save Two Analysis Sets
#################################################################

#Save Full Results with Bounces
outfile0 = "ANALYSIS_experiment_results_with_bounces_errors.csv"
df.to_csv(outfile0, index=False)
print(df)
print(df.shape)
print("[*] saving dataset {} ...".format(outfile0))


#Save Only Pairs without Any Bounces/Error/Other Results
df = df.loc[df['pair_beo_bin'] == 0]
print(df)
print(df.shape)

outfile1 = "ANALYSIS_experiment_results.csv"
df.to_csv(outfile1, index=False)
print("[*] saving dataset {} ...".format(outfile1))


#Save Only Pairs without Any Bounces/Error/Other Results
#and complete FEC data
df = df.loc[~df['found_fec'].isna()]
print(df)
print(df.shape)

outfile2 = "ANALYSIS_experiment_results_fec.csv"
df.to_csv(outfile2, index=False)
print("[*] saving dataset {} ...".format(outfile2))

