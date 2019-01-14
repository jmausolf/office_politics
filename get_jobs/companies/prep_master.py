import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re
from string import punctuation
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings
import itertools
import glob

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
    #exceptions:: / \ - &
    tmp = re.sub(r'[]\\?!#$%(){}+*:;,._`\\|~\\[<=>@\\^]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp).strip()

def parens_content_replace(text):
    return re.sub(r'\(.*?\)', '', text).strip()


def read_csv(csv_file):
    text = str(csv_file)
    print(text)
    f = open(text, 'rU').read()
    #return remove_non_ascii_2(f)
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


def rm_company_stop_words(text, sw=None):

    if sw is None:
        sw = ['LLC', 'LLP', 'Llp', 'LP', 'P.C.', 'Inc', 'International', ' Cos', 'Cos ', 'Group',
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
    c = rm_company_stop_words(c, sw=sw)    
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
    #print(r)
        
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
    df['source'] = 'fortune1000'
    df['job_type'] = 'data_science'

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['id'] = 'f1000_'+df['index']
    df = df[['id', 'company', 'rank', 'source', 'job_type']]
    print(df)
    df.to_csv(clean_csv, index=False)
    return df

#clean_fortune_1000('fortune1000.csv')

## Clean Hedge Fund List
def clean_hedge(source_file):
    clean_csv = modify_csv(source_file)

    df = pd.read_csv(clean_csv)
    df['source'] = 'hedge_fund_100'
    df['job_type'] = 'quant'

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['id'] = 'hedge_'+df['index']
    df = df[['id', 'company', 'rank', 'source', 'job_type']]
    print(df)
    df.to_csv(clean_csv, index=False)
    return df

#clean_hedge('hedge_fund_100_institutional_investors_alpha.csv')

## Clean Vault List
def clean_vault(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)

    #Make Id
    df['index'] = df.index
    df['index'] = df['index'].apply(lambda x: str(x))
    df['id'] = 'vault_'+df['index']
    df = df[['id', 'company', 'rank', 'source', 'job_type']]
    print(df)
    return df

#clean_vault('vault_jobs_2019-01-14.csv')


## Clean Nasdaq List
def clean_nasdaq(source_file):
    clean_csv = modify_csv(source_file)
    df = pd.read_csv(clean_csv)
    df = clean_col_names(df)

    #Remove Duplicate Companies (Some Have Multiple Symbols)
    df = df.drop_duplicates('name')

    #Remove If MarketCap is Zero, Then Rank by Marketcap
    df = df.loc[(df['marketcap'] > 0)]
    df['rank'] = df['marketcap'].rank(method='average', ascending=False)
    df.sort_values(['rank'], ascending=True, inplace=True)

    #Clean Names
    sw = [', Inc.', ', Inc', ' Inc.', ' Inc',
          ', Ltd.', ', Ltd', ' Ltd.', ' Ltd',
          ',  Corp.', ' Corp.',
          ', Co.', ' Co.']
    df['company'] = df['name'].apply(clean_stop_words, sw=sw)

    #Assign ID
    df['id'] = 'nasdaq_'+df['symbol']
    keep_cols = ['id', 'company', 'rank']
    df = df[keep_cols]
    df['source'] = 'nasdaq_tech'
    df['job_type'] = 'data_science'

    #Save
    print(df)
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

prep_df = pd.concat([df1, df2, df3, df4], axis=0)
prep_df.to_csv("clean/master_companies_prep.csv", index=False)
print(prep_df)

#Append Files


#############################################
## Clean and Dedupe Preparation File
#############################################



def rm_company_stop_words(text):

    sw = ['LLC', 'LLP', 'Llp', 'LP', 'P.C.', 'Inc', 'International', ' Cos', 'Cos ', 'Group',
            'Management Co', 'Capital Management', 'Asset Management', 'Management', '& Co']

    for s in sw:
        #print(text)
        #print(s)
        text = text.replace(s, '')
        #print(text)

    text = re.sub(r'\s{2,}', " ", text).strip()
    return text


def clean_hedge(row, col='company'):
    c = row[col]
    return c

def clean_company(row, col='company'):
    c = row[col]
    c = remove_non_ascii_2(c)    
    #c = remove_punct(c)
    c = parens_content_replace(c)
    c = rm_company_stop_words(c)    
    c = select_punct_strip(c)

    if c.isupper() and len(c) > 4:
        c = c.title()

    c = c.strip()
    return c


#df = pd.read_csv('hedge_fund_100_institutional_investors_alpha.csv')
#print(df.shape)
#print(df)
#df['company'] = df.apply(clean_hedge, axis=1)
#print(df)
#dedupe_fuzzy(df, 'company')

#df.drop_duplicates('company', inplace=True)
#df = df.reset_index(drop=True)
#print(df.shape)
#df.to_csv("hedge_test2.csv", index=False)


def show_possible_duplicates(contains_dupes, threshold=70, scorer=fuzz.token_set_ratio):
    """
    A Modified Version of fuzzywuzzy process.dedupe:
    https://github.com/seatgeek/fuzzywuzzy/blob/master/fuzzywuzzy/process.py

    Code is Modified to Return Possible Duplicates to Review and Investigate
    (Original code dropped too many valid non-duplicates even with a high threshold
    and various scorers or conversely missed true duplicates).

    Rather than take the "first item as our 'canonical example'", 
        possible duplicate pairs are sorted and aggregated, then displayed.

    Args:
        contains_dupes: A list of strings that we would like to dedupe.
        threshold: the numerical value (0,100) point at which we expect to find duplicates.
            Defaults to 70 out of 100
        scorer: Optional function for scoring matches between the query and
            an individual processed choice. This should be a function
            of the form f(query, choice) -> int.
            By default, fuzz.token_set_ratio() is used and expects both query and
            choice to be strings.
    
        
        """

    extractor = []
    possibles = []

    # iterate over items in *contains_dupes*
    for item in contains_dupes:
        # return all duplicate matches found
        matches = process.extract(item, contains_dupes, limit=None, scorer=scorer)
        #print(matches)
        # filter matches based on the threshold
        filtered = [x for x in matches if x[1] > threshold]
        #print(filtered)
        # if there is only 1 item in *filtered*, no duplicates were found so append to *extracted*
        if len(filtered) == 1:
            extractor.append(filtered[0][0])

        else:
            # alpha sort
            filtered = sorted(filtered, key=lambda x: x[0])
            #print(filtered)
            # length sort
            filter_sort = sorted(filtered, key=lambda x: len(x[0]), reverse=True)
            #print(filter_sort)
            # take first item as our 'canonical example'
            extractor.append(filter_sort[0][0])
            possibles_no_score = [x[0] for x in filter_sort]
            possibles.append(possibles_no_score)

    # uniquify *extractor* list
    keys = {}


    def sort_lists_by_length(llists):
        l_lengths = [(l, len(l)) for l in llists]
        sorted_ll = sorted(l_lengths, key=lambda x: x[1], reverse=True)
        return [l[0] for l in sorted_ll]

    #Start with a set sorted by length
    possibles = sort_lists_by_length(possibles)
    print(possibles)
    print(len(possibles))

    check_dupes = set()
    possible_dupes = []

    for sl in possibles:
        first_item = sl[0]
        i = 0
        for item in sl:
            i+=1
            if item not in check_dupes and i == 1:    
                possible_dupes.append(sl)
                check_dupes.add(item)
            elif item not in check_dupes and i > 1:
                check_dupes.add(item)


    print(possible_dupes)
    print(len(possible_dupes))

    dupes = pd.Series(possible_dupes)
    dupes.name = 'possible_dupes'
    dupes = pd.DataFrame(dupes)
    print(dupes)


    for e in extractor:
        keys[e] = 1
    extractor = keys.keys()

    # check that extractor differs from contain_dupes (e.g. duplicates were found)
    # if not, then return the original list
    if len(extractor) == len(contains_dupes):
        return contains_dupes
    else:
        return extractor

def dedupe_fuzzy(df, col):

    #Data Column to Dedupe
    to_dedupe = df[col].tolist()[0:500]


    #result =  list(dedupe2(to_dedupe, threshold=82, scorer=fuzz.WRatio))
    #result =  list(dedupe2(to_dedupe, threshold=82, scorer=fuzz._token_set))
    result =  list(dedupe2(to_dedupe, threshold=80))
    #result2 =  list(dedupe2(to_dedupe, threshold=82, scorer=fuzz.WRatio))

    #result = process.default_scorer(s1, s2)
    dupes = list(set(to_dedupe).symmetric_difference(set(result)))
    print(dupes)
    print(len(dupes))

    #print(len(result))
    #print(type(result))
    #print(result)



#df = pd.read_csv('fortune1000-list.csv')
#df = pd.read_csv('master_companies_prep.csv')
#df = pd.read_csv('hedge_fund_100_institutional_investors_alpha.csv')
#print(df.shape)
#print(df)
#df['company'] = df.apply(clean_company, axis=1)
#dedupe_fuzzy(df, 'company')

#df.drop_duplicates('company', inplace=True)
#df = df.reset_index(drop=True)
#print(df.shape)
#df.to_csv("hedge_test2.csv", index=False)