import pandas as pd
import re


def get_domain(email, simple=True):

	domain_base = email.split('@')[1]
	dot_count = domain_base.count('.')
	max_split = dot_count - 1

	if simple is True:
		if dot_count > 1:
			domain = domain_base.split('.', max_split)[-1]
			return domain
		else:
			return domain_base
	else:
		return domain_base


def remove_punct(text):
	tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', "", text)
	return re.sub(r'\s{2,}', "", tmp)


def possible_mismatch(row):
	company = row['company'].lower().replace(' ', '')
	company = remove_punct(company)

	domain = row['domain'].lower().split('.')[0]
	domain = remove_punct(domain)

	return domain not in company 

#Import Waves and Add Wave

def compare_protocol_waves(w1_file, w2_file):

	#First Wave
	w1 = pd.read_csv(w1_file)
	w1['wave'] = 'wave1'
	w1['timestamp'] = w1_file.split('experiment_')[1].split('.csv')[0]
	w1['domain'] = w1['contact_email'].apply(get_domain)
	w1['full_domain'] = w1['contact_email'].apply(get_domain, simple=False)

	#Second Wave
	w2 = pd.read_csv(w2_file)
	w2['wave'] = 'wave2'
	w2['timestamp'] = w2_file.split('experiment_')[1].split('.csv')[0]
	w2['domain'] = w2['contact_email'].apply(get_domain)
	w2['full_domain'] = w2['contact_email'].apply(get_domain, simple=False)

	#Append Waves
	df = pd.concat([w1, w2], axis=0)


	#Get Counts Email
	gb = ['contact_email']
	sm = 'contact_email'
	df['count_email'] = df.groupby(gb)[sm].transform('count')


	#Get Counts Domain
	gb = ['domain']
	sm = 'domain'
	df['count_domain'] = df.groupby(gb)[sm].transform('count')


	#Get Counts Full Domain
	gb = ['full_domain']
	sm = 'full_domain'
	df['count_full_domain'] = df.groupby(gb)[sm].transform('count')

	#Add Domain Flag
	df['mismatch'] = df.apply(possible_mismatch, axis=1)

	#Sort
	df = df.sort_values(['count_domain', 'full_domain', 
						 'count_email', 'mismatch'], ascending=False)
	df.to_csv('compare_protocol_waves.csv', index=False)
	print(df)



def check_single_protocol(df_file):

	#First Wave
	df = pd.read_csv(df_file)
	df['timestamp'] = df_file.split('experiment_')[1].split('.csv')[0]
	df['domain'] = df['contact_email'].apply(get_domain)
	df['full_domain'] = df['contact_email'].apply(get_domain, simple=False)

	#Get Counts Email
	gb = ['contact_email']
	sm = 'contact_email'
	df['count_email'] = df.groupby(gb)[sm].transform('count')


	#Get Counts Domain
	gb = ['domain']
	sm = 'domain'
	df['count_domain'] = df.groupby(gb)[sm].transform('count')


	#Get Counts Full Domain
	gb = ['full_domain']
	sm = 'full_domain'
	df['count_full_domain'] = df.groupby(gb)[sm].transform('count')

	#Add Domain Flag
	df['mismatch'] = df.apply(possible_mismatch, axis=1)

	#Sort
	df = df.sort_values(['count_domain', 'full_domain', 
						 'count_email', 'mismatch'], ascending=False)
	df.to_csv('compare_single_protocol.csv', index=False)
	print(df)





w1 = "../protocols/experiment_2019-04-02-001439.csv"
w2 = "../protocols/experiment_2019-04-23-014656.csv"
compare_protocol_waves(w1, w2)

#TODO Consider Reclassing All Those In a Single Protocol
#with full_domain >=4 & mismatch = True as a bounce / error
#from fuzzy matching error, wrong company
#check_single_protocol(w2)