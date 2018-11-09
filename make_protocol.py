import ast, csv, os, pdb
import numpy as np
import pandas as pd


#Start with Employers.CSV
#print(emp)


#0a TODO Join with Contact Name/Email by Company


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


def make_pairs(df):

	second_pair = df.copy()
	df = df.append(second_pair, ignore_index=True)
	df.sort_values(by=['cid'], inplace=True)
	return df




emp = pd.read_csv('employers_key.csv')
emp = get_regions(emp, 'office_state')
emp = make_pairs(emp)
print(emp)



#TODO
#Number all rows by id, a1, a2, ...

#TODO
#Assign a `profile` to each row through random selection
#look at Rscript, just use that or do in Python??

