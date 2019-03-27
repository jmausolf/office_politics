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


def error_logger(list_id, company, job_keyword, url, date):
    outfile = 'error_no_results_{}.csv'.format(date)
    exists = os.path.isfile('./{}'.format(outfile))

    with open(outfile, "a") as f:
        writer = csv.writer(f)

        if exists:
            writer.writerow([list_id, company, job_keyword, url, date])
        else:
            writer.writerow(['list_id', 'company', 'job_keyword', 'url', 'date'])
            writer.writerow([list_id, company, job_keyword, url, date])

    f.close()
    return


def search_url(job_keyword, company, isrecent, days):
    url_stem = "https://www.indeed.com/jobs?q="
    job = url_str(job_keyword)
    cid = "company%3A({})".format(url_str(company))
    loc = "l=Anywhere"
    jt = "jt=fulltime"
    qry = "{}+{}&{}&{}".format(job, cid, loc, jt)

    if isrecent is False:
        url = url_stem+qry
    else:
        recent = '&fromage={}'.format(days)
        url = url_stem+qry+recent

    return url


def qry_indeed_jobs(job_keyword, company, seconds, isrecent, days):
    url = search_url(job_keyword, company, isrecent, days)
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
                   company, list_id, filestem='indeed_jobs'):


    ##--------------------------
    ## Primary Unsponsored Jobs
    ##--------------------------

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

    #All Posts - Main
    posts1 = main_posts+last_post

    #Job Names Main
    job_pat1 = "a[class='turnstileLink']"
    job_names1 = [find_css(j, job_pat1).get_attribute('title') for j in posts1]


    ##--------------------------
    ## Sponsored Jobs
    ##--------------------------
    
    #Alt Source 1: Main
    pat3 = "//div[@class='jobsearch-SerpJobCard row  result clickcard']"
    alt_main_loc = "xpath", pat3
    alt_main = d.find_elements(*alt_main_loc)

    #Alt Source 2: Last
    pat4 = "//div[@class='jobsearch-SerpJobCard row sjlast result clickcard']"
    alt_last_loc = "xpath", pat4
    alt_last = d.find_elements(*alt_last_loc)

    posts2 = alt_main+alt_last

    job_pat2 = "a[class='jobtitle turnstileLink']"
    job_names2 = [find_css(j, job_pat2).get_attribute('title') for j in posts2]

    #Combined Jobs
    job_names = job_names1+job_names2

    if len(job_names) >= 1:
        pass
    else:
        return False

    # Primary Job Companies and Locations
    companies1 = [find_css(c, "span[class='company']").text for c in posts1]
    locations1 = [find_css(l, "span[class='location']").text for l in posts1]

    # Sponsored Job Companies and Locations
    companies2 = [find_css(c, "span[class='company']").text for c in posts2]
    locations2 = [find_css(l, "div[class='location']").text for l in posts2]

    companies = companies1+companies2
    locations = locations1+locations2

    jobs = {'job':job_names,'company':companies,'location':locations}
    df = pd.DataFrame(jobs)

    #Pass Job Keyword and Job Type to Output File
    df['job_keyword'] = job_key
    df['job_type'] = job_type
    df['qry_company'] = company
    df['list_id'] = list_id

    f = "{}_{}.csv".format(filestem, date)
    exists = os.path.isfile('./{}'.format(f))
    if not exists:
        df.to_csv(f, index=False, header=True)
        return True
    else:
        df.to_csv(f, index=False, header=False, mode='a')
        return True


def get_jobs(job_key, job_type, company,
             list_id, count, seconds, date,
             isrecent, days):
    qry_url = qry_indeed_jobs(job_key, company, seconds, isrecent, days)

    job_tiles = load_job_tiles(count,
                               job_key, 
                               job_type, 
                               company,
                               list_id,
                               filestem=filestem)
    if job_tiles is True:
        pass
    else:
        print("[*] error searching for {} jobs at {}...".format(job_key, 
                                                                company))
        error_logger(list_id, company, job_key, qry_url, date)


def iterator(row):
    list_id = row['list_id']
    company = row['company']
    job_type = row['job_type']
    keywords = ast.literal_eval(row['keywords'])
    counter = row['counter']

    #Display progress
    if counter > 1 and int(counter) % 100 == 0:
        print("\n[*] progress: searched for {} companies...\n".format(counter))
    else:
        pass

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
                
                get_jobs(k, job_type, company,
                         list_id, counter, seconds, date,
                         isrecent, days)
                qc.append(k)

                if len(qc) == n:
                    with open('tmp_collected.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row.tolist())

                        update_remaining_jobs(company)

                else:
                    pass


    except Exception as e:
        print('[*] ERROR: {}'.format(e))
        error_logger(list_id, company, k, search_url(k, company, False, 30))
        return


def update_remaining_jobs(company):
    df = pd.read_csv('tmp_to_collect.csv')
    to_collect = df[df.company != company]
    to_collect.to_csv('tmp_to_collect.csv', index=False)


def check_collected(company):

    df = pd.read_csv('tmp_collected.csv')
    collected = df[df.company == company]
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

        #Inspect Results
        f = "{}_{}.csv".format(filestem, date)
        print(pd.read_csv(f))
        print("[*] successfully searched indeed jobs...experiment-on...")
        complete = True

    except:
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
    parser.add_argument("-r", "--recent", default=False, action='store_true')
    parser.add_argument("-dy", "--days", default=30, type=int)
    args = parser.parse_args()
    
    #Start Get Jobs Scraper
    starttime=time.time()
    d = webdriver.Firefox()
    d.implicitly_wait(0)

    #Set Global Parameters
    global date
    global seconds
    global isrecent
    global days
    global filestem
    global complete

    date = args.date
    seconds = args.seconds
    isrecent = args.recent
    days = args.days
    filestem = args.output
    complete = False
    attempts = 0

    print(isrecent)
    print(days)

    #Create Master Collection File
    cid = pd.read_csv(args.cid)
    key = pd.read_csv(args.param)
    assert check_nan(cid) == False | check_nan(key) == False


    df = cid.merge(key, on='job_type')
    df = df.drop(['backup_keys'], axis=1)
    df['counter'] = df.index
    print(df)

    #Run Main App
    while attempts < 3 and complete is False:

        perform_job_search(df, date)
            
    time.sleep(rt(5))
    d.close()


    



