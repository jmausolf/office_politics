import random
import pandas as pd
import numpy as np
#from new_messages import *
import textwrap
import inspect
import textile
import re
from make_cover_letters import *
from send_email import *
import pdb
import time
import sys



def join_profiles_credentials():
	cred = pd.read_csv("keys/credentials.csv")
	prof = pd.read_csv("keys/profiles.csv")

	df = pd.merge(cred, prof, on=['profile'])
	return df


def ret_mba_treatment(row, infile='keys/mba_treatment_key.csv'):
	ga_sid = row['ga_sid']
	profile = row['profile']
	job_type = row['job_type']
	ug_treatment = row['treatment']

	if job_type not in ['mba', 'mba_finance', 'consultant']:
		return ug_treatment
	else:

		df = pd.read_csv(infile)
		crit = (	(df['ga_sid'] == ga_sid) &
					(df['profile'] == profile)
				)
		treatment = df.loc[crit]['mba_treatment'].tolist()[0]
		return treatment


def update_treatment_leadership(row):
	base_treatment = row['treatment']
	leadership = row['leadership']
	updated_treatment = base_treatment.replace('president', leadership)
	return updated_treatment


def select_ga(row, count):
	profile = row[0]
	job_type = row[1]
	region = row[2]
	proximal = row[3]

	#First Matched Pair
	if count == 0:
		#Select Match from Region or Proximal Region
		gaf = pd.read_csv("keys/ga_school_key.csv")

		criteria_base = ( (gaf['region']==region) & 
						(gaf['job_type']==job_type) & 					
						(gaf['prestige']==profile[-1]) )

		criteria_prox = (((gaf['region']==region) |
						  (gaf['region']==proximal)) & 
						(gaf['job_type']==job_type) & 					
						(gaf['prestige']==profile[-1]))

		#TODO
		#FIX BUG WITH ga prox selection
		#e.g. midwest == region
		try:
			ga = gaf.loc[criteria_base].copy()
			if ga.shape[0] == 0:
				ga = gaf.loc[criteria_prox].copy()
			else: 
				pass
		except:
			ga = gaf.loc[criteria_prox].copy()

		#Add Pair Label
		ga['matched_pair'] = 'A'

		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(ga.index.values, 1)
		df = ga.ix[rows]

		#Drop Selection from GA to Avoid Selection for Pair 2
		ga_selection = df['ga_sid'].values.tolist()[0]
		tmp = gaf[gaf.ga_sid != ga_selection]
		tmp.to_csv("keys/ga_school_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['region', 'job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()[0]
		return vals


	#Second Matched Pair
	elif count == 1:
		#Select Match from Region or Proximal Region
		gaf = pd.read_csv("keys/ga_school_key_tmp.csv")
		criteria_base = ( (gaf['region']==region) & 
						(gaf['job_type']==job_type) & 					
						(gaf['prestige']==profile[-1]) )

		criteria_prox = (((gaf['region']==region) |
						  (gaf['region']==proximal)) & 
						(gaf['job_type']==job_type) & 					
						(gaf['prestige']==profile[-1]))

		try:
			ga = gaf.loc[criteria_base].copy()
			if ga.shape[0] == 0:
				print("no ga result found, trying proximal region")
				ga = gaf.loc[criteria_prox].copy()
			else: 
				pass
		except:
			print("no ga result found, trying proximal region")
			ga = gaf.loc[criteria_prox].copy()

		#Add Pair Label
		ga['matched_pair'] = 'B' 

		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(ga.index.values, 1)
		df = ga.ix[rows]

		#Return Results
		df = df.drop(['region', 'job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()[0]
		return vals

	else:
		pass



def select_ug(row, count):

	profile = row[0]
	region = row[1]
	school = row[2]

	#First Matched Pair
	if count == 0:
		ugf = pd.read_csv("keys/ug_school_key.csv")
		criteria = ((ugf['profile']==profile) & 
					(ugf['region']==region) & 
					(ugf['sid']!=school))
		ug = ugf.loc[criteria] 
		
		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(ug.index.values, 1)
		df = ug.ix[rows]

		#Drop Selection from UG to Avoid Selection for Pair 2
		ug_selection = df['ug_sid'].values.tolist()[0]
		tmp = ugf[ugf.ug_sid != ug_selection]
		tmp.to_csv("keys/ug_school_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['region', 'profile', 'sid'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()[0]
		return vals


	#Second Matched Pair
	elif count == 1:
		ugf = pd.read_csv("keys/ug_school_key_tmp.csv")
		criteria = ((ugf['profile']==profile) & 
					(ugf['region']==region) & 
					(ugf['sid']!=school))
		ug = ugf.loc[criteria]
		
		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(ug.index.values, 1)
		df = ug.ix[rows]

		#Return Results
		df = df.drop(['region', 'profile', 'sid'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()[0]
		return vals		

	else:
		pass


def internships_general(job_type, prestige, company, count):

	#First Matched Pair
	if count == 0:
		intf = pd.read_csv("keys/int_key.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria] 
		
		#Random Selection of Internships Meeting Criteria
		rows = np.random.choice(int_df.index.values, 2, replace=False)
		df = int_df.ix[rows]
		#Drop Selections from Internship to Avoid Selection for Pair 2
		int_selection = df['int_id'].values.tolist()
		tmp = intf[((intf.int_id != int_selection[0]) &
				    (intf.int_id != int_selection[1]))]
		tmp.to_csv("keys/int_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships


	#Second Matched Pair
	elif count == 1:
		intf = pd.read_csv("keys/int_key_tmp.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria] 
		
		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(int_df.index.values, 2, replace=False)
		df = int_df.ix[rows]


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships	

	else:
		pass


def internships_mba(job_type, prestige, company, count):

	#First Matched Pair
	if count == 0:
		intf = pd.read_csv("keys/int_key.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria] 
		
		#Random Selection of Internships Meeting Criteria
		rows = np.random.choice(int_df.index.values, 2, replace=False)
		df = int_df.ix[rows]
		#Drop Selections from Internship to Avoid Selection for Pair 2
		int_selection = df['int_id'].values.tolist()
		tmp = intf[((intf.int_id != int_selection[0]) &
				    (intf.int_id != int_selection[1]))]
		tmp.to_csv("keys/int_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships


	#Second Matched Pair
	elif count == 1:
		intf = pd.read_csv("keys/int_key_tmp.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria] 
		
		#Random Selection of Schools Meeting Criteria
		rows = np.random.choice(int_df.index.values, 2, replace=False)
		df = int_df.ix[rows]


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships	

	else:
		pass


def internships_consultant(job_type, prestige, company, count):
	'''
	Selects a consulting company as the 'first' or most recent 
	work experience. Selects a non-consulting firm as the 'second'
	or pre-MBA work experience.
	'''

	#First Matched Pair
	if count == 0:
		#Base Internships Meeting Criteria for Pair A
		intf = pd.read_csv("keys/int_key.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Drop Selections from Internship to Avoid Selection for Pair 2
		int_selection = df['int_id'].values.tolist()
		tmp = intf[((intf.int_id != int_selection[0]) &
				    (intf.int_id != int_selection[1]))]
		tmp.to_csv("keys/int_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships


	#Second Matched Pair
	elif count == 1:
		intf = pd.read_csv("keys/int_key_tmp.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships	

	else:
		pass


def internships_quant(job_type, prestige, company, count):
	'''
	Selects different first/second internships based on int_key
	'''

	#First Matched Pair
	if count == 0:
		#Base Internships Meeting Criteria for Pair A
		intf = pd.read_csv("keys/int_key.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Drop Selections from Internship to Avoid Selection for Pair 2
		int_selection = df['int_id'].values.tolist()
		tmp = intf[((intf.int_id != int_selection[0]) &
				    (intf.int_id != int_selection[1]))]
		tmp.to_csv("keys/int_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships


	#Second Matched Pair
	elif count == 1:
		intf = pd.read_csv("keys/int_key_tmp.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships	

	else:
		pass


def internships_ordered(job_type, prestige, company, count):
	'''
	Selects different first/second internships based on int_key
	'''

	#First Matched Pair
	if count == 0:
		#Base Internships Meeting Criteria for Pair A
		intf = pd.read_csv("keys/int_key.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Drop Selections from Internship to Avoid Selection for Pair 2
		int_selection = df['int_id'].values.tolist()
		tmp = intf[((intf.int_id != int_selection[0]) &
				    (intf.int_id != int_selection[1]))]
		tmp.to_csv("keys/int_key_tmp.csv", index=False)


		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships


	#Second Matched Pair
	elif count == 1:
		intf = pd.read_csv("keys/int_key_tmp.csv")
		criteria = ((intf['job_type']==job_type) & 
					(intf['prestige']==prestige) & 
					(intf['internship']!=company))
		int_df = intf.loc[criteria]

		#First Internship
		int_1 = int_df.loc[(int_df['int_type']=='first')]
		i1 = np.random.choice(int_1.index.values, 1, replace=False)
		df_1 = int_1.ix[i1]

		#Second Internship
		int_2 = int_df.loc[(int_df['int_type']=='second')]
		i2 = np.random.choice(int_2.index.values, 1, replace=False)
		df_2 = int_2.ix[i2]
		
		#Both Internships
		df = pd.concat([df_1, df_2], axis=0)

		#Return Results
		df = df.drop(['job_type', 'prestige'], axis=1)
		keys = df.columns.tolist()
		vals = df.values.tolist()
		internships =  vals[0]+vals[1]
		return internships	

	else:
		pass


def select_int(row, count):
	#print(row)

	job_type = row[0]
	prestige = row[1]
	company = row[2]

	if job_type in ['data_science', 'computer_science', 'mba', 'mba_finance']:
		internships = internships_general(job_type, prestige, company, count)
	if job_type in ['consultant', 'quant', 'stats']:
		internships = internships_ordered(job_type, prestige, company, count)
	else:
		pass

	return internships









def join_ex_pair(ex_df, cid):

	#Experiment Pair DF
	ex = ex_df.loc[(ex_df['cid']==cid)].reset_index()
	#print(ex)

	#Select GA Schools
	ga_vals = ['department', 'sid', 'ga_sid', 'school', 
			   'school_ctyst', 'school_cszip', 'school_address',
			   'title', 'rgb', 'matched_pair']
	ga_keys = ['profile', 'job_type', 'region', 'proximal_region']


	#Select UG Schools
	ug_vals = ['ug_sid', 'ug_school', 'ug_school_short', 'ug_ctyst', 
			   'treatment', 'prestige']
	ug_keys = ['profile', 'region', 'sid']


	#Select Internships
	int_vals = ['int_id1', 'internship1', 'int1_ctyst', 'int1_title', 'int1_type', 
				'int_id2', 'internship2', 'int2_ctyst', 'int2_title', 'int2_type']
	int_keys = ['job_type', 'prestige', 'company']


	#Determine Unique GA/UG Profiles for Matched Pairs 
	#(Meeting Profile Criteria)
	pairs = []
	for i in list(ex.index):
		row = ex.iloc[[i]].copy()

		#Grad School
		ga_result = select_ga(row[ga_keys].values.tolist()[0], i)
		row[ga_vals] = pd.DataFrame([ga_result], index=row.index)

		#Undergrad
		import pdb
		ug_result = select_ug(row[ug_keys].values.tolist()[0], i)
		row[ug_vals] = pd.DataFrame([ug_result], index=row.index)

		#Internship
		int_result = select_int(row[int_keys].values.tolist()[0], i)
		row[int_vals] = pd.DataFrame([int_result], index=row.index)

		pairs.append(row)


	df = pd.concat(pairs)
	return df


def join_experiment_profiles_counter(experiment_file):
	ex_full = pd.read_csv(experiment_file)
	cids = ex_full.cid.unique()
	print("[*] generating {} requested matched pairs...".format(len(cids)))

	#Join All Experiment Matched Pairs
	matched_pairs = []
	for c in cids:
		pair = join_ex_pair(ex_full, c)
		matched_pairs.append(pair)
	
	ex_all = pd.concat(matched_pairs)
	profiles = join_profiles_credentials()
	df = pd.merge(ex_all, profiles, on=['profile'])

	#Update MBA Treatments 
	df['treatment'] = df.apply(ret_mba_treatment, axis=1)

	#Update Treatment Leadership Position
	df['treatment'] = df.apply(update_treatment_leadership, axis=1)	

	#Sort by ID
	df['sort'] = df['id'].str.extract('(\d+)', expand=False).astype(int)
	df.sort_values('sort',inplace=True, ascending=True)
	df = df.drop('sort', axis=1)
	print(df)
	return df






def send_email_iter(row):
	message = ("[*] sending email to {0} at {1} from {2} - {3}, pair: {4}, version: {5}"
			.format(row['contact_name'],
					row['company'],
					row['name'],
					row['profile'],
					row['matched_pair'],
					row['version']
				))

	try:
		print(message)
		meta = send_email(
					profile=row['profile'],
					job_type=row['job_type'],
					contact=row['contact_name'],
					contact_last_name=row['contact_last_name'],
					job=row['position'],
					office=row['office'], 
					company=row['company'],
					name=row['name'], 
					title=row['title'], 
					school=row['school'],
					school_ctyst=row['school_ctyst'],
					school_cszip=row['school_cszip'],
					school_address=row['school_address'],
					department=row['department'],
					ba_school=row['ug_school'], 
					ba_ctyst=row['ug_ctyst'],
					internship1=row['internship1'],
					int1_ctyst=row['int1_ctyst'],
					int1_title=row['int1_title'],
					internship2=row['internship2'],
					int2_ctyst=row['int2_ctyst'],
					int2_title=row['int2_title'],
					treatment=row['treatment'],
					phone=row['phone'], 
					gmail_user=row['gmail_user'],
					gmail_pass=row['gmail_pass'],
					contact_email=row['contact_email'],
					rgb=row['rgb'],
					pair=row['matched_pair'],
					pair_version=row['version']
					)
		
		return 'metadata::'+meta



	except Exception as e:
		print("[!] error {}".format(message.replace('[*] ', '')))
		print("[!] error code: {}".format(e))
		return 'error::'+str(e)


def deploy_matched_pairs_emails(df, experiment_csv, matched_pair):
	df['metadata'] = df.apply(send_email_iter, axis=1)

	#write result file
	infile = experiment_csv.split('.')[0]
	outfile = "logs/results_log_{0}_pairs_{1}.csv".format(
												infile, 
												matched_pair)
	df.to_csv(outfile, index=False)



def display_time_elapsed(start, end, companies=None, version=None):
	time_elapsed = ((end-start)/60)
	time_message = '[*] {} minutes elapsed...'.format(time_elapsed)
	
	if companies is None and version is None:
		print(time_message)

	if companies is not None and version is not None:
		c = '{} companies...'.format(companies)
		v = 'version {}...'.format(version)
		print(time_message+v+c)
	else:
		pass



def deploy_emails(experiment_csv):
	s1 = time.time()
	df = join_experiment_profiles_counter(experiment_csv)
	ex_out = "logs/{}_output.csv".format(experiment_csv.split(".")[0])
	df.to_csv(ex_out, index=False)

	#Matched Pairs A
	df_A = df.loc[(df['matched_pair']=='A')].copy()
	deploy_matched_pairs_emails(df_A, experiment_csv, "A")
	e1 = time.time()

	for i in range(10,0,-1):
	    sys.stdout.write(str(i)+' ')
	    sys.stdout.flush()
	    time.sleep(1)


	#Matched Pairs B
	s2 = time.time()
	df_B = df.loc[(df['matched_pair']=='B')].copy()
	deploy_matched_pairs_emails(df_B, experiment_csv, "B")
	e2 = time.time()

	display_time_elapsed(s1, e1, df_A.shape[0], "A")
	display_time_elapsed(s2, e2, df_B.shape[0], "B")



deploy_emails("experiment_test.csv")







