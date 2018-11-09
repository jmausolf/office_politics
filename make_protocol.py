import ast, csv, os, pdb
import numpy as np
import pandas as pd


#Start with Employers.CSV
emp = pd.read_csv('employers_key.csv', converters={'office_state': str})
print(emp)
print(emp.dtypes)


#0a TODO Join with Contact Name/Email by Company

#0b TODO Map `region` and `proximal_region` from `office_state` col
def get_region(df, state_col):

	pass
	return df

def get_prox_region(df, state_col):

	pass
	return df

def get_regions(df, state_col, region_key='region_key.csv'):

	regions = pd.read_csv(region_key, converters={'state': str})
	print(regions.dtypes)
	print(regions)
	x = df.merge(regions, how='left', left_on='office_state', right_on='state')
	#x = df.merge(regions, how='left')
	print(x)
	#df = get_region(df, state_col)
	#df = get_prox_region(df, state_col)
	x.to_csv('test_regions.csv', index=False)

	#TODO fix company state cleaning to strip forward whitespace

	return df





###########
###########
get_regions(emp, 'office_state')


#TODO
#Generate Pairs (Duplicate Each Row)
#(Sort by contact name, contact email, cid)

#TODO
#Number all rows by id, a1, a2, ...

#TODO
#Assign a `profile` to each row through random selection
#look at Rscript, just use that or do in Python??
