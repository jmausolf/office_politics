import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd




vault_keys = 	[
					['law/vault-law-100', '10'],
					['consulting/vault-consulting-50', '5'],
					['consulting/best-boutique-consulting-firms', '3'],
					['banking/vault-banking-50', '5'],
					['accounting/vault-accounting-50/', '5']

				]




def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date


def rt(d):
	times = np.random.rand(1000)+np.random.rand(1000)+d
	return np.random.choice(times, 1).tolist()[0]


def scroll_page(n, delay=0.25):
	scroll = 0
	for i in range(1, n+1):
		scroll +=1
		js = "window.scrollTo(0, document.body.scrollHeight);"
		driver.execute_script(js)
		time.sleep(rt(delay))


def vault_url(key):

	rank_list, pages = key[0], key[1]
	stem = 'http://www.vault.com/company-rankings/'
	url = stem+'{}/?pg={}'.format(rank_list, pages)
	return url 


def get_vault_urls(vault_keys):

	urls = []
	for key in vault_keys:
		url = vault_url(key)
		urls.append(url)
	return urls


def extract_source(url):
	stem = 'http://www.vault.com/company-rankings/'
	vault_list = url.split(stem)[1].split('/')[1]
	if vault_list == 'best-boutique-consulting-firms':
		vault_list = 'vault-'+vault_list
	else:
		pass

	return vault_list


def extract_type(url):
	stem = 'http://www.vault.com/company-rankings/'
	cid_type = url.split(stem)[1].split('/')[0]
	return cid_type


def get_companies(url):

	print('[*] extracting companies for Vault url: {}'.format(url))

	d.get(url)

	#Companies
	pat = "//td[@class='infoColumn']"
	c_loc = "xpath", pat
	c_elm = d.find_elements(*c_loc)
	companies = [c.find_element_by_css_selector('h3').text for c in c_elm]

	#Ranks
	pat = "//td[@class='rankColumn']"
	r_loc = "xpath", pat
	r_elm = d.find_elements(*r_loc)
	ranks = [r.find_element_by_css_selector('span').text for r in r_elm]

	#Make Data Frame
	df = pd.DataFrame({'company':companies, 'rank':ranks})

	#Add Company Type
	df['source'] = extract_source(url)
	df['job_type'] = extract_type(url)
	return df


def main(vault_keys, out='vault_jobs'):

	urls = get_vault_urls(vault_keys)
	vault_dfs = []

	for url in urls:

		vault_dfs.append(get_companies(url))
		time.sleep(rt(5))

	vdf = pd.concat(vault_dfs, axis=0, ignore_index=True)
	vdf.drop_duplicates('company', inplace=True)
	print(vdf)
	
	#Output
	outfile = '{}_{}.csv'.format(out, get_date())
	vdf.to_csv(outfile, index=False)




if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", default='vault_jobs', type=str)
	args = parser.parse_args()
	
	#Start Vault Scraper
	starttime=time.time()
	d = webdriver.Firefox()
	d.implicitly_wait(0)

	#Main Vault Scraper
	main(vault_keys, args.output)		  
	time.sleep(rt(5))
	d.close()
