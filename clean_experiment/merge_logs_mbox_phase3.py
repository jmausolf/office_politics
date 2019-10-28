import pandas as pd
import numpy as np

#################################################################
## Phase 3: Left Join Log File with Cleaned App-ID Mbox Results
## Summarize Result Types, Pre-analyis QC/Cleaning
#################################################################



#################################################################
## Step 1: Load Data and Join
#################################################################

#Load Data
mb = pd.read_csv('appid_level_mbox_results.csv')
ex = pd.read_csv("cleaned_experimental_wave_results.csv")
print(mb.shape, ex.shape)

#Join Data and Fill NA with Zero
df = ex.merge(mb, how='left', on='index_wave')
df = df.fillna(0)
print(df.shape)


#################################################################
## Step 2: Add Columns for QC on Bounce/Error/Other & Response
#################################################################

#Add Combined Bounce/Error/Other + Response Cols
df['bounce_error_other_sum'] = df['bounce'] + df['error'] + df['other']
df['bounce_error_other_binary'] = np.where((df['bounce_error_other_sum'] >= 1), 1, 0)

#Get Groupby Sums of Bounce_Error_Other_Binary & Response by Pair ID
dfqc_cols = ['pair_index', 'bounce_error_other_binary', 'response_binary']
dfqc = df[dfqc_cols].groupby(['pair_index']).sum()

#Clean Up Group By
dfqc = pd.DataFrame(dfqc.to_records())
dfqc.columns = ['pair_index', 'pair_beo_bin', 'pair_response_bin']



#Filter to Identify QC Cases to Review
#These are reviewd manually in Phase 1
qc_crit = (

				(
					(dfqc['pair_beo_bin'] >= 1) &
					(dfqc['pair_response_bin'] >= 1)
				)

			)


dfqc_filter = dfqc.loc[qc_crit]
df_qc = df.merge(dfqc_filter, on='pair_index', how = 'inner')
df_qc.to_csv("qc_pair_evaluation.csv", index=False)
print(df_qc)


#################################################################
## Step 3: TODO
#################################################################

## Drop Pairs where the bounce count >= 1
## So drop pairs where both bounced or where at least one bounced
## QC resolved false bounces
## With one exception, all bounces where one definitively bounced and 
	#the other is in question is small
## Ones with a bounce and one or more responses have been resolved

#print(df)

#Add Pair Results Columns
df = df.merge(dfqc, on='pair_index', how = 'inner')
print(df.shape)

#Save Full Results with Bounces
df.to_csv("ANALYSIS_experiment_results_with_bounces_errors.csv", index=False)

#Keep Only Pairs without Any Bounces/Error/Other Results
df = df.loc[df['pair_beo_bin'] == 0]
df.to_csv("ANALYSIS_experiment_results.csv", index=False)
print(df.shape)



#if __name__ == '__main__':

	#mb = make_detailed_outcomes(mb)
	#mb = spread_outcomes_sum(mb)

#	print(mb)

