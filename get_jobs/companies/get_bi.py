import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd


def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date


def rt(d):
	times = np.random.rand(1000)+np.random.rand(1000)+d
	return np.random.choice(times, 1).tolist()[0]


def get_companies(url):

	print('[*] extracting companies for business_insider url: {}'.format(url))

	d.get(url)

	#Companies
	pat = "//h2[@class='slide-title-text']"
	c_loc = "xpath", pat
	c_elm = d.find_elements(*c_loc)
	text_raw = [c.text for c in c_elm]

	#Isolate Companies and Ranks
	companies = [t.split('. ', 1)[1].split(' — ', 1)[0] for t in text_raw]
	ranks = [t.split('. ', 1)[0] for t in text_raw]

	#Make Data Frame
	df = pd.DataFrame({'company':companies, 'rank':ranks})

	#Add Company Type
	df['source'] = 'business_insider25'
	df['job_type'] = 'data_science'
	return df


def main(out='business_insider_jobs'):

	url = 'https://www.businessinsider.com/most-valuable-private-us-startups-2018-10'

	gdf = get_companies(url)
	gdf.drop_duplicates('company', inplace=True)
	print(gdf)
	
	#Output
	outfile = '{}_{}.csv'.format(out, get_date())
	gdf.to_csv(outfile, index=False)




if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", default='business_insider_jobs', type=str)
	args = parser.parse_args()
	
	#Start business_insider Scraper
	starttime=time.time()
	d = webdriver.Firefox()
	d.implicitly_wait(0)

	#Main business_insider Scraper
	main(args.output)		  
	time.sleep(rt(5))
	d.close()
