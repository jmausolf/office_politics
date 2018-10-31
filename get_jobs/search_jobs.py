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


def url_str(text):
    return text.replace(' ', '+')


def error_logger(company, job_keyword, url):
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


def load_job_cards(counter, job_key, job_type, filestem='indeed_jobs'):

    #Job Posts
    post_loc = "xpath", "//div[@class='  row  result clickcard']"
    posts = d.find_elements(*post_loc)

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

    f = "{}_{}.csv".format(filestem, get_date())
    if counter == 1:
        df.to_csv(f, index=False, header=True)
        return True
    else:
        df.to_csv(f, index=False, header=False, mode='a')
        return True


def get_jobs(job_key, job_type, company, count, seconds):
    qry_url = qry_indeed_jobs(job_key, company, seconds)

    if load_job_cards(count, job_key, job_type, filestem=filestem) is True:
        pass
    else:
        print("[*] error searching for jobs at {}...".format(company))
        error_logger(company, job_key, qry_url)
        #import pdb; pdb.set_trace()




def iterator(row):
    company = row[0]
    job_type = row[1]
    keywords = ast.literal_eval(row[2])
    counter = row[3]

    for k in keywords:
        counter+=1
        print("[*] searching for {} jobs at {}...".format(k, company))
        try:
            get_jobs(k, job_type, company, counter, seconds)
        except Exception as e:
            print('[*] ERROR: {}'.format(e))
            error_logger(company, k, search_url(company, k))
            continue


def perform_job_search(companies, job_params):
    print("[*] DEPLOYING JOB SEARCH")

    #Join Companies and Job Params, Drop Backup Keys
    cid = pd.read_csv(companies)
    key = pd.read_csv(job_params)
    df = cid.merge(key, on='job_type')
    df = df.drop(['backup_keys'], axis=1)

    try:
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
    global seconds
    global filestem
    seconds = args.seconds
    filestem = args.output

    #Run Main App
    perform_job_search(args.cid, args.param)
    time.sleep(rt(5))
    d.close()
    



