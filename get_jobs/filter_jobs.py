import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re
from string import punctuation
import warnings

# Suppress Grouping Warning
warnings.filterwarnings("ignore", 'This pattern has match groups')

#Rules:
'''
Hopefully there is at least one job (or 15) per company
Would like to keep the best job option
Ideal job would match the job description (have the type/key in job title)
Job title would be short






'''





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
	#gen a numeric column with the str count of characters of the job title
	#df['job_char'] = df['job'].str.len()
	return len(row[col])


def job_type_to_key(job_type):
	key = job_type.lower().replace('_', ' ')
	return key


def job_match(row, col='job_keyword', stem=False, n=4):
	job = row['job'].lower()
	job_type = row[col]
	key = job_type_to_key(job_type)

	#Additional Term Cleaning
	job = remove_punct(remove_non_ascii_2(job))
	key = remove_punct(remove_non_ascii_2(key))

	#Isolate Stem
	if stem is True:
		key = key[:-n]

	return key in job


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


def job_selector(infile, job_cols):

	date = infile.split('.csv')[0].split('_')[2]
	outfile = 'filtered_jobs_{}.csv'.format(date)

	#Select Infile
	#df = pd.read_csv('indeed_jobs_2018-10-25.csv')
	df = pd.read_csv(infile)

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

	#Calculate Job Description Length
	df['job_descr_len'] = df.apply(title_length, axis=1)

	#Ranking
	gb = ['company', 'ideal_job']
	rc = 'job_descr_len'
	df['rank'] = df.groupby(gb)[rc].rank(method="first", ascending=True)

	#Sort Values
	df.sort_values(by=['company', 'ideal_job', 'rank'], inplace=True)

	#Job Selection Criteria
	keep_crit = (
					#Ideal Count >=1
					(
						( df['ideal_count'] > 0 ) &
						( df['ideal_job'] == True ) &
						( df['is_ctyst'] == True) &
						( df['rank'] == 1) 

					)

					#Ideal Count ==0
					#pass
				)

	#Keep Rows Matching Criteria
	df = df.loc[keep_crit].reset_index()

	#print(df)
	df.to_csv(outfile, index=False)
	return df

#job_selector(df, ['job_type', 'job_keyword'])

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

def employers(infile, outfile):

	#df = pd.read_csv(infile)
	date = infile.split('.csv')[0].split('_')[2]
	print(date)

	df = job_selector(infile, ['job_type', 'job_keyword'])

	#print(df)


	#Make Cleaned File
	keep_cols = ['company', 'position', 'office', 'office_state']
	df_clean = df[keep_cols].copy()

	# Add Company ID Column
	df_clean['index'] = df_clean.index
	df_clean['cid'] = df_clean.apply(make_cid, axis=1)
	df_clean.drop(['index'], axis=1, inplace=True)
	print(df_clean)

employers('indeed_jobs_2018-10-25.csv', 'indeed_jobs_2018-10-25')





