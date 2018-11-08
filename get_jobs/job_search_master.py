import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd
import subprocess
from search_jobs import *
from filter_jobs import *
from get_jobs import *


##Take Master Company CSV, Make A Series of Two Col Company/JobType CSVs


def make_company_csvs(master_companies):

	#
	df = pd.read_csv(master_companies)
	cols = df.columns.values.tolist()
	cols.remove('company')

	company_csvs = []

	n = 1
	for k in cols:

		#Filter Company and Job Type Cols
		job_col = 'job_type_{}'.format(n)
		keep_cols = ['company', job_col]
		df_out = df[keep_cols].copy()
		col_names = ['company', 'job_type']
		df_out.columns = col_names
		print(df_out.shape)

		#TODO
		#remove rows that have NAN job_type

		#Write Outfile
		outfile = "companies_{}.csv".format(n)
		company_csvs.append(outfile)
		df_out.to_csv(outfile, index=False)
		n+=1

	return company_csvs


def get_jobs_scraper(params,
					 cid,
					 output,
					 seconds,
					 pyver):

	    # Run Indeed Job Search
    get_jobs_cmd = "{} search_jobs.py -p {} -c {} -o {} -s {}".format(
                        									   pyver, 
                        									   params, 
                        									   cid, 
                        									   output, 
                        									   seconds)

    print(get_jobs_cmd)
    subprocess.call(get_jobs_cmd, shell=True)

#TODO Make One That Runs for List of Scraped CSVS...

def dedupe_company_jobs(df):

	#Make Rank
	gb = ['company']
	rc = 'job_type_rank'
	df['rank'] = df.groupby(gb)[rc].rank(method="first", ascending=True)


	#Filter Criteria
	keep_crit = (	( df['rank'] == 1) ) 
	df = df.loc[keep_crit]
	return df


def make_clean_df(df_in):

	#Sort by Job Type and Company
	df_in.sort_values(by=['job_type', 'company'], inplace=True)

	#Make Cleaned File
	keep_cols = ['company', 'position', 'office', 'office_state', 
			'job_type']
	df_tmp = df_in[keep_cols].copy().reset_index()

	# Add Company ID Column
	df_tmp['index'] = df_tmp.index
	cid = df_tmp.apply(make_cid, axis=1)
	df = pd.concat([cid, df_tmp[keep_cols]], axis=1)
	cols = ['cid', 'company', 'position', 'office', 'office_state', 
			'job_type']
	df.columns = cols
	return df

def main(master_company,
		 params,
		 cid,
		 output,
		 seconds,
		 pyver,
		 scrape=False):

	#Define Intermediate Output File
	f = "../employers_key_{}.csv".format(get_date())
	exists = os.path.isfile('./{}'.format(f))

	#Define Final Output File
	final_outfile = '../employers_key.csv'


	if scrape is True:

		company_csvs = make_company_csvs(master_company)
		print(company_csvs)

		for c in company_csvs:

			#Extract Job Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')

			#Run Webscraper for Each Company/Job Type CSV
			scraper_out = 'indeed_jobs_{}'.format(jt_rank)
			get_jobs_scraper(params, c, scraper_out, seconds, pyver)

			#Run Filter
			scraper_stem = scraper_out.replace('.csv', '')
			indeed_jobs = "{}_{}.csv".format(scraper_stem, get_date())
			filter_out = 'filtered_employers_{}.csv'.format(jt_rank)		
			df = get_employers(indeed_jobs, filter_out)

			#Add Column Job_Type_Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')
			df['job_type_rank'] = jt_rank

			#Create Appended DF
			if not exists:
				df.to_csv(f, index=False, header=True)
			else:
				df.to_csv(f, index=False, header=False, mode='a')
			

			#Dedupe the Filtered Jobs
			df = dedupe_company_jobs(df)

			#Clean Results and Reset CID
			df = make_clean_df(df)

			#Write Out Results
			df.to_csv(final_outfile, index=False, header=True)

	else:
		#Dedupe the Filtered Jobs
		#assert exists
		df = pd.read_csv(f)
		df = dedupe_company_jobs(df)
		#print(df)

		#Clean Results and Reset CID
		df = make_clean_df(df)
		print(df)		

		#Write Out Results
		df.to_csv(final_outfile, index=False, header=True)


	#TODO Function to Create A Master Errors
	#One that 
	#A takes the original master list less the above file to find missing companies






#Concat Into One File
if __name__=="__main__":
    parser = argparse.ArgumentParser()

    #Search Jobs Args
    parser.add_argument("-p", "--param", default='job_params.csv', type=str)
    parser.add_argument("-c", "--cid", default='companies.csv', type=str)
    parser.add_argument("-o", "--output", default='indeed_jobs', type=str)
    parser.add_argument("-s", "--seconds", default=5, type=int)

    #Get Jobs Args
    parser.add_argument("-py", "--pyver", default='python3', type=str)
    args = parser.parse_args()

    main('master_companies.csv', 
          args.param, 
          args.cid, 
          args.output, 
          args.seconds,
          args.pyver)


