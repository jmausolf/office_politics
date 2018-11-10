import ast, csv, os, pdb
import numpy as np
import pandas as pd
from get_jobs.filter_jobs import index_to_n



################
#0a TODO Join with Contact Name/Email by Company
#and see if you can get the order in a logical way
#################
def convert_xlsx_csv(file):
	print("Converting file: '{}' to .csv file...".format(file))
	pd.read_excel(file).to_csv(str(file).replace("xlsx", "csv"))


def convert_files_xlsx_csv(stem='police_ois_report'):
	files = glob('downloads/*{}*.xlsx'.format(stem))
	for file in files:
		convert_xlsx_csv(file)

		


def get_regions(df,
				state_col,
				region_col='state',
				region_key='region_key.csv'
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

#3
def make_pairs(df,
			   treatment_labs,
			   treatment_probs,
			   control_label,
			   pair_key,
			   order_var=None
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

	#Order
	if order_var is not None:
		order_int = sorted(T[order_var].unique().tolist())
		assert len(order_int) == 2, "order must be one of two ints"
		T[order_var] = T[order_var].apply(lambda x: set_order(x, order_int))
		pass

	#Create Matched Pairs
	MP = C.append(T, ignore_index=True)

	#Sort Matched Pairs and Return
	if order_var is not None:
		MP.sort_values(by=[pair_key, order_var], inplace=True)
	else:
		MP.sort_values(by=[pair_key], inplace=True)
	return MP


#4Join Profile ID based on Prestige and Partisanship
def add_profile_key(experiment_df, 
					profile_key='profiles.csv', 
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

'''
emp = pd.read_csv('employers_key.csv')
emp = get_regions(emp, 'office_state')
emp = assign_prestige(emp, probs=[.7, .3], labels=['High', 'Low'])
emp = assign_order(emp)
emp = make_pairs(emp,
				 ['DEM', 'REP'],
				 [.4, .6],
				 'NEU',
				 'cid',
				 'order'
				 )
emp = add_profile_key(emp)

rm_cols = ['state_name', 'state', 'prestige_level', 'party', 'order', 'name']
emp = cleanup_cols(emp, rm_cols)
emp = add_applicant_id(emp)

print(emp)
emp.to_csv('test_exp.csv', index=False)
'''

def main(**kwargs):

	kw = kwargs

	print(kw)
	print(kw['output'])
	'''
	emp = pd.read_csv('employers_key.csv')
	emp = get_regions(emp, 'office_state')
	emp = assign_prestige(emp, probs=[.7, .3], labels=['High', 'Low'])
	emp = assign_order(emp)
	emp = make_pairs(emp,
					 ['DEM', 'REP'],
					 [.4, .6],
					 'NEU',
					 'cid',
					 'order'
					 )
	emp = add_profile_key(emp)

	rm_cols = ['state_name', 'state', 'prestige_level', 'party', 'order', 'name']
	emp = cleanup_cols(emp, rm_cols)
	emp = add_applicant_id(emp)

	print(emp)
	emp.to_csv('test_exp.csv', index=False)
	'''

main(output="x")


#TODO
#Number all rows by id, a1, a2, ...





