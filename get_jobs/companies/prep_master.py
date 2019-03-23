import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re
from string import punctuation
import warnings
import itertools
import glob
from replace_dict import *


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)

def remove_non_ascii_space(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r"\s{2,}", ' ', text).strip(' ')
    return text


def remove_punct(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp).strip()


def select_punct_strip(text):
    #exceptions:: / \ - & .
    tmp = re.sub(r'[]\\?!#$%(){}+*:;,_`\\|~\\[<=>@\\^]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp).strip()

def parens_content_replace(text):
    return re.sub(r'\(.*?\)', '', text).strip()


def remove_trailing_periods(text):
    #Remove trailing periods
    #not following capital letters
    pat = r'([A-Z][.]$)|([.]$)'
    return re.sub(pat, r'\1', text)


def remove_trailing_corp(text):
    corp_exceptions = ['News Corp', 'Science Applications International Corporation']

    if text.title() in corp_exceptions:
        return text
    else:
        text = re.sub(r'\sCorporation$', '', text)
        text = re.sub(r' Corporation$', '', text)
        text = re.sub(r'\sCorp$', '', text)
        text = re.sub(r' Corp$', '', text)
        return text


def remove_upper_trailing(text):
    text = text.strip()
    exceptions = ['NEWS CORP', 'SCIENCE APPLICATIONS INTERNATIONAL CORPORATION']

    if text.upper() in exceptions:
        return text
    else:
        text = re.sub(r'\sINC$', '', text)

        text = re.sub(r'\sCORPORATION$', '', text)
        text = re.sub(r'\sCORP$', '', text)
        text = re.sub(r'\sCO$', '', text)


        text = re.sub(r'\sGROUP$', '', text)
        text = re.sub(r'\sGRP$', '', text)

        text = re.sub(r'\sTR$', '', text)

        text = re.sub(r'\sINTERNATIONAL$', '', text)
        text = re.sub(r'\sINTL$', '', text)

        return text


def repl_amer(text):
    text = re.sub(r'\sAMER$', ' AMERICA', text)
    text = re.sub(r'\sAMER\s', ' AMERICA ', text)
    text = re.sub(r'-AMER\s', '-AMERICA ', text)
    return text


def repl_grp_corp_of(text):
    text = re.sub(r'\sGRP OF\s', ' GROUP OF ', text)
    text = re.sub(r'\sCORP OF\s', ' CORPORATION OF ', text)
    return text


def lower_of_and(text):
    text = re.sub(r'\s[Oo][Ff]\s', ' of ', text)
    text = re.sub(r'\s[Aa][Nn][Dd]\s', ' and ', text)
    text = re.sub(r'\.[Cc][Oo][Mm]', '.com', text)
    return text


def remove_trailing_ABC(text):

        text = re.sub(r'\sA$', '', text)
        text = re.sub(r'\sB$', '', text)
        text = re.sub(r'\sC$', '', text)
        return text


def remove_trailing_inc(text):
    text = re.sub(r'\s[Ii][Nn][Cc]$', '', text)
    text = re.sub(r'\s[Ii][Nn][Cc][.]$', '', text)
    return text

def replace_bancorp(text):
    bancorp_exceptions = ['Zions Bancorp',
                          'Zions Bancorporation',
                          'New York Community Bancorp',
                          'West Bancorporation']
    if text.title() in bancorp_exceptions:
        return text
    else:
        return text.replace(' Bancorp', ' Bank')


def read_csv(csv_file):
    text = str(csv_file)
    print(text)
    f = open(text, 'rU').read()
    return f


def cleanup_cols(df, rm_col_list):
    cols = df.columns.tolist()
    keep_cols = [c for c in cols if c not in rm_col_list]
    return df[keep_cols].copy().reset_index(drop=True)

def clean_col_text(text):
    text = remove_non_ascii_2(text)
    text = remove_punct(text)
    text = text.replace(' ', '').strip().lower()
    return text

def clean_col_names(df):
    cols = df.columns.tolist()
    clean_cols = [clean_col_text(c) for c in cols]
    df.columns = clean_cols
    return df

#For Nasdaq
def rm_stop_words(text, sw=None):

    if sw is None:
        sw = ['LLC', 'LLP', 'Llp', 'LP', 'P.C.', ' International', ' Cos', 'Cos ', 'Group',
              'Management Co', 'Capital Management', 'Asset Management', 'Management', '& Co']
    else:
        pass

    for s in sw:
        text = text.replace(s, '')

    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text

def clean_stop_words(company_name, sw=None):
    c = company_name
    c = remove_non_ascii_space(c)
    c = parens_content_replace(c)
    c = rm_stop_words(c, sw=sw)
    return c


def convert_xlsx_csv(file):
    print('[*] converting file: {} to .csv file...'.format(file))
    pd.read_excel(file).to_csv(str(file).replace("xlsx", "csv"), index=False)




def article_strip(school):
    s = school.lower().replace('the ', '').title()
    s = ' '.join([w.lower() if len(w) <=2 else w for w in s.split(' ')])
    clean_school = re.sub(r"\s{2,}", ' ', s).lstrip(' ')
    return clean_school


def modify_csv(csv_file, path='source/', dest='clean/', outfile=True, replace=False):

    #load file modify
    infile = '{}{}'.format(path, csv_file)
    r = read_csv(infile)


    r = remove_non_ascii_space(r)

    #write results
    if replace is True:
        output = open(infile, "w")
    else:
        file_stem = csv_file.split('.csv')[0]
        outfile = "{}{}_cleaned.csv".format(dest, file_stem)
        output = open(outfile, "w")

    output.write(r)
    output.close()

    return outfile



#############################################
## Clean Source Files
#############################################

## Clean Fortune 1000 List
def clean_fortune_1000(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']
    df['source'] = 'fortune1000'
    df['job_type'] = 'data_science' 

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'f1000_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df

## Clean Hedge Fund List
def clean_hedge(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']
    df['source'] = 'hedge_fund_100'
    df['job_type'] = 'quant'

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'hedge_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean Vault List
def clean_vault(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'vault_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean Nasdaq List
def clean_nasdaq(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df = clean_col_names(df)

    #Remove Duplicate Companies (Some Have Multiple Symbols)
    df['raw_company'] = df['name']
    df = df.drop_duplicates('name')

    #Remove If MarketCap is Zero, Then Rank by Marketcap
    df = df.loc[(df['marketcap'] > 0)]
    df['rank'] = df['marketcap'].rank(method='average', ascending=False)
    df.sort_values(['rank'], ascending=True, inplace=True)

    #Clean Names
    sw = [', Inc.', ' Inc.',
          ', Ltd.', ', Ltd', ' Ltd.', ' Ltd',
          ',  Corp.', ' Corp.',
          ', Co.', ' Co.']
    df['company'] = df['name'].apply(clean_stop_words, sw=sw)

    #Assign ID
    df['list_id'] = 'nasdaq_'+df['symbol']
    keep_cols = ['list_id', 'company', 'raw_company', 'rank']
    df = df[keep_cols]
    df['source'] = 'nasdaq_tech'
    df['job_type'] = 'data_science_b'

    #Save
    df.to_csv(clean_csv, index=False)
    return df


## Clean Glassdoor List
def clean_glassdoor(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'glassdoor_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean Forbes List
def clean_forbes(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'forbes_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean CNBC List
def clean_cnbc(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']

    #Add Columns
    df['source'] = 'cnbc_disruptor50'
    df['job_type'] = 'data_science'

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'cnbc_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean BI List
def clean_bi(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df['raw_company'] = df['company']

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['list_id'] = 'bi_'+df['index']
    df = df[['list_id', 'company', 'raw_company', 'rank', 'source', 'job_type']]
    df.to_csv(clean_csv, index=False)
    return df


## Clean RU3000 Index
def clean_ru3000(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df = clean_col_names(df)

    #Remove Duplicate Companies (Some Have Multiple Symbols)
    df = df.drop_duplicates('company')
    df['raw_company'] = df['company']

    #Replace & Co
    rep_and_co1 = lambda x: re.sub(r'\&\sCO\s', ' & COMPANY ', x)
    rep_and_co2 = lambda x: re.sub(r'\&\sCO$', ' & COMPANY', x)
    df['company'] = df['company'].apply(rep_and_co1)
    df['company'] = df['company'].apply(rep_and_co2)

    #Replace Financial Services
    rep_fs1 = lambda x: x.replace(' FINL SVCS ', ' FINANCIAL ')
    rep_fs2 = lambda x: x.replace(' FINL', ' FINANCIAL')
    df['company'] = df['company'].apply(rep_fs1)
    df['company'] = df['company'].apply(rep_fs2)

    #Replace Properties
    rep_ps1 = lambda x: x.replace(' PPTYS', ' PROPERTIES')
    rep_ps2 = lambda x: x.replace(' PPTY', ' PROPERTY')
    df['company'] = df['company'].apply(rep_ps1)
    df['company'] = df['company'].apply(rep_ps2)


    #Replace Communications
    rep_comm = lambda x: re.sub(r'\sCOMM$', ' COMMUNICATIONS', x)
    df['company'] = df['company'].apply(rep_comm)

    #Replace Communities / Community
    rep_cmntys = lambda x: re.sub(r'\sCMNTYS', ' COMMUNITIES', x)
    rep_cmnty = lambda x: re.sub(r'\sCMNTY', ' COMMUNITY', x)
    df['company'] = df['company'].apply(rep_cmntys)
    df['company'] = df['company'].apply(rep_cmnty)

    #Replace Systems
    rep_sys1 = lambda x: re.sub(r'\sSYS\s', ' SYSTEMS ', x)
    rep_sys2 = lambda x: re.sub(r'\sSYS$', ' SYSTEMS', x)
    df['company'] = df['company'].apply(rep_sys1)
    df['company'] = df['company'].apply(rep_sys2)

    #Replace International
    rep_intl = lambda x: x.replace('INTL ', 'INTERNATIONAL ')
    df['company'] = df['company'].apply(rep_intl)

    #Replace Mortgage
    rep_mtg = lambda x: x.replace(' MTG', ' MORTGAGE')
    df['company'] = df['company'].apply(rep_mtg)

    #Replace Trust
    rep_mtg = lambda x: x.replace(' TR ', ' TRUST ')
    df['company'] = df['company'].apply(rep_mtg)

    #Replace AMER
    df['company'] = df['company'].apply(repl_amer)

    #Replace GRP OF / CORP OF
    df['company'] = df['company'].apply(repl_grp_corp_of)

    #Clean Names Before Adjusting Case
    sw = [' PLC',
          ' LTD',
          ' SERIES A', ' SERIES B', ' SERIES C',
          ' SER A', 'SER B', 'SER C',
          ' CLASS A', ' CLASS B', ' CLASS C',
          ' CL A', ' CL B', ' CL C',
          ' NV', ' N V',
          ' SVCS',
          ' HLDGS', ' HOLDINGS']

    df['company'] = df['company'].apply(clean_stop_words, sw=sw)

    #Remove Lingering ABC
    df['company'] = df['company'].apply(remove_trailing_ABC)

    #Remove Upper Trailing SW
    df['company'] = df['company'].apply(remove_upper_trailing)


    #Title Case
    df['company'] = df['company'].apply(lambda x: x.title())

    #Lower Of / And
    df['company'] = df['company'].apply(lower_of_and)

    #Drop Duplicates by Cleaned Names
    df = df.drop_duplicates(['company'])
    df = df.sort_values(['company'])

    #No Rank, Just Use Index
    df['rank'] = df.index
    df['rank'] = df['rank'].apply(lambda x: str(x))

    #Assign ID
    df['list_id'] = 'ru_'+df['ticker']
    keep_cols = ['list_id', 'company', 'raw_company', 'rank']
    df = df[keep_cols]
    df['source'] = 'ru3000'
    df['job_type'] = 'data_science_b'

    #Save
    df.to_csv(clean_csv, index=False)
    return df



#############################################
## Create Preparation File
#############################################

#Clean Multiple Source Files
df1 = clean_fortune_1000('fortune1000.csv')
df2 = clean_hedge('hedge_fund_100_institutional_investors_alpha.csv')
df3 = clean_vault('vault_jobs_2019-01-14.csv')
df4 = clean_nasdaq('nasdaq_tech.csv')
df5 = clean_glassdoor('glassdoor_jobs_2019-01-15.csv')
df6 = clean_forbes('forbes_jobs_2019-01-15.csv')
df7 = clean_cnbc('cnbc_disruptor50.csv')
df8 = clean_bi('business_insider_jobs_2019-01-16.csv')
df9 = clean_ru3000('ru3000.csv')

#TODO
#Make Multiple Job_Type Columns for Conditions

prep_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], axis=0)
prep_df.to_csv("clean/master_companies_prep.csv", index=False)
print(prep_df)

#Append Files


#############################################
## Clean and Dedupe Preparation File
#############################################



def rm_company_stop_words(text):

    sw = [' LLC', ' LLP', ' Llp', ' LP', ' P.C.', ' P.L.L.C.', ' PLC', ' Plc', ' plc',
          ' Inc.', ' Incorporated', ' International', ' Cos',
          '  N.V.', ' NV',
          ' Holdings', ' Holding']

    #' Group', ' Management Co.', ' Capital Management', ' Asset Management', ' Management', '& Co']

    for s in sw:
        text = text.replace(s, ' ')

        text = re.sub(r'\s{2,}', " ", text).strip()

    return text



def clean_company(row, col='company'):
    c = row[col]

    c = remove_non_ascii_2(c)
    c = parens_content_replace(c)
    c = rm_company_stop_words(c)
    c = select_punct_strip(c)
    c = remove_trailing_periods(c)
    c = remove_trailing_inc(c)
    c = remove_trailing_corp(c)
    c = replace_bancorp(c)

    #Make Long All Upper Case Companies Title Case
    if c.isupper() and len(c) > 4:
        c = c.title()

    #Make Short Companies UPPER CASE
    if len(c) <= 3:
        c = c.upper()

    c = c.strip()

    return c

## Clean Company
prep_df['company'] = prep_df.apply(clean_company, axis=1)

## Adhoc Value Replacements
prep_df['company'] = prep_df['company'].replace(company_replacements)

##Drop Based on Lowercase Company Name
prep_df['company_lower'] = prep_df['company'].apply(lambda x: x.lower())
prep_df.drop_duplicates('company_lower', inplace=True)
prep_df = prep_df.drop(['company_lower'], axis=1)


#Make Leadiro Specific File and Drop Raw Company
leadiro_abm = prep_df[['list_id', 'company', 'raw_company']]
leadiro_abm.to_csv('../../leadiro/leadiro_master_abm.csv', index=False)
prep_df = prep_df.drop(['raw_company'], axis=1)
print(prep_df)



#############################################
## Make Multiple Job Types
#############################################

#Full Job Types
job_types_dict = {'data_science':['data_science', 'computer_science', 'mba', 'mba_finance', 'stats', 'quant', 'mba_analyst'],
                  'quant':['quant', 'data_science', 'mba_finance', 'computer_science', 'stats', 'mba', 'mba_analyst'],
                  'banking':['quant', 'data_science', 'mba_finance', 'mba', 'stats', 'computer_science', 'mba_analyst'],
                  'accounting':['mba_finance', 'mba', 'stats', 'data_science', 'computer_science', 'quant', 'mba_analyst'],
                  'consulting':['data_science', 'mba_finance', 'mba', 'computer_science', 'stats', 'quant', 'mba_analyst'],
                  'law':['mba', 'mba_finance', 'data_science', 'computer_science', 'stats', 'quant', 'mba_analyst'],
                  'data_science_b':['data_science', 'computer_science', 'mba', 'mba_finance', 'stats', 'quant', 'mba_analyst']
}


#MBA Test
'''
job_types_dict = {'data_science':['mba', 'mba_finance', 'mba_analyst'],
                  'quant':['mba', 'mba_finance', 'mba_analyst'],
                  'banking':['mba', 'mba_finance', 'mba_analyst'],
                  'accounting':['mba', 'mba_finance', 'mba_analyst'],
                  'consulting':['mba', 'mba_finance', 'mba_analyst'],
                  'law':['mba', 'mba_finance', 'mba_analyst'],
                  'data_science_b':['mba', 'mba_finance', 'mba_analyst']
}
'''


def job_col_names(job_types_dict, first_key):
    vals = job_types_dict[first_key]
    n = 1
    job_cols = []
    for v in vals:
        jc = 'job_type_{}'.format(str(n))
        job_cols.append(jc)
        n+=1

    return job_cols


def make_job_search_cols(prep_df, job_types_dict):

    job_cols = job_col_names(job_types_dict, 'data_science')
    jobs_df = pd.DataFrame.from_dict(job_types_dict, orient='index')
    jobs_df.columns = job_cols
    jobs_df['job_type'] = jobs_df.index

    ##Merge
    df = prep_df.merge(jobs_df, how='left', on='job_type')

    #Drop Base Job_Type Key
    df = df.drop(['job_type'], axis=1)
    print(df)
    df.to_csv("clean/master_companies_prep.csv", index=False)
    return df


make_job_search_cols(prep_df, job_types_dict)



