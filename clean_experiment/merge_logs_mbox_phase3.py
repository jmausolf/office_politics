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
#print(df)
#print(df.isna().sum())


df2 = df.loc[df['callback_binary'] == 1]
print(df2.sum())


df2.to_csv("test_joined_data.csv", index=False)


#################################################################
## Step 2: Add Columns for QC on Bounce/Error/Other & Response
#################################################################

#Add Combined Bounce/Error/Other + Response Cols
df['bounce_error_other_sum'] = df['bounce'] + df['error'] + df['other']
df['bounce_error_other_binary'] = np.where((df['bounce_error_other_sum'] >= 1), 1, 0)
#df['beo_and_response_binary'] = df['bounce_error_other_binary'] + df['response_binary']

#Get Groupby Sums of Bounce_Error_Other_Binary & Response by Pair ID
dfqc_cols = ['pair_index', 'bounce_error_other_binary', 'response_binary']
dfqc = df[dfqc_cols].groupby(['pair_index']).sum()
print(dfqc)

#TODO
#add qc filters to review beo where pair sum == 1
#also add qc filter when beo >= 1 & response >= 1
#review those pairs or consider just dropping them

qc_crit = (
				#(
				#	(dfqc['bounce_error_other_binary'] == 1) 
				#) |

				(
					(dfqc['bounce_error_other_binary'] >= 1) &
					(dfqc['response_binary'] >= 1)
				)

			)

dfqc = dfqc.loc[qc_crit]
dfqc = pd.DataFrame(dfqc.to_records())


dfqc.columns = ['pair_index', 'pair_beo_bin', 'pair_response_bin']
print(dfqc)


df_qc = df.merge(dfqc, on='pair_index', how = 'inner')
print(df_qc)


df_qc.to_csv("qc_pair_evaluation.csv", index=False)

#print(df)
#print(df.isna().sum())


def get_reply_types_str(df):

	#Direct Email Reply Crit
	der_crit = (
					(
						(df['merge_match_type'] == 'full_email_match') &
						(df['outcome'].isin(['Callback', 'Reply']))
					) |

					(
						(df['merge_match_type'] == 'username_match') &
						(df['outcome'].isin(['Callback', 'Reply']))
					)

				)

	df['direct_email_reply'] = ''
	df.loc[der_crit, 'direct_email_reply'] = 'direct_email_reply'


	#Other Email Reply
	oer_crit = (

					(
						(df['merge_match_type'].isin(['domain_match', 
													  'verified_linkage_full_email_match',
													  'missing_email_extraction_full_match']
													  )) &
						(df['outcome'].isin(['Callback', 'Reply'])) &
						(df['from_full_domain'] != 'grasshopper.com' )
					)

				)

	df['other_email_reply'] = ''
	df.loc[oer_crit, 'other_email_reply'] = 'other_email_reply'


	#Phone (Voicemail) Reply
	pr_crit = (df['from_full_domain'] == 'grasshopper.com' )
	df['phone_reply'] = ''
	df.loc[pr_crit, 'phone_reply'] = 'phone_reply'
	


	print(df)
	return df.copy()


def join_reply_types(row):

	if row['outcome'] not in ['CALLBACK', 'REPLY']:
		return row['outcome']
	else:
		return row['outcome']+'-'+row['reply_type']


def make_detailed_outcomes(df):

	df = get_reply_types_str(df)
	df['outcome'] = df['outcome'].str.upper()
	reply_cols = ['direct_email_reply', 'other_email_reply', 'phone_reply']

	df['reply_type'] = df[reply_cols].apply(lambda x: ''.join(x.values.astype(str)), axis=1)
	df['outcome_detailed'] = df.apply(join_reply_types, axis=1)
	df = df.groupby(['index_wave', 'outcome_detailed']).size().reset_index(name='count')

	print(df.shape)
	return df


#################################################################
## Step 2: Spread to App-ID Level
#################################################################

#Clean and Lower Column Names
def clean_cols(col):
    return str(col).lower().replace(' ', '_')

#Spread Cols and Sum Function
def spread_outcomes_sum(df):

	#Get Overall Outcome at Index_Wave (App ID) Level
	df = df.pivot_table(index=['index_wave'],
	                    columns='outcome_detailed', 
	                    values='count')


	#Add Total Callbacks_Mes, Total Replies, Total Response Cols
	callback_cols = ['CALLBACK-direct_email_reply',
					 'CALLBACK-other_email_reply',
					 'CALLBACK-phone_reply']

	reply_cols =   ['REPLY-direct_email_reply',
					'REPLY-other_email_reply',
					'REPLY-phone_reply']

	df['total_callback_messages'] = df[callback_cols].sum(axis=1)
	df['total_reply_messages'] = df[reply_cols].sum(axis=1)
	df['total_reponse_messages'] = df['total_callback_messages'] + df['total_reply_messages']

	#Add Binary Cols
	df.loc[(df['total_callback_messages'] >= 1), 'callback_binary'] = 1
	df.loc[(df['total_reply_messages'] >= 1), 'reply_binary'] = 1
	df.loc[(df['total_reponse_messages'] >= 1), 'response_binary'] = 1


	#Clean and Lower Column Names
	old_cols = df.columns.tolist()
	new_cols = [clean_cols(c) for c in old_cols]
	df.columns = new_cols

	#Fill NAN Values with 0
	df = df.fillna(0)


	df=df.reset_index()
	df.to_csv('appid_level_mbox_results.csv', index=False)

	return df


#if __name__ == '__main__':

	#mb = make_detailed_outcomes(mb)
	#mb = spread_outcomes_sum(mb)

#	print(mb)

