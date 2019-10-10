import pandas as pd
import re
from profile_dict import *


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



#Step 0: Load Data
mb = pd.read_csv("mbox_analysis.csv")
ex = pd.read_csv("cleaned_experimental_wave_results.csv")

# Add MB Index
mb = mb.reset_index()
mb['mb_id'] = mb.apply(make_id, prefix='MB_', axis=1)
mb = mb.drop(columns=['wave'])

#Goals of this file
#1. isolate true bounces / other (other has grasshopper and some bounce)
#2. extract email from bounce to merge
#3. drop mbox id's with these features


#Isolate Bounces
mb = mb.loc[mb['outcome'].isin(['Bounce', 'Other'])]
#print(mb.shape)

#Drop Grasshopper Voicemails 
mb = mb.loc[~mb['from_email'].str.contains('grasshopper')]
print(mb.shape)
#print(mb)

def extract_email(message):
	try:
		match = re.search(r'[\w\.-]+@[\w\.-]+', message)
		email = match.group(0)
	except:
		email = None

	if email is not None:
		if email[-1:] == '.':
			email = email[:-1]
		else:
			pass
		#print(email)
		#print(email[-1:])

	return email


def isprofile(email):

	if email in profile_emails:
		return True
	else:
		return False


def ret_email_full_name(row):

	message = row['message']
	to_email = row['to_email']

	try:
		#match = re.search(r'Dear\s\w+\s+\w+\:', message)
		match = re.search(r"Dear\s[\w'\-,.][^0-9_!¡?÷?¿\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}\:", message)
		salutation = match.group(0)
		full_name = salutation.split('Dear ')[1].split(':')[0]
		first_name = full_name.split(' ')[0]
		last_name = full_name.split(' ')[1]

	except:
		full_name = None
		first_name = None
		last_name = None

		
	#print(full_name)
	contact_email = lookup_email_fn(first_name, last_name, to_email, ex)
	return contact_email

	#print(full_name, first_name)

def lookup_email_fn(first, last, to_email, df):


	#print(first, last, to_email)
	crit = (
				(df['contact_name'] == first) &
				(df['contact_last_name'] == last) &
				(df['gmail_user'] == to_email)

			)



	df = df.loc[crit].copy()
	if df.shape[0] >= 1:
		c = df['contact_email'].values[0]
		#print(c)
	else:
		c = None
	#return df['contact_email']
	#print(df)
	return c


def ret_email_domain(row):

	from_domain = row['from_domain']
	to_email = row['to_email']

	contact_email = lookup_email_domain(from_domain, to_email, ex)
	return contact_email


def lookup_email_domain(from_domain, to_email, df):

	print(from_domain, to_email)
	crit = (
				(
					(df['contact_full_domain'] == from_domain) |
					(df['contact_domain'] == from_domain)
				) &

				(df['gmail_user'] == to_email)

			)

	df = df.loc[crit].copy()
	print(df)
	if df.shape[0] >= 1:
		c = df['contact_email'].values[0]
	else:
		c = None
	return c




def fill_bounce_email_legit(row):

	from_user = row['from_user']
	email = row['from_email_clean']

	blist = ['mailer-daemon', 'noreply', 'no-reply', 
			 'postmaster', 'emailsecurity', 'nobody']
	if from_user not in blist:
		return email
	else:
		return None





#Extract Bounce Emails
def filter_bounces_merge(df):

	#Get Bounces DF
	df['extracted_email'] = df['message'].apply(extract_email)
	#print(df)

	#Still Missing
	df_m = df.loc[df['extracted_email'].isna()]

	#Found Emails
	df1 = df.dropna(subset=['extracted_email'])
	print(df1.shape)


	#Lookup Missing Emails Using Extracted Full Names
	df2 = df_m.copy()
	df2['extracted_email'] = df2.apply(ret_email_full_name, axis=1)
	#print(df2)
	print(df2.shape)

	#Still Missing
	df_m = df2.loc[df2['extracted_email'].isna()]
	print(df_m.shape)

	#Found Emails
	df2 = df2.dropna(subset=['extracted_email'])

	#Backfill Bounces Sent to Incorrect (but valid addresses)
	df3 = df_m.copy()
	df3['extracted_email'] = df3.apply(fill_bounce_email_legit, axis=1)

	#Still Missing
	df_m = df3.loc[df3['extracted_email'].isna()]
	print(df_m.shape)

	#Found Emails
	df3 = df3.dropna(subset=['extracted_email'])

	#Try Looking Up Using From Domain and To Email
	df4 = df_m.copy()
	print(df4.columns)
	df4['extracted_email'] = df4.apply(ret_email_domain, axis=1)

	#Still Missing
	df_m = df4.loc[df4['extracted_email'].isna()]
	print(df_m.shape)

	#Found Emails
	df4 = df4.dropna(subset=['extracted_email'])


	#Bounces All
	dfb = pd.concat([df1, df2, df3, df4, df_m])
	dfb['isprofile'] = dfb['extracted_email'].apply(isprofile)

	dfb.to_csv("bounce_test2.csv")
	print(dfb.shape)
	print(dfb.columns)


	#Some 15 are still left, just manually code them


filter_bounces_merge(mb)
print(ex.columns)



