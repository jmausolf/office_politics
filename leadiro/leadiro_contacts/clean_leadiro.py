import subprocess
import pandas as pd
from glob import glob
import re, os, sys
import zipfile
from fuzzywuzzy import process
import warnings
import argparse, textwrap
sys.path.append("..")
#sys.path.append(".")

from replace_dict import *


def remove_punct(text):
	tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', " ", text)
	return re.sub(r'\s{2,}', " ", tmp)


def cleanup_cols(df, rm_col_list):

	cols = df.columns.tolist()
	keep_cols = [c for c in cols if c not in rm_col_list]
	return df[keep_cols].copy().reset_index(drop=True)


def convert_xlsx_csv(file):
	print('[*] converting file: {} to .csv file...'.format(file))
	pd.read_excel(file).to_csv(str(file).replace("xlsx", "csv"), index=False)


def convert_files_xlsx_csv(stem=None):
	if stem is None:
		g = glob('*.xlsx')
	else:
		g = glob('*{}*.xlsx'.format(stem))

	for file in g:
		convert_xlsx_csv(file)


def rename_file_spaces(ext=None, exclude='*.py*'):
	if ext is None:
		g = glob('*')
	else:
		g = glob('*.{}'.format(ext))
	
	raw_fnames = [f for f in g if f not in glob(exclude)]
	clean_fnames = [re.sub(r'\s', '_', f).lower() for f in raw_fnames]

	for r, c in zip(raw_fnames, clean_fnames):
		print('[*] cleaning filename: {}'.format(r))
		os.rename(r, c)

	
def combine_leadiro(outfile, stem='leadiro', clean=True):

	if clean is True:
		rename_file_spaces()
		convert_files_xlsx_csv()

	g = glob('*leadiro*.csv')
	ex1 = glob('*matched*')
	ex2 = glob('*combined*')
	ex3 = glob('*key*')

	ex = [ex1, ex2, ex3]
	exclude = []

	for glob_set in ex:
		if len(glob_set) > 0:
			exclude.extend(glob_set)
		else:
			pass

	glob_clean = [f for f in g if f not in exclude]

	qc = (
			( isinstance(g, list) is True ) &
			( len(g) >= 1)
		 )
	assert qc, "no leadiro csv files found, please add csvs to combine"

	print('[*] combining the following leadiro files: {}'.format(g))

	#Combine CSVs
	count = 0
	for f in glob_clean:
		df = pd.read_csv(f)

		if count == 0:
			#write to csv full
			df.to_csv(outfile, index=False, header=True)
		else:
			#write append
			df.to_csv(outfile, index=False, header=False, mode='a')

		count+=1

	#Dedeupe Combined Data
	df = pd.read_csv(outfile)
	df.drop_duplicates(inplace=True)

	#Rename Columns
	clean_cols = [remove_punct(c) for c in df.columns.tolist()]
	clean_cols = [re.sub(r'\s', '_', c).lower() for c in clean_cols]
	df.columns = clean_cols

	# Adhoc Value Replacements (To Correct Fuzzy Mismatch)
	df['company'] = df['company'].replace(leadiro_changes)

	# Blacklist (Remove Companies Mistakenly Downloaded)
	df['company'] = df['company'].replace(blacklist_companies)
	df = df.dropna(subset=['company'])

	#Save
	df.to_csv(outfile, index=False)
	print(df)


def clean_leadiro(infile, outfile='leadiro_mathed_key.csv'):

	df = pd.read_csv(infile)

	#Drop Tech Install and Revenue
	df.drop(['tech_install_intent', 'revenue'], axis=1, inplace=True)

	#Keep Cols
	keep_cols = ['first_name', 'last_name', 'email', 'out_company']
	df = df[keep_cols].copy().reset_index(drop=True)

	#Renamed Cols
	cols = ['contact_name', 'contact_last_name', 'contact_email', 'company']
	df.columns = cols

	#Keep Only One Contact Per Company
	gb = ['company']
	df = df.groupby(gb).apply(lambda x: x.sample(1)).reset_index(drop=True)
	df.to_csv(outfile, index=False)
	print(df)
	return df


def make_emp_key_replacements(emp_key):
	df = pd.read_csv(emp_key)

	# Adhoc Value Replacements (To Correct Fuzzy Mismatch)
	df['company'] = df['company'].replace(emp_key_adjustments)

	#Emp Key Blacklist
	df['company'] = df['company'].replace(emp_key_blacklist)
	df = df.dropna(subset=['company'])	

	print('[*] modifying {} and overwriting file...'.format(emp_key))
	df.to_csv(emp_key, index=False)
	return df


