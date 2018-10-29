import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re
from string import punctuation
import warnings

# Suppress Grouping Warning
warnings.filterwarnings("ignore", 'This pattern has match groups')


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)


def remove_punct(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', "", text)
    return re.sub(r'\s{2,}', " ", tmp)


def remove_zip(text):
	tmp = re.sub(r'\d{5}(?:[-\s]\d{4})?', "", text)
	return re.sub(r'\s{2,}', " ", tmp).strip()


def comma_replace(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;._`|~\\[<=>@\\^-]', ",", text)
    return re.sub(r'\s{2,}', " ", tmp)


def select_punct_strip(text):
	#exceptions:: / \ - &
    tmp = re.sub(r'[]\\?!#$%(){}+*:;,._`\\|~\\[<=>@\\^]', "", text)
    return re.sub(r'\s{2,}', " ", tmp)


def parens_content_replace(text):
	return re.sub(r'\(.*?\)', '', text)


def split_vars(ovar, nvar1, nvar2, delim, df):
    df[nvar1], df[nvar2] = df[ovar].str.split(delim, 1).str
    return df


def title_length(row, col='job'):
	return len(row[col])


def job_type_to_key(job_type):
	key = job_type.lower().replace('_', ' ')
	return key


def job_match(row, col='job_keyword', stem=False, n=4, inject=False):
	job = row['job'].lower()

	if inject is False:
		job_type = row[col]
	else:
		job_type = col

	key = job_type_to_key(job_type)

	#Additional Term Cleaning
	job = remove_punct(remove_non_ascii_2(job))
	key = remove_punct(remove_non_ascii_2(key))

	#Isolate Stem
	if stem is True:
		key = key[:-n]

	return key in job


def bk_or(*b):
             return (np.logical_or(*b))

def bkup_job_iterator(keywords, df):

	bk = pd.DataFrame(index=df.index.copy())
	#bk = df.copy()
	#bk_crit = []
	for k in keywords:

		crit = df.apply(job_match, axis=1, col=k, inject=True)
		#bk_crit.append(crit)

		bk = pd.concat([bk, crit], axis=1)

	bk.columns = keywords
	#print(bk)

	bk['bk_crit'] = bk.any(axis='columns')
	#print(bk)
	#print(len(bk_crit))
	#print(bk_crit)


	#eturn any(bk_crit)
	return bk.any(axis='columns')



def clean_location(row, col='location'):
	l = row[col]
	l = remove_non_ascii_2(l)
	l = parens_content_replace(l)
	l = remove_zip(l)
	return l


def clean_job(row, col='job'):
	job = row[col]

	#Additional Term Cleaning
	job = remove_non_ascii_2(job)
	job = parens_content_replace(job)

	#IF CITY exists in job, replace city with ''
	city = row['office']
	job = job.replace(city, '').strip().strip(punctuation)
	job = job.replace(', ', '- ')
	job = job.replace('- ', ' - ').replace(' -', ' - ')
	job = select_punct_strip(job)
	return job


def index_to_n(index_number):

	#Set to 1 index versus 0
	i = int(index_number)+1

	#Return as String
	if i <= 9:
		return 'c0'+str(i)
	else:
		return 'c'+str(i)


def make_cid(row):
	index = row['index']
	return index_to_n(index)


def job_selector(infile, job_cols):

	date = infile.split('.csv')[0].split('_')[2]
	outfile = 'filtered_jobs_{}.csv'.format(date)

	#Select Infile
	#df = pd.read_csv('indeed_jobs_2018-10-25.csv')
	df = pd.read_csv(infile)

	#Input Quality Check
	j = job_cols
	print(j)
	condition0 = ( ( len(j) == 2 ) )
	assert condition0, "please provide exactly two columns as a list"

	condition1 = ( 
					( len(j) == 2 ) & 
					( isinstance(j[0], str) is True ) &
					( isinstance(j[1], str) is True ) 
				 )
	assert condition1, "please provide only string columns in list"

	#Find Ideal Jobs
	df['ideal_job'] = False
	ideal_crit = (
				  df.apply(job_match, axis=1, col=j[0]) |
				  df.apply(job_match, axis=1, col=j[1]) |
				  df.apply(job_match, axis=1, col=j[0], stem=True) |
				  df.apply(job_match, axis=1, col=j[1], stem=True)
				 )
	df.loc[ideal_crit, 'ideal_job'] = True

	#Summarize Ideal Jobs (How Many by Company)
	df['ideal_count'] = df.groupby(['company'])['ideal_job'].transform('sum')



	#Make Clean Location
	cl = 'clean_location'
	df[cl] = df.apply(clean_location, axis=1)

	#Bool City, ST Only
	df['is_ctyst'] = False
	ctyst_crit = (df[cl].str.contains(r'^(.+)[,\\s]+(.+?)([A-Z]{2})$'))
	df.loc[ctyst_crit, 'is_ctyst'] = True

	#New City, ST Columns
	df = split_vars('clean_location', 'office', 'office_state', ',', df)

	#Make Clean Job Column
	df['position'] = df.apply(clean_job, axis=1)

	#Perform Secondary Jobs
	df['backup_job'] = False

	#bk_crit =  (
	#			df.apply(job_match, axis=1, col='Research', inject=True) |
	#			df.apply(job_match, axis=1, col='Data', inject=True)			
	#			)

	#print(type(bk_crit))
	#print(bk_crit)
	bk_crit = bkup_job_iterator(['Research', 'Data'], df)
	#bk_crit = df['position'].isin(['Research', 'Data Scientist', 'Data Science'])
	#print(bk_crit)
	#bk_crit = df.isin(bk)
	#df.loc[bk_crit, 'backup_job'] = True

	#bk_crit =  (
	#			df.apply(job_match, axis=1, col='Research', inject=True) |
	#			df.apply(job_match, axis=1, col='Data', inject=True)			
	#			)

	df.loc[bk_crit, 'backup_job'] = True

	#Calculate Job Description Length
	df['job_descr_len'] = df.apply(title_length, axis=1)

	#Ranking
	gb = ['company', 'ideal_job']
	rc = 'job_descr_len'
	df['rank'] = df.groupby(gb)[rc].rank(method="first", ascending=True)


	#Create New Column (Secondary)
	#In cases where an ideal job does not exist
	#Only create for rows where ideal_count == 0
	#which is only for companies where an ideal job dne
	#perhaps brainstorm related keys in the job_params file...

	#Sort Values
	df.sort_values(by=['company', 'ideal_job', 'rank'], inplace=True)
	df.to_csv('tmp.csv', index=False)

	#Job Selection Criteria
	keep_crit = (	
					#Select Ideal Job w/ Shortest Title and City/State
					(
						( df['ideal_count'] > 0 ) &
						( df['ideal_job'] == True ) &
						( df['is_ctyst'] == True) &
						( df['rank'] == 1) 

					) 

					#TODO Need Alt Criteria
					#IF ideal does not exist
					#Avoid equal treatment of conditions
					#Select Job w/ Shortest Title and City/State
					#(
					#	( df['ideal_count'] == 0 ) &
					#	( df['is_ctyst'] == True) &
					#	( df['rank'] == 1) 			   
					#)
					#pass
				)

	#Keep Rows Matching Criteria
	df = df.loc[keep_crit].reset_index()

	print(df)
	df.to_csv(outfile, index=False)
	return df




def get_employers(infile, outfile=None):

	#Outfile
	if outfile is None:
		date = infile.split('.csv')[0].split('_')[2]
		outfile = '../employers_key.csv'

	jobs = job_selector(infile, ['job_type', 'job_keyword'])

	#print(df)


	#Make Cleaned File
	keep_cols = ['company', 'position', 'office', 'office_state']
	df_tmp = jobs[keep_cols].copy()

	# Add Company ID Column
	df_tmp['index'] = df_tmp.index
	cid = df_tmp.apply(make_cid, axis=1)
	df = pd.concat([cid, df_tmp[keep_cols]], axis=1)
	cols = ['cid', 'company', 'position', 'office', 'office_state']
	df.columns = cols
	print(df)

	df.to_csv(outfile, index=False)


#get_employers('indeed_jobs_2018-10-25.csv')
get_employers('indeed_jobs_test.csv')





