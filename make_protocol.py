import ast, csv, os, pdb
import numpy as np
import pandas as pd
import datetime
from get_jobs.filter_jobs import index_to_n



def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d-%X").replace(':','')
	return date


def get_leads(df,
				leads_key='keys/leadiro_matched_key.csv'
				):

	#Initial Merge
	leads = pd.read_csv(leads_key)
	df = df.merge(leads, how='left')

	#Drop Any Rows Without Contact Information
	df = df.dropna(subset=['contact_email'])

	#Drop Duplicate List ID's Keeping the First
	df = df.drop_duplicates(subset='contact_email')
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

	#TODO Issue a Warning if region/prox region have NAN 
	#after the merge
	df.dropna(inplace=True)
	df.to_csv('merged_regions.csv', index=False)
	return df


#Assign Applicant Prestige
def assign_prestige(df, 
					probs=[.7,.3],
					labels=['High', 'Low'],
					col='prestige_level'):
	df[col] = np.random.choice(labels, df.shape[0], p=probs)
	return df


#Assign Order
def assign_order(df, order_list=[1, 2],
				 probs=[.5,.5], col='order'):
	df[col] = np.random.choice(order_list, df.shape[0], p=probs)
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


#Assign Treatment leader
def assign_treatment_leader(df, 
							 leader_list=['president', 'vice president'],
							 probs=[.5,.5], col='leader'):
	df[col] = np.random.choice(leader_list, df.shape[0], p=probs)
	return df

def set_leader(leader_letter, leader_list=None):
	assert isinstance(leader_letter, str), "leader_letter must be string"

	if leader_list is None:
		p = 'president'
		vp = 'vice president'
	else:
		assert len(leader_list) == 2, "only two versions possible"
		p = leader_list[0]
		vp = leader_list[1]

	if leader_letter == p:
		return vp
	if leader_letter == vp:
		return p
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
			   order=None,
			   version=None,
			   leader=None,
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

	The order is the name of the variable for the 
		previously assigned random integer (1, 2)
		determining which subject (Control or Treatment) 
		should be first. 

	The version is the name of the variable for the 
		previously assigned materials version (A, B)
		determining which resume and cover letter version
		a subject is assigned.
		
	The leader is the name of the variable for the 
		previously assigned leadership position
		('president', 'vice president')
		for the treatment/control leadership positions

	Example Parameters:
	df :: an experimental data frame
	treatment_labs :: ['DEM', 'REP']
	treatment_probs :: [.4, .6]
	control_label :: 'NEU'
	pair_key :: 'cid'
	order :: 'order'
	version :: 'version'
	leader :: 'leadership'
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
	if order is not None:
		order_int = sorted(T[order].unique().tolist())
		assert len(order_int) == 2, "order must be one of two ints"
		T[order] = T[order].apply(lambda x: set_order(x, order_int))
		pass

	#Version
	if version is not None:
		versions = sorted(T[version].unique().tolist())
		assert len(versions) == 2, "only two versions are possible"
		T[version] = T[version].apply(lambda x: set_version(x, versions))
		pass

	#Leadership
	if leader is not None:
		leaders = sorted(T[leader].unique().tolist())
		assert len(leaders) == 2, "only two leaderships are possible"
		T[leader] = T[leader].apply(lambda x: set_version(x, leaders))
		pass

	#Create Matched Pairs
	MP = C.append(T, ignore_index=True)

	#Sort Matched Pairs and Return
	if order is not None:
		MP.sort_values(by=[pair_key, order], inplace=True)
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
		 order,
		 order_list,
		 version,
		 version_list,
		 leader,
		 leader_list,
		 rm_cols='default',
		 order_cols='default',
		 outfile_stem='experiment'
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
	emp = assign_order(emp, col=order,
							order_list=order_list)
	emp = assign_materials_version(emp, col=version,
										version_list=version_list)
	emp = assign_treatment_leader(emp, col=leader,
										leader_list=leader_list)
	emp = make_pairs(emp,
					 treatment_labs,
					 treatment_probs,
					 control_lab,
					 pair_key,
					 order,
					 version,
					 leader,
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
						exp_order=order,
						exp_order_list=order_list,
						exp_version=version,
						exp_version_list=version_list,
						exp_leader=leader,
						exp_leader_list=leader_list,
						exp_rm_cols=rm_cols
						)


	#Outfile
	outfile = 'protocols/{}_{}.csv'.format(outfile_stem, get_date())
	log = 'logs/protocol_'+outfile.split('protocols/')[1]

	#Store Detailed File in Logs
	emp = details[0]
	log_exp_details = emp.to_csv(log, index=False)


	#Remove Default Columns
	if rm_cols == 'default':
		rm_cols = ['state_name', 'state', 'prestige_level', 
				   'party', order, 'name']
	
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
					  'position', 'job_type', 'profile', 
					  version, leader]
		emp = emp[cols_order]
	else:
		assert isinstance(order_cols, list), 'provide a column order list'+\
											 'or set order_cols=False'
		emp = emp[order_cols]


	print(emp)
	print(emp.isna().sum())
	print('[*] saving experimental protocol to {}'.format(outfile))
	emp.to_csv(outfile, index=False)
	return outfile, emp
	

