import random
import pandas as pd
import subprocess
import os
import inspect
import textile
import re
import csv
import argparse
from internship_key import internship_keys



def compile_xelatex(path, tex_file):
	owd = os.getcwd()
	os.chdir(path)
	subprocess.call("xelatex {}".format(tex_file), shell=True)
	os.chdir(owd)


def remove_non_ascii_2(text):
	import re
	return re.sub(r'[^\x00-\x7F]+', "", text)


def read_tex(tex_file):
	text = str(tex_file)
	f = open(text, 'rU').read()
	return remove_non_ascii_2(f)


def rep_pair(r, list_pair):
	return r.replace(list_pair[0], list_pair[1])


def article_strip(school):
	stmp = school.lower().replace('the ', '').title()
	clean_school = re.sub(r"\s{2,}", ' ', stmp).lstrip(' ')
	return clean_school


def modify_resume(path, tex_file, pairs, name, replace=False):

	infile = "{}/{}".format(path, tex_file)

	#load tex resume and modify
	r = read_tex(infile)
	for pair in pairs:
		r = rep_pair(r, pair)
		
	#write results
	if replace is True:
		output = open(infile, "w")
	else:
		outfile = "Resume_{}.tex".format(name.replace(' ', '_'))
		output = open("{}/{}".format(path, outfile), "w")
	
	output.write(r)
	output.close()


def make_resume_pairs(
					profile,
					job_type,
					name, 
					phone,
					gmail_user,
					school, 
					school_ctyst,
					school_cszip,
					school_address,
					department,
					ba_school, 
					ba_ctyst, 
					internship1,
					int1_ctyst,
					internship2,
					int2_ctyst,
					treatment 
					):


	keys = ["GRADSCHOOL", "GS_CITYSTATE", "GS_CSZIP", "GS_ADDRESS", "GADEPARTMENT",
			"UGSCHOOL", "UG_CITYSTATE",
			"INTERNSHIP1", "IC1_CITYSTATE", "INTERNSHIP2", "IC2_CITYSTATE",
			"TREATMENT", "ID_NAME", "ID_PHONE", "ID_EMAIL"]

	vals = [school, school_ctyst, school_cszip, school_address, department,
			ba_school, ba_ctyst,
			internship1, int1_ctyst, internship2, int2_ctyst,
			treatment, name, phone, gmail_user]


	resume_pairs = list(map(list, zip(keys, vals)))
	return resume_pairs


def make_resume(profile,
				job_type,
				name, 
				phone,
				gmail_user,
				school, 
				school_ctyst,
				school_cszip,
				school_address,
				department,
				ba_school, 
				ba_ctyst, 
				internship1,
				int1_ctyst,
				internship2,
				int2_ctyst,
				treatment):

	#Remove Articles from School Name
	school_clean = article_strip(school)

	rp = make_resume_pairs(profile,
					job_type,
					name, 
					phone,
					gmail_user,
					school_clean, 
					school_ctyst,
					school_cszip,
					school_address,
					department,
					ba_school, 
					ba_ctyst, 
					internship1,
					int1_ctyst,
					internship2,
					int2_ctyst,
					treatment)


	path = "{}/{}/tex".format(profile, job_type)

	outfile = "Resume_{}.tex".format(name.replace(' ', '_'))
	modify_resume(path, "resume_template.tex", rp, name)

	#compile new resume
	compile_xelatex(path, outfile)




