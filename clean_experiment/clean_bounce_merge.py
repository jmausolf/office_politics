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
		match = re.search(r"Dear\s[\w'\-,.][^0-9_!¡?÷?¿\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}\:", message)
		salutation = match.group(0)
		full_name = salutation.split('Dear ')[1].split(':')[0]
		first_name = full_name.split(' ')[0]
		last_name = full_name.split(' ')[1]

	except:
		full_name = None
		first_name = None
		last_name = None

	contact_email = lookup_email_fn(first_name, last_name, to_email, ex)
	return contact_email


def lookup_email_fn(first, last, to_email, df):

	crit = (
				(df['contact_name'] == first) &
				(df['contact_last_name'] == last) &
				(df['gmail_user'] == to_email)

			)

	df = df.loc[crit].copy()
	if df.shape[0] >= 1:
		c = df['contact_email'].values[0]
	else:
		c = None
	return c


def ret_email_company(row):

	message = row['message']
	to_email = row['to_email']

	try:
		match = re.search(r"(?<=opportunity at )(.*)(?= and)", message)
		company = match.group(0)
	except:
		company = None

	contact_email = lookup_email_company(company, to_email, ex)
	return contact_email


def lookup_email_company(company, to_email, df):

	if company is None:
		return None
	else:
		crit = (
					(
						(df['company'] == company) |
						(df['company'].str.contains(company))
					) &

					(df['gmail_user'] == to_email)

				)

		df = df.loc[crit].copy()
		if df.shape[0] >= 1:
			c = df['contact_email'].values[0]
		else:
			c = None
		return c


def ret_email_domain(row):

	from_domain = row['from_domain']
	to_email = row['to_email']

	contact_email = lookup_email_domain(from_domain, to_email, ex)
	return contact_email


def lookup_email_domain(from_domain, to_email, df):

	crit = (
				(
					(df['contact_full_domain'] == from_domain) |
					(df['contact_domain'] == from_domain)
				) &

				(df['gmail_user'] == to_email)

			)

	df = df.loc[crit].copy()
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

	#Need to Overwrite Profile Emails with None, Search Using Other Methods
	df['isprofile'] = df['extracted_email'].apply(isprofile)
	df.loc[(df['isprofile'] == True), 'extracted_email'] = None

	#Still Missing, Found
	df_m = df.loc[df['extracted_email'].isna()]
	df1 = df.dropna(subset=['extracted_email'])

	#Lookup Missing Emails Using Extracted Full Names
	df2 = df_m.copy()
	df2['extracted_email'] = df2.apply(ret_email_full_name, axis=1)

	#Still Missing, Found
	df_m = df2.loc[df2['extracted_email'].isna()]
	df2 = df2.dropna(subset=['extracted_email'])

	#Backfill Bounces Sent to Incorrect (but valid addresses)
	df3 = df_m.copy()
	df3['extracted_email'] = df3.apply(fill_bounce_email_legit, axis=1)

	#Still Missing, Found
	df_m = df3.loc[df3['extracted_email'].isna()]
	df3 = df3.dropna(subset=['extracted_email'])

	#Try Looking Up Using From Domain and To Email
	df4 = df_m.copy()
	df4['extracted_email'] = df4.apply(ret_email_domain, axis=1)

	#Still Missing, Found
	df_m = df4.loc[df4['extracted_email'].isna()]
	df4 = df4.dropna(subset=['extracted_email'])
	print(df_m.shape)

	#Try Looking Up Using Company and To Email
	df5 = df_m.copy()
	df5['extracted_email'] = df5.apply(ret_email_company, axis=1)

	#Still Missing, Found
	df_m = df5.loc[df5['extracted_email'].isna()]
	df5 = df5.dropna(subset=['extracted_email'])
	print(df_m.shape)

	#Bounces All
	dfb = pd.concat([df1, df2, df3, df4, df5, df_m])
	dfb['isprofile'] = dfb['extracted_email'].apply(isprofile)

	dfb.to_csv("extracted_bounce_emails.csv")
	print(dfb.shape)
	#print(dfb.columns)


	#Some 15 are still left, just manually code them
	#before finding these, try merging with the other code base

	#see if bounces appear in found id's, if so, drop pair or no?

filter_bounces_merge(mb)
#print(ex.columns)



