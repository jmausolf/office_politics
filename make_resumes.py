import random
import pandas as pd
import subprocess
import os
import inspect
import textile
import re
import csv
import argparse



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
	s = school.lower().replace('the ', '').title()
	s = ' '.join([w.lower() if len(w) <=2 else w for w in s.split(' ')])
	clean_school = re.sub(r"\s{2,}", ' ', s).lstrip(' ')
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
		clean_name = name.replace(' ', '_').replace('.', '')
		outfile = "Resume_{}.tex".format(clean_name)
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
					int1_title,
					internship2,
					int2_ctyst,
					int2_title,
					treatment 
					):


	keys = ["GRADSCHOOL", "GS_CITYSTATE", "GS_CSZIP", "GS_ADDRESS", "GADEPARTMENT",
			"UGSCHOOL", "UG_CITYSTATE",
			"INTERNSHIP1", "IC1_CITYSTATE", "INT1TITLE",
			"INTERNSHIP2", "IC2_CITYSTATE", "INT2TITLE",
			"TREATMENT", "ID_NAME", "ID_PHONE", "ID_EMAIL"]

	vals = [school, school_ctyst, school_cszip, school_address, department,
			ba_school, ba_ctyst,
			internship1, int1_ctyst, int1_title,
			internship2, int2_ctyst, int2_title,
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
				int1_title,
				internship2,
				int2_ctyst,
				int2_title,
				treatment,
				pair_version):

	#Remove Articles from School Name
	school_clean = article_strip(school)

	#TODO
	#Make Internship Companies Latex Safe
	#e.g. \textsc{Bain & Company} fails
	#e.g Bryan School of Business & Economics fails
	#funct to replace & with \&


	#Set Path
	path = "{}/{}/tex".format(profile, job_type)

	#Select Resume Version
	if pair_version == 'A':
		resume_infile = "resume_template_A.tex"
	elif pair_version == 'B':
		resume_infile = "resume_template_B.tex"
		#phone = '({}'.format(phone.replace('-', ') ', 1))

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
					int1_title,
					internship2,
					int2_ctyst,
					int2_title,
					treatment)

	clean_name = name.replace(' ', '_').replace('.', '')
	outfile = "Resume_{}.tex".format(clean_name)
	modify_resume(path, resume_infile, rp, name)

	#compile new resume
	compile_xelatex(path, outfile)




