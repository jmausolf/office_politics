import pandas as pd
import re

#####################################################
## Define Experiment Wave Pairs Dictionary
## (results files created from matched output during experiments)
#####################################################

wave_pairs = {
	
	#Experiment Wave 1
	'w1_A1' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_A.csv',
	'w1_B1' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_B.csv',
	'w1_B2' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_P05RH_select_resend_results_pair_B.csv', 

	#Experiment Wave 2
	'w2_A1' : '../logs/2019-04-23-093407_protocol_experiment_2019-04-23-014656_results_pair_A.csv', 
	'w2_B1' : '../logs/2019-04-23-093407_protocol_experiment_2019-04-23-014656_results_pair_B.csv', 


}


#####################################################
# Base Functions
#####################################################

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


def make_id(row):
	index = row['index']
	return index_to_n(index)


def make_pair_id(row):

	#Get App Index from Pair Number
	i = row['id_index']
	i = int(i.split('n')[1])

	#Get Wave, Add Fixed N to W2 i?
	w = row['wave']

	#Get Max Id
	m = row['max_id_index']
	m = int(m.split('n')[1])

	#Extend I in Wave 2
	if w == 'W1':
		i = i

	elif w == 'W2':
		i = i+m

	#Make Pairs
	if i % 2 == 1:
		s = (i+1)/2
		i = int(s)
	elif i % 2 == 0:
		s = i/2
		i = int(i-s)

	letter = 'P'

	#Return as String
	if i < 10:
		return letter+'000'+str(i)
	elif i < 100:
		return letter+'00'+str(i)
	elif i < 1000:
		return letter+'0'+str(i)
	else:
		return letter+str(i)


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


def get_user(email):
	user = email.split('@')[0]
	return user


def remove_punct(text):
	tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', "", text)
	return re.sub(r'\s{2,}', "", tmp)


def possible_mismatch(row):
	company = row['company'].lower().replace(' ', '')
	company = remove_punct(company)

	domain = row['domain'].lower().split('.')[0]
	domain = remove_punct(domain)

	return domain not in company 



#####################################################
# Step 1: Combine Matched Output/Result Files
#####################################################

def prep_results(results_file, wave_pair):
	'''
	results_file :: a results log file for one matched pair,
		e.g. logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_A.csv

	wave_pair :: specify the wave-pair of the results, e.g. w1, w2, 
	'''

	#Read Results for Wave-Pair
	r = pd.read_csv(results_file)

	#Convert the Index to a Sortable Wave Index to Sort by Pair and Wave
	r['id_index'] = r.apply(make_id, axis=1)
	r['wave_pair'] = wave_pair.upper()
	r['wave'] = wave_pair.split('_')[0].upper()
	r['index_wave'] = r['wave'] + '_' + r['id_index']
	r['index_wave'] = r['index_wave'].str.upper()

	#Ensure Emails Lowercase
	r['contact_email'] = r['contact_email'].str.lower()

	#Add Other Data
	r['protocol_ts'] = results_file.split('experiment_')[1].split('_')[0]
	r['output_ts'] = results_file.split('_protocol')[0].split('logs/')[1]

	#Add Contact Domain and User
	r['contact_domain'] = r['contact_email'].apply(get_domain)
	r['contact_full_domain'] = r['contact_email'].apply(get_domain, simple=False)
	r['contact_user'] = r['contact_email'].apply(get_user)

	#TODO add email user, e.g. something@domain
	return r



def combine_result_files(wave_pairs):

	results_dfs = [prep_results(f, wp) for wp, f in wave_pairs.items()]
	results = pd.concat(results_dfs, axis=0).reset_index(drop=True)

	#Sort and Save Combined File
	results.sort_values(by=['index_wave', 'wave_pair'], inplace=True)
	results.to_csv("complete_experimental_wave_results.csv", index=False)	

	#TODO add pair id
	results = results.rename(columns={'index':'wave_index'})
	results = results.reset_index(drop=True)
	results = results.reset_index(drop=True)
	#results['index'] = results['index'] + 1

	#Add N Max Column
	results['max_id_index'] = results['id_index'].max()

	#Add Pair ID
	results['pair_index'] = results.apply(make_pair_id, axis=1)

	#Drop Max ID Col
	results = results.drop(columns=['max_id_index'])

	return results


df = combine_result_files(wave_pairs)


#####################################################
# Step 2: Additional Cleaning
#####################################################

def clean_results(df):

	#Keep Only Sent Emails (Drop Errors)
	print(df.shape)
	df = df.loc[df['metadata'].str.contains('metadata::')]
	print(df.shape)

	#Remove Gmail Spam/Reject Errors That Appeared to Send
	#These Were Sent Again From Alt Email in W1_B2
	tmp = df.groupby(['pair_index']).agg({'gmail_user':['count']})
	tmp = pd.DataFrame(tmp.to_records())
	tmp.columns = ['pair_index', 'pair_index_count']
	df = df.merge(tmp)

	#Keep Criteria
	keep_crit = (
					( 	df['pair_index_count'] == 2 ) |
					(
						(df['pair_index_count'] > 2 ) &
						(df['wave_pair'] != 'W1_B1') 
					)

				)
	df = df.loc[keep_crit]

	df.to_csv("cleaned_experimental_wave_results.csv", index=False)
	print(df)

clean_results(df)

