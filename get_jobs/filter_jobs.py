import ast, csv, os, pdb
import numpy as np
import pandas as pd


df = pd.read_csv('indeed_jobs_2018-10-22.csv')
print(df)
print(df.shape)


#Isolate City, ST


#Isolate City


#Filter Job (Search for Exact or Ideal Term)
#TODO (Insert Ideal Term into CSV in GETJOBS.PY)

def title_length():
	#gen a numeric column with the str count of characters of the job title
	#df['job_char'] = df['job'].str.len()
	pass


def ideal_job(df, job_type):

	df['ideal_job'] = False
	#jobtype col == ?

	#ideal criteria
	ideal_crit = ((df[job_type].str.contains(job_type)))
	df.loc[ideal_crit, ideal_job] = True