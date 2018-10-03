import random
import pandas as pd
import numpy as np
from new_messages import *
import textwrap
import inspect
import textile
from internship_key import internship_keys
from make_cover_letters import *
from send_email import *
import pdb

#pdb.set_trace()

def join_profiles_credentials():
	cred = pd.read_csv("credentials.csv")
	prof = pd.read_csv("profiles.csv")

	df = pd.merge(cred, prof, on=['profile'])
	return df



def select_ga(row):

	profile = row[0]
	job_type = row[1]
	region = row[2]
	proximal = row[3]

	#Select Match from Region or Proximal Region
	ga = pd.read_csv("ga_school_key.csv")
	criteria = (((ga['region']==region) |
				 (ga['region']==proximal)) & 
				(ga['job_type']==job_type) & 					
				(ga['prestige']==profile[-1]))
	#print(criteria)
	ga = ga.loc[criteria] 

	#Random Selection of Schools Meeting Criteria
	rows = np.random.choice(ga.index.values, 1)
	df = ga.ix[rows]
	df = df.drop(['region', 'job_type', 'prestige'], axis=1)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	return vals


def select_ug(row):

	#TODO
	#build in a counter,

	profile = row[0]
	region = row[1]
	school = row[2]

	ug = pd.read_csv("ug_school_key.csv")
	criteria = ((ug['profile']==profile) & 
				(ug['region']==region) & 
				(ug['ba_school']!=school))
	ug = ug.loc[criteria] 
	
	#Random Selection of Schools Meeting Criteria
	rows = np.random.choice(ug.index.values, 1)
	#print(rows)
	df = ug.ix[rows]
	df = df.drop(['region', 'profile'], axis=1)
	#print(df)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	#print(vals)
	return vals





def select_ga3(row, count):

	#index = row.index
	#print(index)
	#print(row)

	#count+=1


	profile = row[0]
	job_type = row[1]
	region = row[2]
	proximal = row[3]


	if count == 0:
		print("FIRST MATCHED PAIR")
	elif count == 1:
		print("SECOND MATCHED PAIR")
	else:
		pass

	#Select Match from Region or Proximal Region
	ga = pd.read_csv("ga_school_key.csv")
	criteria = (((ga['region']==region) |
				 (ga['region']==proximal)) & 
				(ga['job_type']==job_type) & 					
				(ga['prestige']==profile[-1]))
	#print(criteria)
	ga = ga.loc[criteria] 
	#print(ga)


	#Random Selection of Schools Meeting Criteria
	rows = np.random.choice(ga.index.values, 1)
	df = ga.ix[rows]
	df = df.drop(['region', 'job_type', 'prestige'], axis=1)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	#print(vals)
	return vals
	#print(df)
	#return df


def select_ug3(row, count):

	#TODO
	#build in a counter,

	profile = row[0]
	region = row[1]
	school = row[2]


	if count == 0:
		print("FIRST MATCHED PAIR")
	elif count == 1:
		print("SECOND MATCHED PAIR")
	else:
		pass

	ug = pd.read_csv("ug_school_key.csv")
	criteria = ((ug['profile']==profile) & 
				(ug['region']==region) & 
				(ug['ba_school']!=school))
	ug = ug.loc[criteria] 
	
	#Random Selection of Schools Meeting Criteria
	rows = np.random.choice(ug.index.values, 1)
	#print(rows)
	df = ug.ix[rows]
	df = df.drop(['region', 'profile'], axis=1)
	#print(df)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	#print(vals)
	return vals








def join_experiment_profiles(experiment_file):
	ex = pd.read_csv(experiment_file)
	#print(ex.shape)

	#perhaps do it by cid, for c in cid, ret 2 vals


	#Select GA Schools
	ga_vals = ['department','school','school_short','school_ctyst',
			   'school_cszip','school_address','title']
	ga_keys = ['profile', 'job_type', 'region', 'proximal_region']

	ex[ga_vals] = ex[ga_keys].apply(
							 lambda row: pd.Series(select_ga(row)), axis=1)

	print(ex)
	print(ex.shape)

	#Select UG Schools
	ug_vals = ['ba_school', 'ba_school_short', 'ba_ctyst', 
			   'treatment', 'prestige']
	ug_keys = ['profile', 'region', 'school']

	ex[ug_vals] = ex[ug_keys].apply(
							 lambda row: pd.Series(select_ug(row)), axis=1)


	print(ex)
	print(ex.shape)

	profiles = join_profiles_credentials()
	df = pd.merge(ex, profiles, on=['profile'])
	#print(df)
	return df


	#Currently this function runs s.t. it does all ga, then all ug, same list basis each time
	#need to try to reorg an intermediary function that gets ga and ug for a row
	#reorg the lamda then with a counter function
	#if count == 0, start with base lists
	#if count > 0, subtract ug/ga lines from list, save as tmp list, sample from this list
	#then ga/ug will not be the same for the same profile




