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
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp)


def remove_zip(text):
	tmp = re.sub(r'\d{5}(?:[-\s]\d{4})?', "", text)
	return re.sub(r'\s{2,}', " ", tmp).strip()


def comma_replace(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;._`|~\\[<=>@\\^-]', " , ", text)
    return re.sub(r'\s{2,}', " ", tmp)


def select_punct_strip(text):
	#exceptions:: / \ - &
    tmp = re.sub(r'[]\\?!#$%(){}+*:;,._`\\|~\\[<=>@\\^]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp)


def parens_content_replace(text):
	return re.sub(r'\(.*?\)', '', text)


def split_vars(ovar, nvar1, nvar2, delim, df):
	df[nvar1], df[nvar2] = df[ovar].str.split(delim, 1).str
	df[nvar1] = df[nvar1].str.strip()
	df[nvar2] = df[nvar2].str.strip()
	return df


def title_length(row, col='job'):
	return len(row[col])


def job_type_to_key(job_type, lower=True):
	if lower is True:
		return job_type.lower().replace('_', ' ')
	else:
		return job_type.replace('_', ' ')


def job_match(row, col='job_keyword', stem=False, n=4, inject=False):
	#Determine Type of Keyword
	#From a Row or Direct Inject
	if inject is False:
		job_type = row[col]
	else:
		job_type = col

	#Case for Job Search
	#Based on Case of Key
	if job_type.isupper():
		job = row['job']
		key = job_type_to_key(job_type, lower=False)
	else:
		job = row['job'].lower()
		key = job_type_to_key(job_type, lower=True)

	#Additional Term Cleaning
	job = remove_punct(remove_non_ascii_2(job))
	key = remove_punct(remove_non_ascii_2(key))

	#Isolate Stem
	if stem is True:
		if len(key) > 4:
			n = len(key)//3
			key = key[:-n]
		else:
			pass

	return key in job


def bkup_jobs(bkup_key, job, stem=False):

	if bkup_key.isupper():
		job = job
		key = job_type_to_key(bkup_key, lower=False)
	else:
		job = job.lower()
		key = job_type_to_key(bkup_key, lower=True)

	#Additional Term Cleaning
	job = remove_punct(remove_non_ascii_2(job))
	key = remove_punct(remove_non_ascii_2(key))

	#Isolate Stem
	if stem is True:
		if len(key) > 4:
			n = len(key)//3
			key = key[:-n]
		else:
			pass

	return key in job


def job_match_bkup(row, col='backup_keys'):

	bkup_keys = ast.literal_eval(row[col])
	job = row['job']

	#Result Original
	r1 = [bkup_jobs(key, job) for key in bkup_keys]

	#Result Stemmed
	r2 = [bkup_jobs(key, job, stem=True) for key in bkup_keys]

	results = r1+r2
	return any(results)
	

def bkup_job_iterator(df, keywords):

	bk = pd.DataFrame(index=df.index.copy())
	cols = []
	for k in keywords:

		#Full Key Search
		crit = df.apply(job_match, axis=1, col=k, inject=True)
		bk = pd.concat([bk, crit], axis=1)
		cols.append(k)

		#Stemmed Key Search
		if len(k) > 4:
			stem_n = len(k)//3
			crit = df.apply(job_match, axis=1, col=k, inject=True, 
						stem=True, n=stem_n)
			bk = pd.concat([bk, crit], axis=1)
			cols.append('{}_stemmed'.format(k))
		else:
			pass

	bk.columns = cols
	bk['bk_crit'] = bk.any(axis='columns')
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

def clean_company(row, col='web_company'):
	c = row[col]
	c = remove_non_ascii_2(c)	
	#c = remove_punct(c)
	c = select_punct_strip(c)

	if c.isupper() and len(c) > 4:
		c = c.title()

	return c


