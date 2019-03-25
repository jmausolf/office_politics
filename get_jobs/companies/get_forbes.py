import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ast, csv, os, pdb
import numpy as np
import pandas as pd



def get_date():
	#Get Date for Filenames
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	return date


def rt(dtime):
	times = np.random.rand(1000)+np.random.rand(1000)+dtime
	return np.random.choice(times, 1).tolist()[0]


def show_all():

	#Button Pattern
	pat = "//button[@class='ng-binding']"
	button_loc = "xpath", pat
	button = d.find_element(*button_loc)

	#Navigate to Button
	actions.move_to_element_with_offset(button, 0, 50).perform()
	button.send_keys(Keys.UP)
	button.send_keys(Keys.UP)
	button.send_keys(Keys.UP)

	#Click and Sleep
	button.click()
	time.sleep(rt(5))


def get_companies(url):

	print('[*] extracting companies for forbes url: {}'.format(url))

	#Get Url
	try:
		d.set_page_load_timeout(15)
		d.get(url)
	except Exception:
		print('[*] page slow to load, consider clicking to stop browser...')
		print('[*] please continue in debugger mode...')
		print('[*] after stopping browser, enter [c]...')
		import pdb; pdb.set_trace()

	#Show All Companies
	show_all()

	#Companies
	c_elm = d.find_elements_by_css_selector("td:nth-child(2)")
	companies = [c.find_element_by_css_selector('a').text for c in c_elm]

	#Ranks
	r_elm = d.find_elements_by_css_selector("td:nth-child(1)")
	ranks = [r.find_element_by_css_selector('div').text for r in r_elm]

	#Make Data Frame
	df = pd.DataFrame({'company':companies, 'rank':ranks})

	#Add Company Type
	df['source'] = 'forbes_cloud100'
	df['job_type'] = 'data_science'
	return df


def main(out='forbes_jobs'):

	url = 'https://www.forbes.com/cloud100/'

	gdf = get_companies(url)
	gdf.drop_duplicates('company', inplace=True)
	print(gdf)
	
	#Output
	outfile = '{}_{}.csv'.format(out, get_date())
	gdf.to_csv(outfile, index=False)




if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", default='forbes_jobs', type=str)
	args = parser.parse_args()
	
	#Start forbes Scraper
	starttime=time.time()
	d = webdriver.Firefox()
	d.implicitly_wait(0)
	actions = ActionChains(d)

	#Main forbes Scraper
	main(args.output)		  
	time.sleep(rt(5))
	d.close()