def company_match(row, 
				  leadiro_col='in_company', 
				  key_col='out_company',
				  exact=True,
				  ratio=False):

	leadiro_col = row[leadiro_col].lower()
	key_col = row[key_col].lower()

	parens_search = re.search(r'\(.*?\)', leadiro_col)
	if parens_search:
		leadiro_parens = parens_search.group(0)
		leadiro_parens = leadiro_parens.replace('(', '').replace(')', '')
	else:
		leadiro_parens = '()'

	if ratio is True:
		r = (len(leadiro_col) / len(key_col))
		return r
	else:

		if exact is True:
			if leadiro_col == key_col:
				return True
			elif leadiro_parens == key_col:
				return True
			else:
				return False
		else:
			if leadiro_col != key_col and key_col in leadiro_col:
				return True
			else:
				return False


def match_warning(row, 
				  match_col='match',
				  maybe_match_col='maybe_match',
				  ratio_match='ratio_match'
				  ):
	match_col = row[match_col]
	maybe_match_col = row[maybe_match_col]
	ratio_match = row[ratio_match]

	if match_col is False and maybe_match_col is False:
		return "WARNING"
	elif match_col is False and ratio_match > 4:
		return "WARNING"
	else:
		return "PASS"


def match_names(left_names, right_names):

	names_array=[]
	ratio_array=[]

	for row in left_names:
		x = process.extractOne(row, right_names)
		names_array.append(x[0])
		ratio_array.append(x[1])

	return names_array, ratio_array
 

def score_filter(row, col, min_score=50):
 	rc = row[col]
 	score = row['match_score']

 	if score > min_score:
 		return rc
 	else:
 		return 'unknown'


def fuzzy_match_df_cols(left_df, right_df, 
						left_col, right_col,
						outfile='matched_cid.csv',
						min_score=50,
						left_prefix='in_',
						right_prefix='out_'):

	ldf, lc, lp = left_df, left_col, left_prefix
	rdf, rc, rp = right_df, right_col, right_prefix

	#Left dataset
	left_names = pd.read_csv(ldf)[lc].dropna().values

	#Right dataset
	right_names = pd.read_csv(rdf)[rc].values
	name_match, ratio_match = match_names(left_names, right_names)


	#Make Key from Matches
	df = pd.read_csv(ldf)
	if lc == rc:
		df.rename(columns={lc:lp+lc}, inplace=True)
		lc = lp+lc
		rc = rp+rc
	else:
		pass

	df[rc]=pd.Series(name_match)
	df['match_score']=pd.Series(ratio_match)
	df[rc] = df.apply(score_filter, axis=1, col=rc)

	#Write Full Result
	df.to_csv(outfile, index=False)

	#Evaluate Matches / Warn for False Matches
	df['match'] = df.apply(company_match, axis=1, exact=True)
	df['maybe_match'] = df.apply(company_match, axis=1, exact=False)
	df['ratio_match'] = df.apply(company_match, axis=1, ratio=True)
	df['match_warning'] = df.apply(match_warning, axis=1)
	sort_cols = ['match_warning', 'ratio_match', 'match_score']
	df = df.sort_values(by=sort_cols, ascending=False)

	#Make Simple Result File
	outfile = outfile.split('.csv')[0]+'_simple.csv'
	df = df[[lc, rc, 'match_score', 'ratio_match', 'match_warning']]
	df.to_csv(outfile, index=False)
	print(df)





def clean_leadiro_main(
		combined_leadiro_file='leadiro_combined.csv',
		leadiro_col = 'company',
		emp_file = '../../keys/employers_key.csv',
		emp_col = 'company',
		local_out = '../leadiro_matched.csv',
		matched_leadiro_key = '../../keys/leadiro_matched_key.csv',
		match_only=False

	):

	if match_only is False:
	
		#Clean File Names
		rename_file_spaces()

		#Convert Leadiro XLSX to CSV
		convert_files_xlsx_csv()

		#Combine Files and Drop Duplicates
		combine_leadiro(combined_leadiro_file)

		#Adjust Emp Key
		make_emp_key_replacements(emp_file)

		#Fuzzy Match Leadiro Company Names and Employer Key Company Names
		fuzzy_match_df_cols(combined_leadiro_file, emp_file,
							leadiro_col, emp_col,
							outfile=local_out)

		#Clean Output and Select One Lead Per Company
		clean_leadiro(local_out, matched_leadiro_key)

	else:

		#Adjust Emp Key
		make_emp_key_replacements(emp_file)

		#Fuzzy Match Leadiro Company Names and Employer Key Company Names
		fuzzy_match_df_cols(combined_leadiro_file, emp_file,
							leadiro_col, emp_col,
							outfile=local_out)

		#Clean Output and Select One Lead Per Company
		clean_leadiro(local_out, matched_leadiro_key)



if __name__=="__main__":


    clean_leadiro_main(
		combined_leadiro_file='leadiro_combined.csv',
		leadiro_col = 'company',
		emp_file = '../../keys/cleaned_employers_key.csv',
		emp_col = 'company',
		local_out = 'leadiro_matched.csv',
		matched_leadiro_key = '../../keys/leadiro_matched_key.csv',
		match_only=False
	)
