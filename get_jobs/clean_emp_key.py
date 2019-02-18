import pandas as pd
import re
from nltk.corpus import stopwords
import ast


#######################################
## Cleaning Code
#######################################

def ret_position_stop_words():

    ## Position Specific Stop Words
    position_stop_words = ['I', 'II', 'III', 'IV', 'V', 'VI',
                           'R&D', 'FP&A', 'IT', 'UX', 'SQL', 'SQA',
                           'M&A', 'M&E', 'TCL', 'VP', 'QA', 'EHS', 'IP',
                           'HR', 'IPM', 'NERA', 'HRIS',
                           'OMS/ESB', 'OMS', 'ESB', 'CPQ', 'WFO',
                           'MBA', 'PHD',
                           'TMT', 'SOX', 'ERP', 'DAS', 'HW', 'CLS',
                           'HRIS', 'SAP', 'NLP', 'ML', 'AI', 'ML/AI', 'GIS', 'BI',
                           'FT', 'NSW', 'NLU', 'NAV', 'BMW', 'MEP', 'BIM',
                           'ABA', 'PMO' ]


    ## Add State Abbreviations
    state_abb = pd.read_csv('../keys/region_key.csv')['state'].tolist()
    stop_words = position_stop_words
    stop_words.extend(state_abb)


    ## Add Uppercase Words from Included Companies
    company_words = []
    companies = df = pd.read_csv('../keys/employers_key.csv')['company'].tolist()
    [company_words.extend(c.split(' ')) for c in companies]
    company_uppers = [c for c in company_words if c.isupper()]
    stop_words.extend(company_uppers)
    return stop_words


def rm_state_abb_pat(text, state_abb):

    state_abb_pat = [' - - {}'.format(s) for s in state_abb]

    for s in state_abb_pat:
        text = text.replace(s, '')
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text


def upper_post_crit(word, stop_words):
    w = word

    crit =  (
                (w.isupper()) & 
                (len(w) > 4) &
                (w not in stop_words)
            )

    if crit:
        return w.title()
    else:
        return w


def lower_post_crit(word, stop_words):
    w = word

    crit =  (
                (w.islower()) & 
                (w not in stop_words)
            )

    if crit:
        return w.title()
    else:
        return w


def clean_position(text, upper_sw, lower_sw):

    #Starting Position
    p = text

    ##Fix Upper Case Words
    p = ' '.join([upper_post_crit(w, upper_sw) for w in p.split(' ')])

    ##Fix Lowercase Words
    p = ' '.join([lower_post_crit(w, lower_sw) for w in p.split(' ')])

    return p


def article_strip(school):
    s = school.lower().replace('the ', '').title()
    s = ' '.join([w.lower() if len(w) <=2 else w for w in s.split(' ')])
    clean_school = re.sub(r"\s{2,}", ' ', s).lstrip(' ')
    return clean_school



def cleaned_emp_key(emp_key='../keys/employers_key.csv',
                    outfile='../keys/cleaned_employers_key.csv'):

    print("[*] cleaning {}, outfile = {}".format(emp_key, outfile))
    df = pd.read_csv(emp_key)

    #State Abbreviations
    sb = pd.read_csv('../keys/region_key.csv')['state'].tolist()

    #Uppercase Stop Words
    up_sw = ret_position_stop_words()

    #Lowercase Stop Words
    lw_sw = set(stopwords.words('english'))


    #Correct State Abbreviations
    df['position'] = df['position'].apply(rm_state_abb_pat, state_abb=sb)

    #Correct Upper and Lower Words
    df['position'] = df['position'].apply(clean_position,
                                          upper_sw=up_sw,
                                          lower_sw=lw_sw)
    print(df['position'])
    df.to_csv(outfile, index=False)
    return df




#######################################
## Reclassify Code
#######################################


def join_emp_key_master_companies(emp_key, master_key):
    df_employ = pd.read_csv(emp_key)
    df_master = pd.read_csv(master_key)

    #Fill NA Values in Last Column
    df_master = df_master.fillna(axis=0, method='bfill')
    df_master = df_master.fillna(axis=0, method='ffill')

    df = pd.merge(df_employ, df_master, on=['list_id', 'company'], how='left')
    return df

def make_ranking_col(emp_key, master_key, rank_cols):
    df = join_emp_key_master_companies(emp_key, master_key)
    df['job_ranks'] = df[rank_cols].values.tolist()
    df['ranks_len'] = df['job_ranks'].apply(lambda x: len(x))
    return df


def compare_ranks(row):
    job_type = row[0]
    rank_cols = row[1]
  
    c = 0
    for r in rank_cols:
        if r == job_type:
            return c
        else:
            c+=1
            pass


def extract_job_param_key(job_type):
    keys = pd.read_csv('job_params.csv')
    result = keys.loc[(keys['job_type'] == job_type)]
    result = result['keywords'].values.tolist()[0]
    result = ast.literal_eval(result)
    return result


def get_keys(row):
    keys = []
    for r in row['job_ranks']:
        k = extract_job_param_key(r)
        keys.append(k)

    return keys


def reclass(row):

    if row['job_rank'] > 0:
        position = row['position'].lower()
        job_keys = row['keys']
        job_ranks = row['job_ranks']


        key_index = 0
        for key_set in job_keys:
            for k in key_set:
                if k in position:
                    return job_ranks[key_index]
                #TODO Stems
                else:
                    pass
            key_index+=1
            
    else:
        pass


def reclass_arbitrate(row):

    original = row['job_type']
    reclass = row['reclass']

    if reclass is None:
        return original
    else:
        return reclass


def reclassify_jobs(emp_key,
                    master_key,
                    rank_cols,
                    outfile='../keys/cleaned_employers_key.csv',
                    clean=True):

    #Prep
    df = make_ranking_col(emp_key, master_key, rank_cols)
    df['job_rank'] = df[['job_type', 'job_ranks']].apply(compare_ranks, axis=1)
    print('[*] extracting job keys, order for all job ranks and types....')
    df['keys'] = df.apply(get_keys, axis=1)

    print(df)
    
    #Main Reclassification and Arbitration
    df['reclass'] = df.apply(reclass, axis=1)
    df['job_type_reclass'] = df.apply(reclass_arbitrate, axis=1)


    if clean is True:
        keep_cols = ['cid', 'list_id', 'company', 'position', 'office', 'office_state', 'job_type_reclass', 'rank', 'source']
        org_cols = ['cid', 'list_id', 'company', 'position', 'office', 'office_state', 'job_type', 'rank', 'source']
        df = df[keep_cols]
        df.columns = org_cols

    print(df)
    df.to_csv(outfile, index=False)
    


#######################################
## Clean Raw Employers Key
#######################################

cleaned_emp_key('../keys/employers_key.csv',
                '../keys/cleaned_employers_key.csv')


#######################################
## Reclassify Job Types
#######################################

ranks = ['job_type_1', 'job_type_2', 'job_type_3',
         'job_type_4', 'job_type_5', 'job_type_6']
reclassify_jobs('../keys/cleaned_employers_key.csv',
                'master_companies.csv', ranks)