def check_profile_load(limit, df=None, protocol_file=None,
					   df_name='dataframe', ret_max=False):

	err_message1 = '[*] must provide either a dataframe or csv...'
	err_message2 = '[*] must only provide a dataframe OR csv, not both...'
	assert any(v is not None for v in [df, protocol_file]), err_message1
	assert any(v is None for v in [df, protocol_file]), err_message2

	if df is not None:
		m = '[*] evaluating profile load for {}...'.format(df_name)
		counts = df['profile'].value_counts()

	if protocol_file is not None:
		m = '[*] evaluating profile load for {}...'.format(protocol_file)
		df = pd.read_csv(protocol_file)
		counts = df['profile'].value_counts()
		
	
	if ret_max is True:
		return counts.max()
	else:
		print(m)
		print(counts)
		if counts.max() > limit:
			return False
		else:
			return True


def replicate_match_pairs(protocol_file, limit, ret_max=False):

	df = pd.read_csv(protocol_file)
	df_A = df.loc[(df['version']=='A')].copy()
	df_B = df.loc[(df['version']=='B')].copy()

	result1 = check_profile_load(limit, df=df_A, 
								 df_name='df_A', ret_max=ret_max)
	result2 = check_profile_load(limit, df=df_B, 
								 df_name='df_B', ret_max=ret_max)

	if ret_max is False:
		if result1 is True and result2 is True:
			return True
		else: 
			return False
	else:
		return result1, result2


def need_batches(protocol_file, limit):
	print('\n[*] CHECKING to see if batches are required....')
	result = check_profile_load(limit, protocol_file=protocol_file)
	if result is True:
		print('[*] NO: batches are not required...')
		return False
	else:
		print('[*] WARNING: batches may be required for protocol...')
		
		#Check A/B pairs and see if it still needs batching
		subresults = replicate_match_pairs(protocol_file, limit)
		if subresults is True:
			print('[*] NO: batches not required for using A/B pairs...')
			print('[*] ENSURE: at least a 24 hour delay between batches...')
			return False
		else:
			print('[*] YES: batches ARE REQUIRED even using A/B pairs...')
			return True


def index_marks(nrows, chunk_size):
	first = 1 * chunk_size
	second = (nrows // chunk_size + 1) * chunk_size
	third = chunk_size
	return range(first, second, third)


def split(dfm, chunk_size):
	indices = index_marks(dfm.shape[0], chunk_size)
	return np.split(dfm, indices)


def make_batches(protocol_file, limit):
	
	if need_batches(protocol_file, limit) is True:
		protocol_df = pd.read_csv(protocol_file)
		r1, r2 = replicate_match_pairs(protocol_file, limit, ret_max=True)
		max_load = max(r1, r2)
		batches = (max_load // limit)+1
		print('[*] TOTAL of {} batches are suggested...'.format(batches))

		n = protocol_df.shape[0] // batches
		if n % 2 == 0:
			pass
		else: 
			n +=1

		chunks = split(protocol_df, n)
		batch_number = 0
		batches = []
		for c in chunks:
			if c.shape[0] > 0:
				print("Shape: {}; {}".format(c.shape, c.index))
				batch_number +=1
				protocol_stem = protocol_file.split('.csv')[0]
				outfile = '{}_batch_{}.csv'.format(protocol_stem, batch_number)
				batches.append(outfile)
				c.to_csv(outfile, index=False)
			else:
				pass

	
		#Recheck Batches for Compliance
		for b in batches:
			make_batches(b, limit)

		return batches

	else:
		return ["No batches"]





protocol_outfile, protocol_df = main(
	 employers='keys/cleaned_employers_key.csv',
     state_col='office_state',
     prestige_probs=[.7, .3],
     prestige_labs=['High', 'Low'],
     treatment_probs=[.4, .6],
     treatment_labs=['DEM', 'REP'],
     control_lab='NEU',
     pair_key='cid',
     order='order',
     order_list=[1,2],
     version='version',
     version_list=['A', 'B'],
     leader='leadership',
     leader_list=['president', 'vice president'],
     rm_cols='default',
     order_cols='default'
    )


batches = make_batches(protocol_outfile, limit=700)
print([protocol_outfile]+batches)


#make_batches('experiment_2019-03-26-224927.csv', limit=1000)





