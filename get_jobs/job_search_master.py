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
	#output_stems

	#print(cols)
	n = 1
	for k in cols:

		#Filter Company and Job Type Cols
		job_col = 'job_type_{}'.format(n)
		keep_cols = ['company', job_col]
		df_out = df[keep_cols].copy()
		col_names = ['company', 'job_type']
		df_out.columns = col_names
		print(df_out.shape)
		#print(df_out)

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

def main(master_company,
		 params,
		 cid,
		 output,
		 seconds,
		 pyver):


	company_csvs = make_company_csvs(master_company)
	print(company_csvs)

	for c in company_csvs:

		#Extract Job Rank
		jt_rank = c.replace('companies_', '').replace('.csv', '')


		#Run Webscraper for Each Company/Job Type CSV
		#(only need a filestem)
		scraper_out = 'indeed_jobs_{}'.format(jt_rank)
		#print(scraper_out)
		#ws_out = c.replace('companies_', 'indeed_jobs_')
		get_jobs_scraper(params, c, scraper_out, seconds, pyver)

		#Run Filter
		scraper_stem = scraper_out.replace('.csv', '')
		indeed_jobs = "{}_{}.csv".format(scraper_stem, get_date())
		#print(indeed_jobs)
		filter_out = 'filtered_employers_{}.csv'.format(jt_rank)
		#print(filter_out)
		#filter_out = c.replace('companies_', 'filtered_employers_')
		
		
		df = get_employers(indeed_jobs, filter_out)

		#Add Column Job_Type_Rank
		jt_rank = c.replace('companies_', '').replace('.csv', '')
		df['job_type_rank'] = jt_rank

		#Create Appended DF
		f = "../employers_key_{}.csv".format(get_date())
		exists = os.path.isfile('./{}'.format(f))
		if not exists:
			df.to_csv(f, index=False, header=True)
		else:
			df.to_csv(f, index=False, header=False, mode='a')
		






#For c in company_csvs, run search_jobs.py
	#run seach_jobs.py with given c.csv, at time run, spec output_stem
		#create outfile name == X
	#run filter(X, outfile=selected_employers_1, 2, 3...)
	#ALT
	#Create df
	# do return df
	#Create/Append rows to df created file

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

    '''
    # Run Indeed Job Search
    get_jobs_cmd = "{} search_jobs.py -p {} -c {} -o {} -s {}".format(
                                                    args.pyver, 
                                                    args.param, 
                                                    args.cid, 
                                                    args.output, 
                                                    args.seconds)

    print(get_jobs_cmd)
    subprocess.call(get_jobs_cmd, shell=True)

    # Filter Indeed Jobs
    indeed_jobs = "{}_{}.csv".format(args.output, get_date())
    get_employers(indeed_jobs)
    '''

