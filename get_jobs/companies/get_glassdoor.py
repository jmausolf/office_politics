import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd




url_keys = {
			'Best-Places-to-Work-LST_KQ0,19.htm':'large',
			'Best-Small-and-Medium-Companies-to-Work-For-LST_KQ0,43.htm': 
				'med_small'
		  }


def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date


def rt(d):
	times = np.random.rand(1000)+np.random.rand(1000)+d
	return np.random.choice(times, 1).tolist()[0]


def glassdoor_url(key):

	stem = 'https://www.glassdoor.com/Award/'
	url = stem+'{}'.format(key)
	return url 


def get_glassdoor_urls(url_keys):

	urls = []
	for key, val in url_keys.items():
		url = glassdoor_url(key)
		urls.append(url)
	return urls


def extract_source(url):

	stem = 'https://www.glassdoor.com/Award/'
	key = url.split(stem)[1]
	return 'glassdoor_{}'.format(url_keys[key])


def get_companies(url):

	print('[*] extracting companies for glassdoor url: {}'.format(url))

	d.get(url)

	#Companies
	pat = "//div[@class='bptwSingle w-100 ']"
	c_loc = "xpath", pat
	c_elm = d.find_elements(*c_loc)
	companies = [c.find_element_by_css_selector('p').text for c in c_elm]

	#Ranks
	ranks_raw = [c.find_element_by_css_selector('span').text for c in c_elm]
	ranks_clean = [r.split('#')[1] for r in ranks_raw]

	#Make Data Frame
	df = pd.DataFrame({'company':companies, 'rank':ranks_clean})

	#Add Company Type
	df['source'] = extract_source(url)
	df['job_type'] = 'data_science'
	return df


def main(url_keys, out='glassdoor_jobs'):

	urls = get_glassdoor_urls(url_keys)
	glassdoor_dfs = []

	for url in urls:

		glassdoor_dfs.append(get_companies(url))
		time.sleep(rt(5))

	gdf = pd.concat(glassdoor_dfs, axis=0, ignore_index=True)
	gdf.drop_duplicates('company', inplace=True)
	print(gdf)
	
	#Output
	outfile = '{}_{}.csv'.format(out, get_date())
	gdf.to_csv(outfile, index=False)




if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", default='glassdoor_jobs', type=str)
	args = parser.parse_args()
	
	#Start glassdoor Scraper
	starttime=time.time()
	d = webdriver.Firefox()
	d.implicitly_wait(0)

	#Main glassdoor Scraper
	main(url_keys, args.output)		  
	time.sleep(rt(5))
	d.close()
