import ast, csv, os, pdb
import numpy as np
import pandas as pd
import re
from string import punctuation
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings
import itertools


def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)


def remove_punct(text):
    tmp = re.sub(r'[]\\?!\"\'#$%&(){}+*/:;,._`|~\\[<=>@\\^-]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp).strip()


def select_punct_strip(text):
	#exceptions:: / \ - &
    tmp = re.sub(r'[]\\?!#$%(){}+*:;,._`\\|~\\[<=>@\\^]', " ", text)
    return re.sub(r'\s{2,}', " ", tmp).strip()

def parens_content_replace(text):
	return re.sub(r'\(.*?\)', '', text).strip()

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


def dedupe2(contains_dupes, threshold=70, scorer=fuzz.token_set_ratio):
    """This convenience function takes a list of strings containing duplicates and uses fuzzy matching to identify
    and remove duplicates. Specifically, it uses the process.extract to identify duplicates that
    score greater than a user defined threshold. Then, it looks for the longest item in the duplicate list
    since we assume this item contains the most entity information and returns that. It breaks string
    length ties on an alphabetical sort.
    Note: as the threshold DECREASES the number of duplicates that are found INCREASES. This means that the
        returned deduplicated list will likely be shorter. Raise the threshold for fuzzy_dedupe to be less
        sensitive.
    Args:
        contains_dupes: A list of strings that we would like to dedupe.
        threshold: the numerical value (0,100) point at which we expect to find duplicates.
            Defaults to 70 out of 100
        scorer: Optional function for scoring matches between the query and
            an individual processed choice. This should be a function
            of the form f(query, choice) -> int.
            By default, fuzz.token_set_ratio() is used and expects both query and
            choice to be strings.
    Returns:
        A deduplicated list. For example:
            In: contains_dupes = ['Frodo Baggin', 'Frodo Baggins', 'F. Baggins', 'Samwise G.', 'Gandalf', 'Bilbo Baggins']
            In: fuzzy_dedupe(contains_dupes)
            Out: ['Frodo Baggins', 'Samwise G.', 'Bilbo Baggins', 'Gandalf']
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
df = pd.read_csv('master_companies_prep.csv')
print(df.shape)

#df['company'] = df.apply(clean_company, axis=1)
dedupe_fuzzy(df, 'company')

#df.drop_duplicates('company', inplace=True)
#df = df.reset_index(drop=True)
#print(df.shape)
df.to_csv("master_companies_clean.csv", index=False)