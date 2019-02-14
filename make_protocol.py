import ast, csv, os, pdb
import numpy as np
import pandas as pd
import datetime
from get_jobs.filter_jobs import index_to_n



def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date


def get_leads(df,
				leads_key='keys/leadiro_matched_key.csv'
				):

	leads = pd.read_csv(leads_key)
	df = df.merge(leads, how='left')


	#TODO Issue a Warning if name/email have NAN 
	#after the merge
	print(df)
	return df


def get_regions(df,
				state_col,
				region_col='state',
				region_key='keys/region_key.csv'
				):

	sc = state_col
	rc = region_col

	regions = pd.read_csv(region_key)
	df = df.merge(regions, how='left', left_on=sc, right_on=rc)
	df.to_csv('test_regions.csv', index=False)
	return df


#Assign Applicant Prestige
def assign_prestige(df, 
					probs=[.7,.3],
					labels=['High', 'Low'],
					col='prestige_level'):
	df[col] = np.random.choice(labels, df.shape[0], p=probs)
	return df


#Assign Order
def assign_order(df, probs=[.5,.5], col='order'):
	df[col] = np.random.choice([1, 2], df.shape[0], p=probs)
	return df


def set_order(order_number, order_int=None):
	assert isinstance(order_number, int), "order must be an integer"

	if order_int is None:
		o1 = 1
		o2 = 2
	else:
		assert len(order_int) == 2, "order ints must have only two options"
		o1 = order_int[0]
		o2 = order_int[1]

	if order_number == o1:
		return o2
	if order_number == o2:
		return o1
	else:
		return None


#Assign Materials Version
def assign_materials_version(df, version_list=['A', 'B'],
							 probs=[.5,.5], col='version'):
	df[col] = np.random.choice(version_list, df.shape[0], p=probs)
	return df

def set_version(version_letter, version_list=None):
	assert isinstance(version_letter, str), "version_letter must be string"

	if version_list is None:
		vA = 'A'
		vB = 'B'
	else:
		assert len(version_list) == 2, "only two versions possible"
		vA = version_list[0]
		vB = version_list[1]

	if version_letter == vA:
		return vB
	if version_letter == vB:
		return vA
	else:
		return None


#Assign Partisanship
def assign_partisanship(df, condition, 
						probs=[.5,.5], labels=None,
						col='party'):

	qc = condition
	qc_condition = ( 
						( isinstance(qc, str) is True ) &
						( qc == 'treatment' or qc == 'control') 
				   )
	assert qc_condition, "condition should equal 'treatment' or 'control' "

	#Assign Labels
	if labels is None:
		if condition == 'treatment':
			df[col] = np.random.choice(['DEM', 'REP'], 
											df.shape[0], p=probs)
			return df
		elif condition == 'control':
			df[col] = 'NEU'

	else:

		lb = labels
		lb_conditionT = ( 
							( len(probs) == len(list(labels)) ) &
							( isinstance(lb, list) is True) &
							( isinstance(lb[0], str) is True)
					 	)

		lb_conditionC = ( 
							( isinstance(lb, str) is True)
					 	)

		#Assign User Provided Labels for Treatment and Control
		if condition == 'treatment':
			assert lb_conditionT, "labels should be a list of strings; "+\
								  "label list should be same length as probs"
			df[col] = np.random.choice(labels, df.shape[0], p=probs)


		elif condition == 'control':
			assert lb_conditionC, "control can have only one label; "+\
								  "label must be string format"
			df[col] = labels


	return df






def make_pairs(df,
			   treatment_labs,
			   treatment_probs,
			   control_label,
			   pair_key,
			   order_var=None,
			   version=None
			   ):

	'''
	This function randomly assigns treatment and control conditions
	assuming a matched pair design, where each pair has a treatment
	and a control.

	The control is designed to be the same condition for all receiving it.
	control prob == 1.0

	The treatment can take any number of labels, but should be >=2 labels
	The probability of receiving these labels should sum to 1
	Treatment probabilities should be the same number as the number of labels

	The experimental dataframe may have other conditions.
	These should be assigned before making the matched pairs.
		e.g. matched subject attributes such as
		prestige, race, or gender should be assigned before
		assigning the matched pair treatments/control

	The pair_key is the id variable to be given the matched pair.
		e.g. pair_key could be the company id to send resumes, 'cid'

	The order_var is the previously assigned random integer (1, 2)
		determining which subject (Control or Treatment) 
		should be first. 
		If order does not matter, use order_var=None

	Example Parameters:
	df :: an experimental data frame
	treatment_labs :: ['DEM', 'REP']
	treatment_probs :: [.4, .6]
	control_label :: 'NEU'
	pair_key :: 'cid'
	order_var :: 'order'
	'''

	#Control Matched Subjects
	C = df.copy()
	C = assign_partisanship(C, 'control', labels=control_label)

	#Treatment(s) Matched Subjects
	T = df.copy()
	T = assign_partisanship(T, 'treatment', 
							labels=treatment_labs, 
							probs=treatment_probs)

	# Determine Order and Version for Treatment
	# Using Randomly Assigned Order and Version for Control

	#Order
	if order_var is not None:
		order_int = sorted(T[order_var].unique().tolist())
		assert len(order_int) == 2, "order must be one of two ints"
		T[order_var] = T[order_var].apply(lambda x: set_order(x, order_int))
		pass

	#Version
	if version is not None:
		versions = sorted(T[version].unique().tolist())
		assert len(versions) == 2, "only two versions are possible"
		T[version] = T[version].apply(lambda x: set_version(x, versions))
		pass

	#Create Matched Pairs
	MP = C.append(T, ignore_index=True)

	#Sort Matched Pairs and Return
	if order_var is not None:
		MP.sort_values(by=[pair_key, order_var], inplace=True)
	else:
		MP.sort_values(by=[pair_key], inplace=True)
	return MP


