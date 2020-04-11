import pandas as pd

def recode_outcomes(df):

	#W1_N1305
	df.loc[(df['mb_id'] == 'MB_2152'), 'outcome'] = 'Autoreply'
	df.loc[(df['mb_id'] == 'MB_1514'), 'outcome'] = 'Reply'

	#P0725: W1_N1449, W1_N1450 
	#Said "undeliverable" but got actual replies from direct poc
	df.loc[(df['mb_id'] == 'MB_2039'), 'outcome'] = 'Autoreply'
	df.loc[(df['mb_id'] == 'MB_0798'), 'outcome'] = 'Autoreply'

	#P0967: W1_N1933, W1_N1934
	#Maternity leave, not bounce
	df.loc[(df['mb_id'] == 'MB_0308'), 'outcome'] = 'Autoreply'
	df.loc[(df['mb_id'] == 'MB_0830'), 'outcome'] = 'Autoreply'


	#P0123: W1_N0246 MB_0068
	df.loc[(df['mb_id'] == 'MB_0068'), 'outcome'] = 'Bounce'

	#W1_N0297	P0149
	df.loc[(df['mb_id'] == 'MB_0973'), 'outcome'] = 'Reply'


	#W1_N1461	P0731
	df.loc[(df['mb_id'] == 'MB_0339'), 'outcome'] = 'Bounce'

	#P0965 MB_2173 MB_0198: Leave as is

	#MB_1237			W1_N2408	P1204
	df.loc[(df['mb_id'] == 'MB_1237'), 'outcome'] = 'Bounce'

	#MB_0586	W2_N0697
	df.loc[(df['mb_id'] == 'MB_0586'), 'outcome'] = 'Reply'


	#MB_0974		W1_N0172	P0086
	df.loc[(df['mb_id'] == 'MB_0974'), 'outcome'] = 'Autoreply'

	#MB_2206			W1_N1064	P0532
	df.loc[(df['mb_id'] == 'MB_2206'), 'outcome'] = 'Bounce'

	#MB_2167 	W1_N1857
	df.loc[(df['mb_id'] == 'MB_2167'), 'outcome'] = 'Autoreply'

	#Leave As Is
	#MB_0837		W1_N2021	P1011
	#MB_1580		W1_N2022	P1011

	#Leave As Is
	#MB_0175		W2_N0799	P1806
	#MB_0548		W2_N0800	P1806

	return df

