import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd



def rt(d):
    times = np.random.rand(1000)+np.random.rand(1000)+d
    return np.random.choice(times, 1).tolist()[0]


def url_str(text):
    text = text.replace(' ', '+')
    text = text.replace('&', '%26')
    text = text.replace("'", '%27')
    return text


def error_logger(company, job_keyword, url, date):
    outfile = 'error_no_results_{}.csv'.format(date)
    exists = os.path.isfile('./{}'.format(outfile))

    with open(outfile, "a") as f:
        writer = csv.writer(f)

        if exists:
            writer.writerow([company, job_keyword, url, date])
        else:
            writer.writerow(['company', 'job_keyword', 'url', 'date'])
            writer.writerow([company, job_keyword, url, date])

    f.close()
    return


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
    d.get(url)
    time.sleep(rt(seconds))
    return url


def indeed_home():
    url = "https://www.indeed.com/"
    d.get(url)
    time.sleep(rt(2))


def query_job_home(job_keyword, company, city=None):

    #What Job?
    search_what = "{} company:{}".format(job_keyword, company)
    what_job = d.find_element_by_xpath("//input[@id='text-input-what']")
    what_job.send_keys(search_what)
    time.sleep(rt(3))

    #Where?
    where_job = d.find_element_by_xpath("//input[@id='text-input-where']")
    time.sleep(rt(3))
    where_job.clear()
    where_job.send_keys("Anywhere")
    where_job.send_keys(Keys.RETURN)
    time.sleep(rt(2))


def query_job_search(job_keyword, company, city=None):

    #What Job?
    search_what = "{} company:{}".format(job_keyword, company)
    what_job = d.find_element_by_xpath("//input[@id='what']")
    what_job.clear()
    what_job.send_keys(search_what)
    what_job.send_keys(Keys.RETURN)
    time.sleep(rt(3))

    #Where?
    where_job = d.find_element_by_xpath("//input[@id='where']")
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
        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(rt(delay))




def find_css(element, css):
    return element.find_element_by_css_selector(css)


def load_job_tiles(counter, job_key, job_type, 
                   company, filestem='indeed_jobs'):

    #Job Posts
    #Source 1: Main Posts
    pat1 = "//div[@class='jobsearch-SerpJobCard   row  result clickcard']"
    main_post_loc = "xpath", pat1
    main_posts = d.find_elements(*main_post_loc)

    #Source 2: Last Post / First Post (If Only One Post Exists)
    p2_class = 'jobsearch-SerpJobCard lastRow  row  result clickcard'
    pat2 = "//div[@class='{}']".format(p2_class)
    last_post_loc = "xpath", pat2
    last_post = d.find_elements(*last_post_loc)

    #All Posts
    posts = main_posts+last_post

    #Job Names
    job_pat = "a[class='turnstileLink']"
    job_names = [find_css(j, job_pat).get_attribute('title') for j in posts]

    if len(job_names) >= 1:
        pass
    else:
        return False

    # Job Companies and Locations
    companies = [find_css(c, "span[class='company']").text for c in posts]
    locations = [find_css(l, "span[class='location']").text for l in posts]
    jobs = {'job':job_names,'company':companies,'location':locations}
    df = pd.DataFrame(jobs)

    #Pass Job Keyword and Job Type to Output File
    df['job_keyword'] = job_key
    df['job_type'] = job_type
    df['qry_company'] = company

    f = "{}_{}.csv".format(filestem, date)
    exists = os.path.isfile('./{}'.format(f))
    #print(exists)
    #if counter == 1:
    if not exists:
        df.to_csv(f, index=False, header=True)
        return True
    else:
        df.to_csv(f, index=False, header=False, mode='a')
        return True



def get_jobs(job_key, job_type, company, count, seconds, date):
    qry_url = qry_indeed_jobs(job_key, company, seconds)

    job_tiles = load_job_tiles(count, job_key, job_type, 
                               company, filestem=filestem)
    if job_tiles is True:
        pass
    else:
        print("[*] error searching for {} jobs at {}...".format(job_key, 
                                                                company))
        error_logger(company, job_key, qry_url, date)
        #import pdb; pdb.set_trace()