#Join Profile ID based on Prestige and Partisanship
def add_profile_key(experiment_df, 
					profile_key='keys/profiles.csv', 
					prestige_col='prestige_level',
					party_col='party'):

	pst = prestige_col
	pid = party_col
	key = pd.read_csv(profile_key)

	df = experiment_df.merge(key,
							 how='left',
							 on=[pst, pid])

	return df


#Drop Extra Columns
def cleanup_cols(df, rm_col_list):
	'''
	Removes columns from the data frame to conform to
	ideal experimental protocol config needed in experiment.py

	Removes:
	(A) extraneous cols
	(B) columns already joined later in the experiment
	'''

	cols = df.columns.tolist()
	keep_cols = [c for c in cols if c not in rm_col_list]

	return df[keep_cols].copy().reset_index(drop=True)


def add_applicant_id(df, col='id'):

	#Make Appplicant ID
	df['index'] = df.index
	df[col] = df['index'].apply(lambda x: index_to_n(x, 'a'))

	#Change Column Order
	df_id = df['id'].copy()
	df = cleanup_cols(df, ['index', 'id'])
	df = pd.concat([df_id, df], axis=1) 
	return df


def store_details(df, **kwargs):

	details = []
	for k, v in kwargs.items():
		df[k] = str(v)
		details.append(k)

	return [df, details]


def main(employers,
		 state_col,
		 prestige_probs,
		 prestige_labs,
		 treatment_probs,
		 treatment_labs,
		 control_lab,
		 pair_key,
		 order_var,
		 version,
		 rm_cols='default',
		 order_cols='default',
		 outfile='experiment.csv'
		):


	#Load Employer Data
	emp = pd.read_csv(employers)

	#Get Regions
	emp = get_regions(emp, state_col)

	#Get Leads
	emp = get_leads(emp)

	#Make Assignments
	emp = assign_prestige(emp, 
						  probs=prestige_probs,
						  labels=prestige_labs
						  )
	emp = assign_order(emp)
	emp = assign_materials_version(emp)
	emp = make_pairs(emp,
					 treatment_labs,
					 treatment_probs,
					 control_lab,
					 pair_key,
					 order_var,
					 version
					 )
	emp = add_profile_key(emp)

	#Add Experiment Details to Full File
	details = store_details(emp,
						exp_date=get_date(),
						exp_employers=employers,
						exp_state_col=state_col,
						exp_prestige_probs=prestige_probs,
						exp_prestige_labs=prestige_labs,
						exp_treatment_probs=treatment_probs,
						exp_treatment_labs=treatment_labs,
						exp_control_lab=control_lab,
						exp_pair_key=pair_key,
						exp_order_var=order_var,
						exp_version=version,
						exp_rm_cols=rm_cols
						)



	#Store Detailed File in Logs
	emp = details[0]
	stem = outfile.replace('.csv', '')
	log = 'logs/protocol_{}_{}.csv'.format(stem, get_date())
	log_exp_details = emp.to_csv(log)


	#Remove Default Columns
	if rm_cols == 'default':
		rm_cols = ['state_name', 'state', 'prestige_level', 
				   'party', order_var, 'name']
	
	#Or User Provided Column List
	else:
		assert isinstance(rm_cols, list), 'provide a list of cols to remove'


	#Make Clean File to Run
	log_cols = details[1]
	rm_cols = rm_cols+log_cols
	emp = cleanup_cols(emp, rm_cols)
	emp = add_applicant_id(emp)

	#Order Remaining Columns
	if order_cols is False:
		pass
	elif order_cols == 'default':
		cols_order = ['id', 'cid', 'list_id', 'company',
					  'contact_name', 'contact_last_name', 'contact_email',
					  'office', 'office_state', 'region', 'proximal_region', 
					  'position', 'job_type', 'profile', version]
		emp = emp[cols_order]
	else:
		assert isinstance(order_cols, list), 'provide a column order list'+\
											 'or set order_cols=False'
		emp = emp[order_cols]


	print(emp)
	print('[*] saving experimental protocol to {}'.format(outfile))
	emp.to_csv(outfile, index=False)
	


main(employers='keys/cleaned_employers_key.csv',
     state_col='office_state',
     prestige_probs=[.7, .3],
     prestige_labs=['High', 'Low'],
     treatment_probs=[.4, .6],
     treatment_labs=['DEM', 'REP'],
     control_lab='NEU',
     pair_key='cid',
     order_var='order',
     version='version',
     rm_cols='default',
     order_cols='default'
    )





