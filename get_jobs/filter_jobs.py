import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re


df = pd.read_csv('indeed_jobs_2018-10-25.csv')
#print(df)
#print(df.shape)


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)

def remove_punct(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', "", text)
    return re.sub(r'\s{2,}', " ", tmp)

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


#Isolate City


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


def clean_job(row, col='job'):
	job = row[col]

	#Additional Term Cleaning
	job = remove_non_ascii_2(job)
	job = parens_content_replace(job)
	job = job.replace(', ', '- ')
	job = job.replace('- ', ' - ').replace(' -', ' - ')
	job = select_punct_strip(job)
	#job = comma_rep(remove_non_ascii_2(job)).title()
	#print(job)
	return job



def ideal_job(df, job_cols):
	j = job_cols
	condition0 = ( ( len(j) == 2 ) )
	assert condition0, "please provide exactly two columns as a list"


	condition1 = ( 
					( len(j) == 2 ) & 
					( isinstance(j[0], str) is True ) &
					( isinstance(j[1], str) is True ) 
				 )
	assert condition1, "please provide only string columns in list"

	df['ideal_job'] = False
	ideal_crit = (
				  df.apply(job_match, axis=1, col=j[0]) |
				  df.apply(job_match, axis=1, col=j[1]) |
				  df.apply(job_match, axis=1, col=j[0], stem=True) |
				  df.apply(job_match, axis=1, col=j[1], stem=True)
				 )
	df.loc[ideal_crit, 'ideal_job'] = True

	df['clean_job'] = df.apply(clean_job, axis=1)

	df['job_descr_len'] = df.apply(title_length, axis=1)

	print(df)
	df.to_csv('test.csv')
	return df



ideal_job(df, ['job_type', 'job_keyword'])
#ideal_job(df, ['job_type'])