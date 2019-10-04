import pandas as pd
import re

## Define Experiment Wave Pairs Dictionary
## (results files created from matched output during experiments)


wave_pairs = {
	
	#Experiment Wave 1
	'w1_A1' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_A.csv',
	'w1_B1' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_B.csv',
	'w1_B2' : '../logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_P05RH_select_resend_results_pair_B.csv', 

	#Experiment Wave 2
	'w2_A1' : '../logs/2019-04-23-093407_protocol_experiment_2019-04-23-014656_results_pair_A.csv', 
	'w2_B1' : '../logs/2019-04-23-093407_protocol_experiment_2019-04-23-014656_results_pair_B.csv', 


}

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


## Base Functions 

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


## Misc 

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



# Step 1: Combine Matched Output Cols with A/B Results
#not needed, the results is the same as output but with a metadata col

# Step 2: Combine Matched Output/Result Files

def prep_results(results_file, wave_pair):
	'''
	results_file :: a results log file for one matched pair,
		e.g. logs/2019-04-02-100810_protocol_experiment_2019-04-02-001439_results_pair_A.csv

	wave_pair :: specify the wave-pair of the results, e.g. w1, w2, 
	'''

	#Read Results for Wave-Pair
	r = pd.read_csv(results_file)

	#Convert the Index to a Sortable Wave Index to Sort by Pair and Wave
	r['index'] = r.apply(make_id, axis=1)
	r['wave_pair'] = wave_pair
	r['wave'] = wave_pair.split('_')[0]
	r['index_wave'] = r['wave'] + '_' + r['index'] 

	#Add Other Data
	r['protocol_ts'] = results_file.split('experiment_')[1].split('_')[0]
	r['output_ts'] = results_file.split('_protocol')[0].split('logs/')[1]
	r['domain'] = r['contact_email'].apply(get_domain)
	r['full_domain'] = r['contact_email'].apply(get_domain, simple=False)

	return r



def combine_result_files(wave_pairs):

	results_dfs = [prep_results(f, wp) for wp, f in wave_pairs.items()]
	results = pd.concat(results_dfs, axis=0).reset_index(drop=True)

	#Sort and Save Combined File
	results.sort_values(by=['index_wave', 'wave_pair'], inplace=True)
	results.to_csv("complete_experimental_wave_results.csv", index=False)	

	print(results.columns)
	print(results)
	return results


df = combine_result_files(wave_pairs)


# Step 3: Additional Cleaning

## keep only the non-error results (these emails never sent on gmail side)
#df.loc[df['metadata'].str.contains]

def clean_results(df):

	print(df.shape)
	df = df.loc[df['metadata'].str.contains('metadata::')]
	print(df.shape)

	df.to_csv("cleaned_experimental_wave_results.csv", index=False)

clean_results(df)

#Import Waves and Add Wave



#TODO Consider Reclassing All Those In a Single Protocol
#with full_domain >=4 & mismatch = True as a bounce / error
#from fuzzy matching error, wrong company
#check_single_protocol(w2)

#TODO remove possible accidental resends
#that occur from a dupe in the master_cid_csv
#that had a successfull send
#but reappear in W2 from a match on the dupe cid_master
#under a different email address
#so those companies that may have been send a w2 when they received a w1
#find by isolating unique w1 successful domains join w2 domains and drop the matches 
#from w2 results?