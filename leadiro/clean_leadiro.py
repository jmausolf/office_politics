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
	qc = (
			( isinstance(g, list) is True ) &
			( len(g) >= 1)
		 )
	assert qc, "no leadiro csv files found, please add csvs to combine"

	print('[*] combining the following leadiro files: {}'.format(g))

	#Combine CSVs
	count = 0
	for f in g:
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

	#Drop Tech Install
	df.drop(['tech_install_intent'], axis=1, inplace=True)

	#Save
	df.to_csv(outfile, index=False)
	print(df)



#rename_file_spaces()
#convert_files_xlsx_csv()
#combine_leadiro('leadiro_key.csv')


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

	ldf, lc = left_df, left_col
	rdf, rc = right_df, right_col

	#Left dataset
	left_names = pd.read_csv(ldf)[lc].dropna().values

	#Right dataset
	right_names = pd.read_csv(rdf)[rc].values
	name_match, ratio_match = match_names(left_names, right_names)


	#Make Key from Matches
	df = pd.read_csv(ldf)
	if lc == rc:
		df.rename(columns={lc:'l_'+lc}, inplace=True)
		lc = 'l_'+lc
		rc = 'r_'+rc
	else:
		pass

	df[rc]=pd.Series(name_match)
	df['match_score']=pd.Series(ratio_match)

	#df[rc] = df[rc, 'match_score'].apply(lambda x: x[0] if x[1] > 50 else 'none' )
	df[rc] = df.apply(score_filter, axis=1, col=rc)

	#Write Result
	df.to_csv(outfile, index=False)
	print(df[[lc, rc, 'match_score']].head(10))


fuzzy_match_df_cols('leadiro_key.csv', 'employers_key.csv',
					'company', 'company')

#fuzzy_match_df_cols('employers_key.csv', 'leadiro_key.csv', 
#					'company', 'company')


