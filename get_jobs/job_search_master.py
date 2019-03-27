import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd
import subprocess
from search_jobs import *
from filter_jobs import *
from cleanup_files import *


def get_date():
    #Get Date for Filenames
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return date


def make_company_csvs(master_companies):

	#
	df = pd.read_csv(master_companies)
	print(df)
	cols = df.columns.values.tolist()

	#Remove All Non Job_Type Cols
	non_job_cols = ['list_id', 'company', 'rank', 'source']
	cols = [c for c in cols if c not in non_job_cols]
	company_csvs = []

	n = 1
	for k in cols:

		#Filter Company and Job Type Cols
		job_col = 'job_type_{}'.format(n)
		keep_cols = ['list_id', 'company', job_col]
		df_out = df[keep_cols].copy()
		col_names = ['list_id', 'company', 'job_type']
		df_out.columns = col_names

		#Remove Rows that have NAN job_type
		#(To Avoid Searching Certain Companies for Some Job Functions)
		df_out = df_out.dropna(axis=0, how='any')
		df_out.isna().sum()
		print(df_out.shape)

		#Write Outfile
		outfile = "companies_{}.csv".format(n)
		company_csvs.append(outfile)
		df_out.to_csv(outfile, index=False)
		n+=1

	return company_csvs


def get_jobs_scraper(date,
					 param,
					 cid,
					 output,
					 seconds,
					 pyver,
					 isrecent,
					 days):

	if isrecent is True:
		isrecent = '--recent'
	else:
		isrecent = ''

	# Run Indeed Job Search
	get_jobs_cmd = "{} search_jobs.py -d {} -p {} -c {} -o {} -s {} {} -dy {}".format(
				pyver,
				date,
				param, 
				cid, 
				output, 
				seconds,
				isrecent,
				days,
				)

	print(get_jobs_cmd)
	subprocess.call(get_jobs_cmd, shell=True)


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
	keep_cols = ['list_id', 'company', 'position', 'office', 'office_state', 
			'job_type']
	df_tmp = df_in[keep_cols].copy().reset_index(drop=True)

	# Add Company ID Column
	df_tmp['index'] = df_tmp.index
	cid = df_tmp.apply(make_cid, axis=1)
	df = pd.concat([cid, df_tmp[keep_cols]], axis=1)
	cols = ['cid', 'list_id', 'company', 'position', 'office', 'office_state', 
			'job_type']
	df.columns = cols
	return df


def company_error_check(master_company, final_df, fname, date):

	mc = master_company
	fo = final_df
	N = fo.shape[0]

	full_df = mc.merge(fo, how='left')
	errors = full_df[pd.isnull(full_df['job_type'])].reset_index(drop=True)
	errors = errors.drop(['cid', 'position',
						  'office', 'office_state', 'job_type'],
						  axis=1)
	n = errors.shape[0]

	if n > 0:
		#Error Firms
		print("[*] failed to find jobs for {} firms...".format(n))
		print(errors)
		outfile = 'total_errors_filtered_jobs_{}.csv'.format(date)
		print("[*] writing errors to {}...".format(outfile))
		errors.to_csv(outfile, index=False)

		#Found Firms
		print("[*] found jobs for {} firms, file: {}".format(N, fname))
		print(fo)
		print("[*] done.")


	else:
		#Found Firms
		print("[*] found jobs for all {} firms, file: {}".format(N, fname))
		print(fo)
		print("[*] done.")


