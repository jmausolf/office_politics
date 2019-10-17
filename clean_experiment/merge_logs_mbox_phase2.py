import pandas as pd



## Phase 2: Take MBOX Data Linked to App ID's and spread into new columns
##(for response type: direct, third-party reply, phone reply)

#Mail Box Linked Index Applicant Id Wave
mb = pd.read_csv('found_appid_deduped.csv')
print(mb.columns)
#print(mb)

#mbla = pd.read_csv('found_appid_deduped.csv')
#print(mbla)
#Make Detailed Outcome Column
mbla = mb[[	'index_wave', 'message', 'outcome', 'from_full_domain', 'merge_match_type', 'linkage']]
mbla.to_csv("phase2_test.csv", index=False)


def get_reply_types_bool(df):

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

	df.loc[der_crit, 'direct_email_reply'] = True


	#Other Email Reply
	oer_crit = (
					(
						(df['merge_match_type'] == 'domain_match') &
						(df['outcome'].isin(['Callback', 'Reply']))
					) |

					(
						(df['merge_match_type'] == 'verified_linkage_full_email_match') &
						(df['outcome'].isin(['Callback', 'Reply'])) &
						(df['from_full_domain'] != 'grasshopper.com' )
					)

				)

	df.loc[oer_crit, 'other_email_reply'] = True


	#Phone (Voicemail) Reply
	pr_crit = (df['from_full_domain'] == 'grasshopper.com' )
	df.loc[pr_crit, 'phone_reply'] = True
	

	#Any Reply
	ar_crit = (
					(
						(df['direct_email_reply'] == True ) |
						(df['other_email_reply'] == True ) |
						(df['phone_reply'] == True ) 
					) 

				)
	df['any_reply'] = False
	df.loc[ar_crit, 'any_reply'] = True
	print(df)
	return df.copy()

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
						(df['merge_match_type'] == 'domain_match') &
						(df['outcome'].isin(['Callback', 'Reply']))
					) |

					(
						(df['merge_match_type'] == 'verified_linkage_full_email_match') &
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



#df.loc[(df['isprofile'] == True), 'missing_email'] = None
#mbla_bool = get_reply_types_bool(mbla)
mbla = get_reply_types_str(mbla)
mbla['outcome'] = mbla['outcome'].str.upper()
reply_cols = ['direct_email_reply', 'other_email_reply', 'phone_reply']

mbla['reply_type'] = mbla[reply_cols].apply(lambda x: ''.join(x.values.astype(str)), axis=1)
#mbla['outcome_detailed'] = mbla['outcome']+'-'+mbla['reply_type']
mbla['outcome_detailed'] = mbla.apply(join_reply_types, axis=1)
#mbla = mbla.groupby(['index_wave', 'outcome_detailed']).agg(['count'])
mbla = mbla.groupby(['index_wave', 'outcome_detailed']).size().reset_index(name='count')


print(mbla.shape)
print(mbla)
#mbla['direct_email_reply'] = 


mbla.to_csv("phase2_test.csv", index=False)

#Keep Key MBOX Columns
#mbla = mb[[	'index_wave', 'message', 'outcome']]
#print(mbla.shape)

#Strat
#Don't need all the rich data, message cols for quant analysis
#If you want to pull quotes or anything else, go back to the mbox data later
#Not needed for now

#Strat 2
#Let's get metric cols for more specific results and their counts
#outcome is the overall index_wave level result
#need a categorical outcome column at the index_wave level
#want another column for response types (for callbacks)
#direct reply, other reply, phone reply with counts
#and total message count



#Get Overall Outcome at Index_Wave (App ID) Level
#mbo = mbla.drop_duplicates(subset=['index_wave', 'outcome'])
#mbo = mbla.drop_duplicates(subset=['index_wave'])
#print(mbo.shape)
#mbo.to_csv("phase2_dupes_test.csv")


#Keep Key MBOX Columns
#mbla = mbla[[	'index_wave', 'outcome_detailed', 'outcome_count']]

#mbla = mb[[	'index_wave', 'mb_id', 'date', 
#			'from_email', 'from_email_clean', 'to_email', 'mbox_email',  
#			'subject', 'labels', 'message', 'message_id', 
#			'mbox', 'profile', 'outcome']]

#print(mbla)

#TODO Add Response Type Column
#(e.g. grasshopper, email, etc)

#Work on Pivoting Data / Spread

#df=pd.pivot_table(mbla,index='index_wave',columns='outcome',values='message')


#df = mbla.pivot_table(index=['index_wave'],
#                                     columns='outcome', 
#                                     values='message',
#                                     aggfunc=lambda x: ' '.join(x))

df = mbla.pivot_table(index=['index_wave'],
                                     columns='outcome_detailed', 
                                     values='count')
                                     #aggfunc=lambda x: ' '.join(x))


print(df.shape)
print(df.columns)
print(df)


df=df.reset_index()
#print(df)
#print(df.columns)
df.to_csv('test_pivot.csv', index=False)


