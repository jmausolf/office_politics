import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re


#Rules:
'''
Hopefully there is at least one job (or 15) per company
Would like to keep the best job option
Ideal job would match the job description (have the type/key in job title)
Job title would be short






'''

df = pd.read_csv('indeed_jobs_2018-10-25.csv')
#print(df)
#print(df.shape)


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


#Isolate City, ST

#^(.+)[,\\s]+(.+?)([A-Z]{2})$
#Isolate City
def split_vars(ovar, nvar1, nvar2, delim, df):
    df[nvar1], df[nvar2] = df[ovar].str.split(delim, 1).str
    #df.drop([ovar], axis=1, inplace=True)
    return df


#Filter Job (Search for Exact or Ideal Term)
#TODO (Insert Ideal Term into CSV in GETJOBS.PY)

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

	#Additional Term Cleaning
	l = remove_non_ascii_2(l)
	l = parens_content_replace(l)
	l = remove_zip(l)

	return l


def clean_job(row, col='job'):
	job = row[col]

	#Additional Term Cleaning
	job = remove_non_ascii_2(job)
	job = parens_content_replace(job)

	#TODO IF CITY exists in job, replace city with ''

	job = job.replace(', ', '- ')
	job = job.replace('- ', ' - ').replace(' -', ' - ')
	job = select_punct_strip(job)
	#job = comma_rep(remove_non_ascii_2(job)).title()
	#print(job)
	return job




def job_selector(df, job_cols):

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

	#Make Clean Location
	cl = 'clean_location'
	df[cl] = df.apply(clean_location, axis=1)

	#Bool City, ST Only
	df['is_ctyst'] = False
	ctyst_crit = (df[cl].str.contains(r'^(.+)[,\\s]+(.+?)([A-Z]{2})$'))
	df.loc[ctyst_crit, 'is_ctyst'] = True

	#New City, ST Columns
	#df['office'], df['office_state'] = df[''].str.split(delim, 1).str

	df = split_vars('clean_location', 'office', 'office_state', ',', df)

	#Make Clean Job Column
	df['clean_job'] = df.apply(clean_job, axis=1)

	#Calculate Job Description Length
	df['job_descr_len'] = df.apply(title_length, axis=1)


	#Ranking
	df['rank'] = df.groupby(['company', 'ideal_job'])['job_descr_len'].rank(method="first", ascending=True)

	df.sort_values(by=['company', 'ideal_job', 'rank'], inplace=True)


	print(df)
	df.to_csv('test.csv')
	return df



job_selector(df, ['job_type', 'job_keyword'])
#ideal_job(df, ['job_type'])