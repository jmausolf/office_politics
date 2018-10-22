import selenium, time, argparse
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import ast
import csv
import os
import pdb


def get_date():
    #Get Date for Filenames
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return date


def rt(d):
    times = np.random.rand(1000)+np.random.rand(1000)+d
    return np.random.choice(times, 1).tolist()[0]


def url_str(text):
    return text.replace(' ', '+')


def error_logger(company, job_keyword, url):

    pdb.set_trace()

    date = get_date()
    outfile = 'error_no_results_{}.csv'.format(date)
    exists = os.path.isfile('./{}'.format(outfile))

    with open(outfile, "a") as f:
        writer = csv.writer(f)

        if exists:
            writer.writerow([company, job_keyword, url, date])
        else:
            writer.writerow(['company', 'job_keyword', 'url', 'date'])
            writer.writerow([company, job_keyword, url, date])




def search_url(job_keyword, company):

    url_stem = "https://www.indeed.com/jobs?q="
    job = url_str(job_keyword)
    cid = "company%3A{}".format(url_str(company))
    loc = "l=Anywhere"
    jt = "jt=fulltime"
    qry = "{}+{}&{}&{}".format(job, cid, loc, jt)
    url = url_stem+qry
    return url


def qry_indeed_jobs(job_keyword, company, seconds):

    url = search_url(job_keyword, company)
    driver.get(url)
    time.sleep(rt(seconds))
    return url


def indeed_home():
    url = "https://www.indeed.com/"
    driver.get(url)
    time.sleep(rt(2))

def query_job_home(job_keyword, company, city=None):

    #pdb.set_trace()

    #What Job?
    search_what = "{} company:{}".format(job_keyword, company)
    what_job = driver.find_element_by_xpath("//input[@id='text-input-what']")
    what_job.send_keys(search_what)
    time.sleep(rt(3))

    #Where?
    where_job = driver.find_element_by_xpath("//input[@id='text-input-where']")
    time.sleep(rt(3))
    where_job.clear()
    where_job.send_keys("Anywhere")
    where_job.send_keys(Keys.RETURN)
    time.sleep(rt(2))



def query_job_search(job_keyword, company, city=None):

    #pdb.set_trace()

    #What Job?
    search_what = "{} company:{}".format(job_keyword, company)
    what_job = driver.find_element_by_xpath("//input[@id='what']")
    what_job.clear()
    what_job.send_keys(search_what)
    what_job.send_keys(Keys.RETURN)
    time.sleep(rt(3))

    #Where?
    where_job = driver.find_element_by_xpath("//input[@id='where']")
    time.sleep(rt(3))
    where_job.clear()
    where_job.send_keys("Anywhere")
    where_job.send_keys(Keys.RETURN)
    time.sleep(rt(2))


def scroll_page(n, delay=3):
    scroll = 0
    print("[*] scrolling through all items in closet...")
    for i in range(1, n+1):
        scroll +=1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(rt(delay))


def load_job_cards(counter, filestem='indeed_jobs'):

    #TODO
    #Try again if no posts/job names for query
    posts = driver.find_elements_by_xpath("//div[@class='  row  result clickcard']")
    job_names = [j.find_element_by_css_selector("a[class='turnstileLink']").get_attribute('title') for j in posts]
    #print(job_names)


    if len(job_names) >= 1:
        pass
    else:
        return False

    companies = [c.find_element_by_css_selector("span[class='company']").text for c in posts]

    locations = [l.find_element_by_css_selector("span[class='location']").text for l in posts]

    jobs = {'job':job_names,'company':companies,'location':locations}
    df = pd.DataFrame(jobs)

    f = "{}_{}.csv".format(filestem, get_date())

    if counter == 1:
        df.to_csv(f, index=False, header=True)
    else:
        df.to_csv(f, index=False, header=False, mode='a')

    return True



def get_jobs(job_keyword, company, counter, seconds):
    #pdb.set_trace()
    qry_url = qry_indeed_jobs(job_keyword, company, seconds)

    if load_job_cards(counter, filestem) is True:
        pass
    elif load_job_cards(counter, filestem) is False:
        print("[*] error searching for jobs at {}...".format(company))
        pdb.set_trace()
        error_logger(company, job_keyword, qry_url)
        pass


def iterator(row):
    #pdb.set_trace()
    company = row[0]
    job_type = row[1]
    keywords = ast.literal_eval(row[2])
    counter = row[3]

    #pdb.set_trace()

    for k in keywords:
        counter+=1
        #print(company, k, counter)
        print("[*] searching for {} jobs at {}...".format(k, company))
        try:
            get_jobs(k, company, counter, seconds)
        except Exception as e:
            print('[*] ERROR: {}'.format(e))
            error_logger(company, k, search_url(company, k))
            pass




def perform_job_search(job_params):
    print("[*] DEPLOYING JOB SEARCH")

    try:
        df = pd.read_csv(job_params)
        df['counter'] = df.index
        print(df)

        df.apply(iterator, axis=1)

        
        #Inspect Results
        f = "{}_{}.csv".format(filestem, get_date())
        print(pd.read_csv(f))
        print("[*] successfully searched indeed jobs...experiment-on...")
        pass

    except:
        print("[*] ERROR in Job Search")
        pass






if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", default=3600, type=float, help="time in seconds")
    parser.add_argument("-p", "--param", default='job_params.csv', type=str, help="name of job search parameters file")
    parser.add_argument("-o", "--output", default='indeed_jobs', type=str, help="name of output file stem")
    parser.add_argument("-s", "--seconds", default=5, type=int, help="number of seconds delay")
    args = parser.parse_args()

    #Start Share War Loop
    starttime=time.time()

    #while True:
    #Start Driver, Get URLS, Close
    driver = webdriver.Firefox()
    driver.implicitly_wait(0)

    #Time Delay: While Loop
    random_loop_time = rt(args.time)

    #Set Global Parameters
    global seconds
    global filestem
    seconds = args.seconds
    filestem = args.output

    #Run Main App
    perform_job_search(args.param)

    #pdb.set_trace()


    time.sleep(rt(5))
    driver.close()




