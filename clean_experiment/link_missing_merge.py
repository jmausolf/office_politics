import pandas as pd
import re
from profile_dict import *
from link_bounce_merge import *



def extract_email(message):
	try:
		match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z]+\.[a-zA-Z]+)", message)
		#match = re.search(r'[\w\.-]+@[\w\.-]+', message)
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


#Load Data
def load_bounce_data():

	#Step 0: Load Data
	mb = pd.read_csv("missing_emails.csv")
	ex = pd.read_csv("cleaned_experimental_wave_results.csv")
	print(mb.shape)

	#Drop Grasshopper Voicemails 
	mb = mb.loc[~mb['from_email'].str.contains('grasshopper')]
	print(mb.shape)

	return mb, ex




#Extract Bounce Emails
def link_missing_merge(df):

	#Get Bounces DF
	df['missing_email'] = df['message'].apply(extract_email)

	#Need to Overwrite Emails Mataching Prior Link Efforts
	#Search Using Other Methods
	df['isprofile'] = df['missing_email'].apply(isprofile)
	df.loc[(df['isprofile'] == True), 'missing_email'] = None
	df.loc[(df['missing_email'] == df['extracted_email']), 'missing_email'] = None
	df.loc[(df['missing_email'] == df['from_email_clean']), 'missing_email'] = None


	#Still Missing, Found
	df_m = df.loc[df['missing_email'].isna()]
	df1 = df.dropna(subset=['missing_email'])

	#Lookup Missing Emails Using Extracted Full Names
	df2 = df_m.copy()
	df2['missing_email'] = df2.apply(ret_email_full_name, axis=1)

	#Still Missing, Found
	df_m = df2.loc[df2['missing_email'].isna()]
	df2 = df2.dropna(subset=['missing_email'])

	#Backfill Bounces Sent to Incorrect (but valid addresses)
	df3 = df_m.copy()
	df3['missing_email'] = df3.apply(fill_bounce_email_legit, axis=1)

	#Still Missing, Found
	df_m = df3.loc[df3['missing_email'].isna()]
	df3 = df3.dropna(subset=['missing_email'])

	#Try Looking Up Using From Domain and To Email
	df4 = df_m.copy()
	df4['missing_email'] = df4.apply(ret_email_domain, axis=1)

	#Still Missing, Found
	df_m = df4.loc[df4['missing_email'].isna()]
	df4 = df4.dropna(subset=['missing_email'])
	print(df_m.shape)

	#Try Looking Up Using Company and To Email
	df5 = df_m.copy()
	df5['missing_email'] = df5.apply(ret_email_company, axis=1)

	#Still Missing, Found
	df_m = df5.loc[df5['missing_email'].isna()]
	df5 = df5.dropna(subset=['missing_email'])
	print(df_m.shape)

	#Bounces All
	dfb = pd.concat([df1, df2, df3, df4, df5, df_m])
	dfb['isprofile'] = dfb['missing_email'].apply(isprofile)

	dfb.to_csv("linked_missing_emails.csv", index=False)
	print(dfb.shape)
	print(dfb.columns)


	#Some 15 are still left, just manually code them
	#before finding these, try merging with the other code base

	#see if bounces appear in found id's, if so, drop pair or no?


#print(ex.columns)

if __name__=='__main__':
	mb, ex = load_bounce_data()
	link_missing_merge(mb)
	


