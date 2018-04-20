import random
import pandas as pd
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

def join_experiment_profiles(experiment_file):
	experiment = pd.read_csv(experiment_file)
	profiles = join_profiles_credentials()
	df = pd.merge(experiment, profiles, on=['profile'])

	return df








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
					job_type=row['category'],
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




