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
from replace_dict import *




#############################################
## Duplicate Scrap
#############################################


'''
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
            an indiv
            ual processed choice. This should be a function
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
'''