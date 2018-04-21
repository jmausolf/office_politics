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
	os.chdir(path)
	subprocess.call("xelatex {}".format(tex_file), shell=True)



def remove_non_ascii_2(text):
	import re
	return re.sub(r'[^\x00-\x7F]+', "", text)

def read_tex(tex_file):
	text = str(tex_file)
	f = open(text, 'rU').read()
	return remove_non_ascii_2(f)


def rep_pair(r, list_pair):
	return r.replace(list_pair[0], list_pair[1])


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


"""
resume_pairs = [
	["GRADSCHOOL", "Massachusetts Institute of Technology"],
	["GS_CITYSTATE", "Cambridge, MA"],
	["GS_CSZIP", "Cambridge, MA 02139"],
	["GS_ADDRESS", "77 Massachusetts Ave, Sera 204"],
	["UGSCHOOL", "University of Michigan"],
	["UG_CITYSTATE", "Ann Arbor, MI"],
	["INTERNSHIP1", "Google"],
	["IC1_CITYSTATE", "Mountain View, CA"],
	["INTERNSHIP2", "Twitter"],
	["IC2_CITYSTATE", "San Francisco, CA"],
	["TREATMENT", "Michigan College Republicans"],
	["ID_NAME", "Matthew Zachary Hartman"],
	["ID_PHONE", "336-948-0756"],
	["ID_EMAIL", "matthewzhartman@gmail.com"]
]
"""



def make_resume_pairs(school, school_ctyst, school_cszip, school_address, ba_school, ba_ctyst, internships, profile, job_type, name, phone, gmail_user):

	#todo
	#get internvars from internphrase
	ik = "{}_{}".format(job_type, profile[-1])
	intern_key = internship_keys[ik]
	ints = internships.replace(' and ', ',').strip().split(',')

	int1=ints[0]
	int2=ints[1]
	int1_ctyst=intern_key[int1][1]
	int2_ctyst=intern_key[int2][1]

	#todo
	#get treatment from profile+jobregion+dictlookup
	experiment = "the Harvard Republican Club"

	keys = ["GRADSCHOOL", "GS_CITYSTATE", "GS_CSZIP", "GS_ADDRESS",
			"UGSCHOOL", "UG_CITYSTATE",
			"INTERNSHIP1", "IC1_CITYSTATE", "INTERNSHIP2", "IC2_CITYSTATE",
			"TREATMENT", "ID_NAME", "ID_PHONE", "ID_EMAIL"]

	vals = [school, school_ctyst, school_cszip, school_address,
			ba_school, ba_ctyst,
			int1, int1_ctyst, int2, int2_ctyst,
			experiment,
			name, phone, gmail_user]


	resume_pairs = list(map(list, zip(keys, vals)))
	print(resume_pairs)
	return resume_pairs


rp = make_resume_pairs("Massachusetts Institute of Technology", "New York, NY", "New York, NY 10013", 
	"4700 S Woodlawn, 402", "Harvard", "Cambridge, MA", 
	"Google and LinkedIn", "P05RH", "data_science", 
	"Matthew Zachary Hartman", "336-948-0756", "matthewzhartman@gmail.com")

#TODO
#Next task to write code to gen the resume pairs

name = "Matthew Zachary Hartman"
outfile = "Resume_{}.tex".format(name.replace(' ', '_'))


modify_resume("P04NL/quant/tex/", "resume_template.tex", rp, name)

#compile new resume
compile_xelatex("P04NL/quant/tex/", outfile)


def make_resume(profile, 
				job_type,
				#TODO VARS
				name, 
				title, 
				school, 
				phone, 
				gmail_user):

	rp = make_resume_pairs("Massachusetts Institute of Technology", "New York, NY", "New York, NY 10013", 
	"4700 S Woodlawn, 402", "Harvard", "Cambridge, MA", 
	"Google and LinkedIn", "P05RH", "data_science", 
	"Matthew Zachary Hartman", "336-948-0756", "matthewzhartman@gmail.com")


	outfile = "Resume_{}.tex".format(name.replace(' ', '_'))

	modify_resume("P04NL/quant/tex/", "resume_template.tex", rp, name)

	#compile new resume
	compile_xelatex("P04NL/quant/tex/", outfile)