def iterator(row):
    company = row[0]
    job_type = row[1]
    keywords = ast.literal_eval(row[2])
    counter = row[3]
    #company_id = row[4]

    #print(row)

    qc = []
    n = len(keywords)
    try:

        is_collected = check_collected(company)
        if is_collected is True:
            print("company is already collected...")
            return
        else:
            for k in keywords:
                counter+=1
                print("[*] searching for {} jobs at {}...".format(k, company))
                
                get_jobs(k, job_type, company, counter, seconds, date)
                qc.append(k)

                if len(qc) == n:
                    #print("[*] adding {} to tmp_collected.csv...".format(company))
                    with open('tmp_collected.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row.tolist())

                        update_remaining_jobs(company)

                else:
                    pass


    except Exception as e:
        print('[*] ERROR: {}'.format(e))
        error_logger(company, k, search_url(company, k))
        return
        #pass



def update_remaining_jobs(company):

    df = pd.read_csv('tmp_to_collect.csv')
    to_collect = df[df.company != company]
    to_collect.to_csv('tmp_to_collect.csv', index=False)


def check_collected(company):

    df = pd.read_csv('tmp_collected.csv')
    collected = df[df.company == company]
    #print(collected)
    #print(collected.shape[0])
    if collected.shape[0] > 0:
        return True
    else:
        return False

def check_nan(df):
    return df.isnull().values.any()

def remaining_jobs(jobs, attempts):

    assert check_nan(jobs) == False

    if attempts == 0:
        print('first attempt to perform_job_search')
        #Jobs To Collect
        to_collect = jobs.copy()
        to_collect.to_csv('tmp_to_collect.csv', index=False)

        #Collected Jobs
        collected = jobs.copy().iloc[0:0]
        collected.to_csv('tmp_collected.csv', index=False)

    else:
        print('additional attempt to perform_job_search, attempt number: {}'.format(attempts))
        to_collect = pd.read_csv('tmp_to_collect.csv')
    
    return to_collect


def perform_job_search(jobs, date):
    print("[*] DEPLOYING JOB SEARCH")

    global attempts
    global complete

    try:

        to_collect = remaining_jobs(jobs, attempts)
        print(to_collect)
        to_collect.apply(iterator, axis=1)
        #import pdb; pdb.set_trace()

        #Inspect Results
        f = "{}_{}.csv".format(filestem, date)
        print(pd.read_csv(f))
        print("[*] successfully searched indeed jobs...experiment-on...")
        complete = True

    except:
        #import pdb; pdb.set_trace()
        print("[*] ERROR in Job Search")
        attempts+=1
        to_collect = remaining_jobs(jobs, attempts)
        print(to_collect)
        





if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str)
    parser.add_argument("-p", "--param", default='job_params.csv', type=str)
    parser.add_argument("-c", "--cid", default='companies.csv', type=str)
    parser.add_argument("-o", "--output", default='indeed_jobs', type=str)
    parser.add_argument("-s", "--seconds", default=5, type=int)
    args = parser.parse_args()
    
    #Start Get Jobs Scraper
    starttime=time.time()
    d = webdriver.Firefox()
    d.implicitly_wait(0)

    #Set Global Parameters
    global date
    global seconds
    global filestem
    global complete

    date = args.date
    seconds = args.seconds
    filestem = args.output
    complete = False
    attempts = 0

    #Create Master Collection File
    cid = pd.read_csv(args.cid)
    key = pd.read_csv(args.param)
    assert check_nan(cid) == False | check_nan(key) == False


    df = cid.merge(key, on='job_type')
    df = df.drop(['backup_keys'], axis=1)
    df['counter'] = df.index
    #df['cid'] = df.index

    #Run Main App
    #while complete is False:
    while attempts < 3 and complete is False:

        perform_job_search(df, date)
            
    time.sleep(rt(5))
    d.close()


    