def main(master_company,
		 date,
		 param,
		 cid,
		 output,
		 seconds,
		 pyver,
		 filter_only,
		 isrecent,
		 days):


	#Cleanup Files
	cleanup_files(date)

	#Define Intermediate Output File
	f = "../employers_key_{}.csv".format(date)
	exists = os.path.isfile('./{}'.format(f))

	#Define Final Output File
	final_outfile = '../keys/employers_key.csv'

	print("filter only is {}".format(filter_only))
	if filter_only is False:

		
		company_csvs = make_company_csvs(master_company)
		print(company_csvs)

		for c in company_csvs:

			#Extract Job Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')

			#Run Webscraper for Each Company/Job Type CSV
			scraper_out = 'indeed_jobs_{}'.format(jt_rank)
			get_jobs_scraper(date, param, c, scraper_out, 
							 seconds, pyver, isrecent, days)

			#Run Filter
			scraper_stem = scraper_out.replace('.csv', '')
			indeed_jobs = "{}_{}.csv".format(scraper_stem, date)
			filter_out = 'filtered_employers_{}.csv'.format(jt_rank)		
			df = get_employers(indeed_jobs, filter_out)

			#Add Column Job_Type_Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')
			df['job_type_rank'] = jt_rank

			#Create Appended DF
			exists = os.path.isfile('./{}'.format(f))
			if not exists:
				df.to_csv(f, index=False, header=True)
			else:
				df.to_csv(f, index=False, header=False, mode='a')
			

		#Dedupe the Filtered Jobs
		#import pdb; pdb.set_trace()
		df = pd.read_csv(f)
		df = dedupe_company_jobs(df)

		#Clean Results and Reset CID
		df = make_clean_df(df)

		#Write Out Results
		df.to_csv(final_outfile, index=False, header=True)
		
		#Error Check
		master_company = pd.read_csv(master_company)
		company_error_check(master_company, df, final_outfile, date)


	if filter_only is True:
		#Dedupe the Filtered Jobs
		#exists = os.path.isfile('./{}'.format(f))
		#assert exists is True, 'the expected job file does not exist...'+ \
		#		'rerun using scrape=True'


		company_csvs = make_company_csvs(master_company)
		print(company_csvs)

		for c in company_csvs:

			#Extract Job Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')

			#Run Filter
			scraper_out = 'indeed_jobs_{}'.format(jt_rank)
			scraper_stem = scraper_out.replace('.csv', '')
			indeed_jobs = "{}_{}.csv".format(scraper_stem, date)
			filter_out = 'filtered_employers_{}.csv'.format(jt_rank)		
			df = get_employers(indeed_jobs, filter_out)

			#Add Column Job_Type_Rank
			jt_rank = c.replace('companies_', '').replace('.csv', '')
			df['job_type_rank'] = jt_rank

			#Create Appended DF
			exists = os.path.isfile('./{}'.format(f))
			if not exists:
				df.to_csv(f, index=False, header=True)
			else:
				df.to_csv(f, index=False, header=False, mode='a')


		#Dedupe the Filtered Jobs
		df = pd.read_csv(f)
		df = dedupe_company_jobs(df)

		#Clean Results and Reset CID
		df = make_clean_df(df)

		#Write Out Results
		df.to_csv(final_outfile, index=False, header=True)
		
		#Error Check
		master_company = pd.read_csv(master_company)
		company_error_check(master_company, df, final_outfile, date)


	#Cleanup Files
	cleanup_files(date)



#Concat Into One File
if __name__=="__main__":
    parser = argparse.ArgumentParser()

    #Search Jobs Args
    parser.add_argument("-d", "--date", default=get_date(), type=str)
    parser.add_argument("-p", "--param", default='job_params.csv', type=str)
    parser.add_argument("-c", "--cid", default='companies.csv', type=str)
    parser.add_argument("-o", "--output", default='indeed_jobs', type=str)
    parser.add_argument("-sec", "--seconds", default=1, type=int)
    parser.add_argument("-filter", "--filter_only", default=False, action='store_true')
    parser.add_argument("-r", "--recent", default=False, action='store_true')
    parser.add_argument("-dy", "--days", default=30, type=int)

    #Get Jobs Args
    parser.add_argument("-py", "--pyver", default='python3', type=str)
    args = parser.parse_args()

    main('master_companies.csv',
    	  args.date,
          args.param, 
          args.cid, 
          args.output, 
          args.seconds,
          args.pyver,
          args.filter_only,
          args.recent,
          args.days)

    clean_cmd = '{} clean_emp_key.py'.format(args.pyver)
    subprocess.call(clean_cmd, shell=True)

