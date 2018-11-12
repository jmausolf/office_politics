import subprocess
import pandas as pd
from glob import glob
import re, os, sys
import zipfile
from fuzzywuzzy import process
import warnings

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

	#Save
	df.to_csv(outfile, index=False)
	print(df)


def clean_leadiro(infile, outfile='leadiro_mathed_key.csv'):

	df = pd.read_csv(infile)

	#Drop Tech Install and Revenue
	df.drop(['tech_install_intent', 'revenue'], axis=1, inplace=True)

	#Keep Cols
	keep_cols = ['first_name', 'email', 'out_company']
	df = df[keep_cols].copy().reset_index(drop=True)

	#Renamed Cols
	cols = ['contact_name', 'email', 'company']
	df.columns = cols

	#Keep Only One Contact Per Company
	gb = ['company']
	df = df.groupby(gb).apply(lambda x: x.sample(1)).reset_index(drop=True)
	df.to_csv(outfile, index=False)
	print(df)
	return df


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

	#df[rc] = df[rc, 'match_score'].apply(lambda x: x[0] if x[1] > 50 else 'none' )
	df[rc] = df.apply(score_filter, axis=1, col=rc)

	#Write Result
	df.to_csv(outfile, index=False)
	print(df[[lc, rc, 'match_score']].head(10))



def main():

	#Clean File Names
	rename_file_spaces()

	#Convert Leadiro XLSX to CSV
	convert_files_xlsx_csv()

	#Combine Files and Drop Duplicates
	combine_leadiro('leadiro_combined.csv')

	#Fuzzy Match Leadiro Company Names and Employer Key Company Names
	fuzzy_match_df_cols('leadiro_combined.csv', '../keys/employers_key.csv',
						'company', 'company',
						outfile='leadiro_matched.csv')

	#Clean Output and Select One Lead Per Company
	clean_leadiro('leadiro_matched.csv', '../keys/leadiro_matched_key.csv')


main()
