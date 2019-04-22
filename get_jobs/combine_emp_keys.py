import subprocess
import pandas as pd
from glob import glob
import re, os, sys


def get_rank(filename):
	r = filename.split('_rank_')[1].split('.csv')[0]
	return int(r)


def get_file(filename):
	f = filename.split('../keys/')[1]
	return f

def index_to_n(index_number, letter='c'):

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


def make_cid(row):
	index = row['index']
	return index_to_n(index)


def combine_emp_keys(outfile_tail='_ranked_data.csv', 
					 stem='../keys/employers_key'):

	emp_key_pat = '{}_*.csv'.format(stem)
	g = glob(emp_key_pat)
	ex1 = glob('../keys/*key_ranked*.csv')
	ex2 = glob('../keys/employers_key.csv')

	ex = [ex1, ex2]
	exclude = []

	for glob_set in ex:
		if len(glob_set) > 0:
			exclude.extend(glob_set)
		else:
			pass
	glob_clean = [f for f in g if f not in exclude]
	print(glob_clean)

	emp_keys_list = []
	for f in glob_clean:

		filename = get_file(f)
		rank = get_rank(f)
		emp_df = pd.read_csv(f)

		message = '[*] making df for {}, rank = {}, shape = {}'.format(
					f, rank, emp_df.shape)
		print(message)

		emp_df['filename'] = filename
		emp_df['file_rank'] = rank
		emp_keys_list.append(emp_df)

	#Append Emp Keys
	df = pd.concat(emp_keys_list)


	#Count Companies
	gb = ['list_id']
	cm = 'list_id'
	df['cid_count'] = df.groupby(gb)[cm].transform('count')

	#Sort Values by Rank and List ID
	df = df.sort_values(by=['file_rank', 'list_id'], ascending=True)

	#Drop Duplicate List ID's Keeping the First (Highest Rank)
	df = df.drop_duplicates(subset='list_id')

	
	#Make Cleaned File
	keep_cols = ['list_id', 'company', 'position', 'office', 
				 'office_state', 'job_type', 'filename', 'file_rank']
	df_tmp = df[keep_cols].copy().reset_index()

	# Make New Company ID Column
	df_tmp['index'] = df_tmp.index
	cid = df_tmp.apply(make_cid, axis=1)
	df = pd.concat([cid, df_tmp[keep_cols]], axis=1)
	cols = ['cid', 'list_id', 'company', 'position', 'office', 
			'office_state', 'job_type', 'filename', 'file_rank']
	df.columns = cols


	# Keep Only Companies in Current Master Companies
	mc = pd.read_csv('master_companies.csv')['list_id'].to_frame()
	df = df.merge(mc, how='inner', on='list_id')
	print(df)

	#Save Full File
	outfile = stem+outfile_tail
	df.to_csv(outfile, index=False)

	#Save Standard Columns File
	keep_cols = ['cid', 'list_id', 'company', 'position', 'office',
				 'office_state', 'job_type', 'file_rank']
	outfile = stem+'.csv'
	df = df[keep_cols]
	df.to_csv(outfile, index=False)


combine_emp_keys()