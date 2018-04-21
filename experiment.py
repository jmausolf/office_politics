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


def join_profiles_credentials():
	cred = pd.read_csv("credentials.csv")
	prof = pd.read_csv("profiles.csv")

	df = pd.merge(cred, prof, on=['profile'])
	return df



def select_ga(row):

	profile = row[0]
	job_type = row[1]
	region = row[2]

	ga = pd.read_csv("ga_school_key.csv")
	criteria = ((ga['region']==region) & 
				(ga['job_type']==job_type) & 
				(ga['prestige']==profile[-1]))
	ga = ga.loc[criteria] 

	#Random Selection of Schools Meeting Criteria
	rows = np.random.choice(ga.index.values, 1)
	df = ga.ix[rows]
	df = df.drop(['region', 'job_type', 'prestige'], axis=1)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	return vals


def select_ug(row):

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
	df = ug.ix[rows]
	df = df.drop(['region', 'profile'], axis=1)

	keys = df.columns.tolist()
	vals = df.values.tolist()[0]
	return vals



def join_experiment_profiles(experiment_file):
	ex = pd.read_csv(experiment_file)

	#Select GA Schools
	ga_keys = ['department','school','school_short','school_ctyst','school_cszip','school_address','title']
	ex[ga_keys] = ex[['profile', 'job_type', 'region']].apply(lambda row: pd.Series(select_ga(row)), axis=1)

	#Select UG Schools
	ug_keys = ['ba_school', 'ba_school_short', 'ba_ctyst', 'experiment', 'prestige']
	ex[ug_keys] = ex[['profile', 'region', 'school']].apply(lambda row: pd.Series(select_ug(row)), axis=1)


	profiles = join_profiles_credentials()
	df = pd.merge(ex, profiles, on=['profile'])
	#print(df)
	return df



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

	df = join_experiment_profiles("experiment_test.csv")
	#print(df)

	df['metadata'] = df.apply(send_email_iter, axis=1)
	print(df)

	#write result file
	outfile = "logs/results_log_{}".format(experiment_csv)
	df.to_csv(outfile, index=False)



deploy_emails("experiment_test.csv")




