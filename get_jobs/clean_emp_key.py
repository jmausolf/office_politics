import pandas as pd
import re
from nltk.corpus import stopwords



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



##TODO
## Manual Subs
## Part Time Positions
## Poor Fits (Retail Associate, etc)
## Check / Add Missing Companies (LinkedIn, etc)


def cleaned_emp_key():

	df = pd.read_csv('../keys/employers_key.csv')
	sb = pd.read_csv('../keys/region_key.csv')['state'].tolist()
	up_sw = ret_position_stop_words()
	lw_sw = set(stopwords.words('english'))
	df['position'] = df['position'].apply(rm_state_abb_pat, state_abb=sb)
	df['position'] = df['position'].apply(clean_position, 
										  upper_sw=up_sw,
										  lower_sw=lw_sw)
	print(df['position'])
	df.to_csv('../keys/cleaned_employers_key.csv', index=False)
	return df


cleaned_emp_key()