def join_ex_pair(ex_df, cid):


	count = 0
	ex = ex_df.loc[(ex_df['cid']==cid)]
	#print(ex.shape)

	#ex1 = ex.iloc[1]



	#Select GA Schools
	ga_vals = ['department','school','school_short','school_ctyst',
			   'school_cszip','school_address','title']
	ga_keys = ['profile', 'job_type', 'region', 'proximal_region']


	#Select UG Schools
	ug_vals = ['ba_school', 'ba_school_short', 'ba_ctyst', 
			   'treatment', 'prestige']
	ug_keys = ['profile', 'region', 'school']


	#TODO
	#Now that 1 and 2 are working, do diff actions for first and second pair
	#run first pair as is, but drop school selected school ids
	#write new df
	#for second df, sample from tmp df created in pair 1

	pairs = []
	for i in list(ex.index):
		row = ex.iloc[[i]].copy()

		#Grad School
		ga_result = select_ga3(row[ga_keys].values.tolist()[0], i)
		row[ga_vals] = pd.DataFrame([ga_result], index=row.index)

		#Undergrad
		ug_result = select_ug3(row[ug_keys].values.tolist()[0], i)
		row[ug_vals] = pd.DataFrame([ug_result], index=row.index)

		pairs.append(row)


	df = pd.concat(pairs)

	return df



def join_experiment_profiles_counter(experiment_file):
	#ex = pd.read_csv(experiment_file)
	ex_full = pd.read_csv(experiment_file)




	"""
	#print(ex.iloc[[1]])
	ex = ex_full.iloc[0:2]
	#ex = ex_full.iloc[[0]]
	#print(ex.shape)

	#perhaps do it by cid, for c in cid, ret 2 vals
	#ex_ci

	#Select GA Schools
	ga_vals = ['department','school','school_short','school_ctyst',
			   'school_cszip','school_address','title']
	ga_keys = ['profile', 'job_type', 'region', 'proximal_region']

	ex[ga_vals] = ex[ga_keys].apply(
							 lambda row: pd.Series(select_ga(row)), axis=1)
	#ex[ga_vals] = pd.Series(select_ga(ex.iloc[[1]]))


	#print(ex)
	#print(ex.shape)

	#Select UG Schools
	ug_vals = ['ba_school', 'ba_school_short', 'ba_ctyst', 
			   'treatment', 'prestige']
	ug_keys = ['profile', 'region', 'school']

	ex[ug_vals] = ex[ug_keys].apply(
							 lambda row: pd.Series(select_ug(row)), axis=1)
	#ex[ug_vals] = pd.Series(select_ug(ex.iloc[[1]]))
	"""

	df0 = join_ex_pair(ex_full, 'c01')
	print(df0)
	#print(ex)
	#print(ex.shape)

	#profiles = join_profiles_credentials()
	#df = pd.merge(ex, profiles, on=['profile'])
	#print(df)
	#return df


#join_experiment_profiles("experiment_test.csv")




def send_email_iter(row):

	message = ("[*] sending email to {0:<10} at {1:<20} from {2:>10} - {3:>5}..."
			.format(row['contact_name'],
					row['company'],
					row['name'],
					row['profile']
				))

	try:
		print(message)
		meta = send_email(
					profile=row['profile'],
					job_type=row['job_type'],
					contact=row['contact_name'],
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
					ba_school=row['ba_school'], 
					ba_ctyst=row['ba_ctyst'],
					treatment=row['treatment'],
					phone=row['phone'], 
					gmail_user=row['gmail_user'],
					gmail_pass=row['gmail_pass'],
					contact_email=row['contact_email']
					)
		
		return 'metadata::'+meta



	except Exception as e:
		print("[!] error {}".format(message.replace('[*] ', '')))
		print("[!] error code: {}".format(e))
		return 'error::'+str(e)





def deploy_emails(experiment_csv):

	#df = join_experiment_profiles(experiment_csv)
	df = join_experiment_profiles_counter(experiment_csv)
	#print(df)

	ex_out = "{}_output.csv".format(experiment_csv.split(".")[0])
	#df.to_csv(ex_out, index=False)

	#TODO
	#split DF into day1_app1, day2_app2
	#apply exp to day1df, wait, apply to day2df

	#df['metadata'] = df.apply(send_email_iter, axis=1)
	#print(df)

	#write result file
	#outfile = "logs/results_log_{}".format(experiment_csv)
	#df.to_csv(outfile, index=False)



deploy_emails("experiment_test.csv")





