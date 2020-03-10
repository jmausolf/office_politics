import pandas as pd
import numpy as np


#################################################################
## Phase 4: Merge FEC CID Data
#################################################################

#################################################################
# Utility Functions
#################################################################

def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff


#################################################################
## Step 0A: Get Fullname Fortune 1000 List with List_ID
#################################################################

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
fk.to_csv("fortune1000-list_id.csv", index=False)
print(fk)
#print(fk.columns)


#################################################################
## Step 0B: Target Companies List
#################################################################

ext = pd.read_csv("experiment_results_with_bounces_errors.csv")
print(ext.columns)

ext = ext[['wave_index', 'company', 'list_id', 'party', 'callback_binary', 'pair_callback_bin']]

#need antijoin
ext_focus = ext.loc[ext['pair_callback_bin'] >= 1]
print(ext_focus)

#Make OpenSecrets QC FEC Crosswalk Blank
ext = ext[['company', 'list_id']]
ext = ext.merge(fk, how = 'left', on = 'list_id')
ext['os_party'] = None
ext = ext.drop_duplicates()
ext = ext.sort_values(['list_id'])
ext.to_csv("OpenSecrets_crosswalk_fec.csv", index=False)

print(ext)

#################################################################
## Step 1A: Load Data and Join OpenSecrets QC FEC
#################################################################

os_fec = pd.read_csv("MASTER_OpenSecrets_crosswalk_fec.csv")
os_fec = os_fec[['list_id', 'os_party']]
print(os_fec.isna().sum())

#Load Experiment Data, Join with FEC
ex = pd.read_csv("experiment_results_with_bounces_errors.csv")
print(ex)

#Join Data and Fill NA with Zero
df1A = ex.merge(os_fec, how='left', on='list_id')
print(df1A)
#df1A['found_party'] = df1A['os_party']
df1A['found_fec'] = np.where((df1A['os_party'].notna()), 
								True, None)
df1A = df1A.dropna(subset=['found_fec'])


ex_rem = anti_join(ex, df1A, key='index_wave')
print("Experiment 1A: remaining:", ex_rem.shape, df1A.shape)
#print(df1A.columns)

#################################################################
## Step 1B: Load Data and Join FEC Direct
#################################################################


#Load FEC Analysis Data, Join FK
fec = pd.read_csv("company_party_polarization.csv")
fec = fec.merge(fk, how='left', 
					left_on=['cid_master'],
					right_on=['fec_company'])

#Add FEC Indicator Variable
fec['found_fec'] = True
#print(fec)



#Load Experiment Data, Join with FEC
ex = pd.read_csv("experiment_results_with_bounces_errors.csv")
#print(ex)

#Join FEC With Remaining Experiment Data
df1B = ex_rem.merge(fec, how='left', on='list_id')
#print(df1B)

#Identify Max Cycle by Company and Keep Max
df1B['cycle_max'] = df1B.groupby(['company'])['cycle'].transform(max)
df1B = df1B.loc[ (df1B['cycle'] == df1B['cycle_max']) |
			 (df1B['found_fec'].isna()) ]


df1B = df1B.dropna(subset=['found_fec'])
ex_rem = anti_join(ex_rem, df1B, key='index_wave')
print("Experiment 1B: remaining:", ex_rem.shape, df1B.shape)


##Append the Results and Dedupe
df = pd.concat([df1A, df1B, ex_rem], 
				axis=0, sort=True).reset_index(drop=True)
print(df.shape)

#Drop Pure Duplicates
df = df.drop_duplicates()
#print(df.columns.tolist())




#################################################################
## Step 3: Save Two Analysis Sets
#################################################################

#Save Full Results with Bounces
outfile0 = "ANALYSIS_experiment_results_with_bounces_errors.csv"
df.to_csv(outfile0, index=False)
#print(df)
print(df.shape)
print("[*] saving dataset {} ...".format(outfile0))


#Save Only Pairs without Any Bounces/Error/Other Results
df = df.loc[df['pair_beo_bin'] == 0]
#print(df)
print(df.shape)

outfile1 = "ANALYSIS_experiment_results.csv"
df.to_csv(outfile1, index=False)
print("[*] saving dataset {} ...".format(outfile1))


#Save Only Pairs without Any Bounces/Error/Other Results
#and complete FEC data
df = df.loc[~df['found_fec'].isna()]
#print(df)
print(df.shape)

outfile2 = "ANALYSIS_experiment_results_fec.csv"
df.to_csv(outfile2, index=False)
print("[*] saving dataset {} ...".format(outfile2))


outfile2 = "../analysis/ANALYSIS_experiment_results_fec.csv"
df.to_csv(outfile2, index=False)
print("[*] saving dataset {} ...".format(outfile2))

