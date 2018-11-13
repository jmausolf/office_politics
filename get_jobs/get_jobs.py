import selenium, time, datetime, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ast, csv, os, pdb
import numpy as np
import pandas as pd
import subprocess
from search_jobs import *
from filter_jobs import *



if __name__=="__main__":
    parser = argparse.ArgumentParser()

    #Search Jobs Args
    parser.add_argument("-d", "--date", type=str)
    parser.add_argument("-p", "--param", default='job_params.csv', type=str)
    parser.add_argument("-c", "--cid", default='companies.csv', type=str)
    parser.add_argument("-o", "--output", default='indeed_jobs', type=str)
    parser.add_argument("-s", "--seconds", default=5, type=int)

    #Get Jobs Args
    parser.add_argument("-py", "--pyver", default='python3', type=str)
    args = parser.parse_args()


    # Run Indeed Job Search
    get_jobs_cmd = "{} search_jobs.py -p {} -c {} -o {} -s {}".format(
                                                    args.pyver,
                                                    args.date,
                                                    args.param, 
                                                    args.cid, 
                                                    args.output, 
                                                    args.seconds)

    print(get_jobs_cmd)
    subprocess.call(get_jobs_cmd, shell=True)

    # Filter Indeed Jobs
    indeed_jobs = "{}_{}.csv".format(args.output, get_date())
    get_employers(indeed_jobs)