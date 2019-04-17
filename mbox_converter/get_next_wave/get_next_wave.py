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


def get_domain(email):

	domain_base = email.split('@')[1]
	dot_count = domain_base.count('.')
	max_split = dot_count - 1

	if dot_count > 1:
		domain = domain_base.split('.', max_split)[-1]
		return domain
	else:
		return domain_base


def prepare_emails(protocol_file, bounces_file):

	#Prepare Protocol
	df_p = pd.read_csv(protocol_file)
	df_p = df_p.drop_duplicates(['contact_email'])
	df_p['contact_email'] = df_p['contact_email'].str.lower()
	df_p['domain'] = df_p['contact_email'].apply(get_domain)
	print(df_p)

	#Prepare Bounces
	df_b = pd.read_csv(bounces_file)
	df_b['contact_email'] = df_b['bounce_email'].str.lower()
	df_b['domain'] = df_b['contact_email'].apply(get_domain)
	print(df_b)

	return df_p, df_b



#Prepare Protocol and Bounces for Join
protocol_file = "protocol_experiment_2019-04-02-001439.csv"
bounces_file = "bounce_emails_W1.csv"
base_protocol, bounces = prepare_emails(protocol_file, bounces_file)

#Get Successful Emails
successful_emails = anti_join(base_protocol, bounces, 'domain')
successful_emails.to_csv('successful_emails_W1.csv', index=False)
print(successful_emails)

#Get Failed Emails
failed_emails = anti_join(base_protocol, successful_emails, 'contact_email')
failed_emails.to_csv('failed_emails_W1.csv', index=False)
#print(failed_emails)

#Bounces Not Explicitly Found
unfound_bounces = anti_join(bounces, failed_emails, 'domain')
#print(unfound_bounces)




########################################################
## Step Two: Remove Successful Emails from Master CID
## (Antijoin Successful Emails and Master CID)
########################################################


master_cid_file = "master_companies_W1.csv"
master_cid = pd.read_csv(master_cid_file)
print(master_cid.shape)

new_master_cid = anti_join(master_cid, successful_emails, 'list_id')
print(new_master_cid)
new_master_cid.to_csv('master_companies_W2.csv')

#top_priority_cid = master_cid.merge(failed_emails, how='inner', on='list_id')
#print(top_priority_cid)
