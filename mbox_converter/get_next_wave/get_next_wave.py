import pandas as pd


def anti_join(df_A, df_B, key):

	set_diff = set(df_A[key]).difference(df_B[key])
	bool_diff = df_A[key].isin(set_diff)
	df_diff = df_A.loc[bool_diff]

	return df_diff



########################################################
## Step One: ID Successful Emails from Base Protocol
## (Antijoin Deduped Protocol and Bounces)
########################################################


base_protocol = pd.read_csv("protocol_experiment_2019-04-02-001439.csv")
base_protocol = base_protocol.drop_duplicates(['contact_email'])
print(base_protocol)

bounces = pd.read_csv("bounce_emails_W1.csv")
bounces.columns = ['contact_email', 'count']
#bounces['contact_email'] = bounces['bounce_email']
#print(bounces)

successful_emails = anti_join(base_protocol, bounces, 'contact_email')
print(successful_emails)

failed_emails = bounces.merge(base_protocol, on = 'contact_email')
print(failed_emails)

unfound_bounces = anti_join(bounces, failed_emails, 'contact_email')
print(unfound_bounces)

##Try to lowercase all emails before joining

##Try to split on domain to match that way @apple.com

########################################################
## Step Two: Remove Successful Emails from Master CID
## (Antijoin Successful Emails and Master CID)
########################################################