def company_match(row, 
				  qry_col='qry_company', 
				  res_col='company',
				  exact=True):
	'''qry_col = company queried for :: res_col = result from web'''

	qry_company = row[qry_col].lower()
	res_company = row[res_col].lower()

	if exact is True:
		if qry_company == res_company:
			return True	
		else:
			return False
	else:
		if qry_company != res_company and qry_company in res_company:
			return True
		else:
			return False


def index_to_n(index_number, letter='c'):

	#Set to 1 index versus 0
	i = int(index_number)+1

	#Return as String
	if i <= 9:
		return letter+'0'+str(i)
	else:
		return letter+str(i)


def make_cid(row):
	index = row['index']
	return index_to_n(index)


def job_selector(infile, job_cols):

	date = infile.split('.csv')[0].split('_')[2]
	outfile_all = 'all_filtered_jobs_{}.csv'.format(date)
	outfile_select = 'selected_filtered_jobs_{}.csv'.format(date)
	outfile_errors = 'errors_filtered_jobs_{}.csv'.format(date)

	#Select Infile
	df = merge_companies_job_params(infile)

	#Input Quality Check
	j = job_cols
	condition0 = ( ( len(j) == 2 ) )
	assert condition0, "please provide exactly two columns as a list"

	condition1 = ( 
					( len(j) == 2 ) & 
					( isinstance(j[0], str) is True ) &
					( isinstance(j[1], str) is True ) 
				 )
	assert condition1, "please provide only string columns in list"

	#Rename Company and Make Clean Company Column
	df.rename(columns={'company':'web_company'}, inplace=True)
	df['company'] = df.apply(clean_company, axis=1)

	#Match Companies
	df['cid_match'] = df.apply(company_match, axis=1, exact=True)
	df['maybe_cid_match'] = df.apply(company_match, axis=1, exact=False)

	#Summarize Company Matches

	#Exact Matches
	gb = ['qry_company']
	cm = 'cid_match'
	df['cid_match_count'] = df.groupby(gb)[cm].transform('sum')

	#Possible Matches
	cm = 'maybe_cid_match'
	df['maybe_cid_match_count'] = df.groupby(gb)[cm].transform('sum')


	#Intern Filter
	df['internship'] = False
	intern_crit = 	(
						df['job'].str.contains(r'([iI]nternship)(s*\W*(?!\w))') |
						df['job'].str.contains(r'([iI]ntern)(s*\W*(?!\w))') 

					)
	df.loc[intern_crit, 'internship'] = True


	#Find Ideal Jobs
	df['ideal_job'] = False
	ideal_crit = (
					(
					  df.apply(job_match, axis=1, col=j[0]) |
					  df.apply(job_match, axis=1, col=j[1]) |
					  df.apply(job_match, axis=1, col=j[0], stem=True) |
					  df.apply(job_match, axis=1, col=j[1], stem=True)
					) &
					( df['internship'] == False )
				 )	
	df.loc[ideal_crit, 'ideal_job'] = True

	#Summarize Ideal Jobs (How Many by Company)
	df['ideal_count'] = df.groupby(['qry_company'])['ideal_job'].transform('sum')



	#Perform Backup Jobs
	df['bkup_job'] = False
	bk_crit = df.apply(job_match_bkup, axis=1)
	df.loc[bk_crit, 'bkup_job'] = True

	#Ensure Backup Jobs Are True Only If Not Also Ideal Jobs
	df.loc[( df['ideal_job'] == True ), 'bkup_job'] = False

	#Remove Internships from Backup Jobs
	df.loc[( df['internship'] == True), 'bkup_job'] = False	

	#Summarize Backup Jobs (How Many by Company)
	df['bkup_count'] = df.groupby(['qry_company'])['bkup_job'].transform('sum')

	#Make Clean Location
	cl = 'clean_location'
	df[cl] = df.apply(clean_location, axis=1)

	#Bool City, ST Only
	df['is_ctyst'] = False
	ctyst_crit = (df[cl].str.contains(r'^(.+)[,\\s]+(.+?)([A-Z]{2})$'))
	df.loc[ctyst_crit, 'is_ctyst'] = True

	#New City, ST Columns
	df = split_vars('clean_location', 'office', 'office_state', ',', df)

	#TODO
	#Strip Whitespace from 'office' and 'office state'

	#Make Clean Job Column
	df['position'] = df.apply(clean_job, axis=1)

	#Calculate Job Description Length
	df['job_descr_len'] = df.apply(title_length, axis=1)

	#Ranking
	gb = ['qry_company', 'ideal_job', 'bkup_job', 'cid_match']
	rc = 'job_descr_len'
	df['rank'] = df.groupby(gb)[rc].rank(method="first", ascending=True)

	#Sort Values
	df.sort_values(by=['qry_company', 'ideal_job', 'rank'], inplace=True)
	df.to_csv(outfile_all, index=False)

	#Job Selection Criteria
	keep_crit = (	
					#Select Ideal Job w/ Shortest Title and City/State
					#Where Company Completely Matches
					(
						( df['ideal_count'] > 0 ) &
						( df['ideal_job'] == True ) &
						( df['is_ctyst'] == True) &
						( df['cid_match'] == True) &
						( df['rank'] == 1) 

					) ^

					#If No Company Completely Matches
					#Select Ideal Job w/ Shortest Title and City/State
					#Where Company Maybe Matches
					(
						( df['ideal_count'] > 0 ) &
						( df['ideal_job'] == True ) &
						( df['is_ctyst'] == True) &
						( df['cid_match'] == False) &
						( df['cid_match_count'] == 0) &
						( df['maybe_cid_match'] == True) &
						( df['maybe_cid_match_count'] > 0) &
						( df['rank'] == 1) 

					) ^

					#Otherwise
					#Select Backup Job w/ Shortest Title and City/State
					(
						( df['ideal_count'] == 0 ) &
						( df['bkup_count'] > 0 ) &
						( df['bkup_job'] == True ) &
						( df['ideal_job'] == False ) &
						( df['is_ctyst'] == True) &
						( df['rank'] == 1) &
						(
							( df['cid_match'] == True) |
							( df['maybe_cid_match'] == True)
						)		   
					)
				)

	#Log Companies Lacking an Ideal or Backup Job
	missing_jobs = 	(	
						(	#Either No Ideal & No Backup Job
							( df['ideal_count'] == 0 ) &
							( df['bkup_count'] == 0 ) 

						) |

						(	#OR No Company Match or Maybe Match
							( df['cid_match_count'] == 0 ) &
							( df['maybe_cid_match_count'] == 0 )
							
						) 

 
					)


	#Job Filter Null Results
	errors = df.loc[missing_jobs]
	if errors.shape[0] > 0:
		errors.to_csv(outfile_errors, index=False)
	else:
		pass


	#Keep Rows Matching Criteria
	df = df.loc[keep_crit]
	df.to_csv(outfile_select, index=False)
	return df


def merge_companies_job_params(jobsfile, 
							   job_params='job_params.csv'):
	
	jobs = pd.read_csv(jobsfile)
	key = pd.read_csv(job_params)
	df = jobs.merge(key, on='job_type')
	return df


def get_employers(infile, outfile=None):

	#Outfile
	if outfile is None:
		date = infile.split('.csv')[0].split('_')[2]
		outfile = '../employers_key.csv'

	jobs = job_selector(infile, ['job_type', 'job_keyword'])

	#Make Cleaned File
	keep_cols = ['qry_company', 'position', 'office', 'office_state', 
				 'job_type']
	df_tmp = jobs[keep_cols].copy().reset_index()

	# Add Company ID Column
	df_tmp['index'] = df_tmp.index
	cid = df_tmp.apply(make_cid, axis=1)
	df = pd.concat([cid, df_tmp[keep_cols]], axis=1)
	cols = ['cid', 'company', 'position', 'office', 'office_state', 
			'job_type']
	df.columns = cols
	print(df)

	df.to_csv(outfile, index=False)

	return df


#get_employers('indeed_jobs_4_2018-11-14.csv', 'filter_test.csv')
