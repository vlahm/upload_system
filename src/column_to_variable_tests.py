# script exploring search algorithms and language processing strategies to help
# auto-match user uploaded data variable names with macrosheds-canonical variable names
import pandas as pd
import sys
import json
from fuzzywuzzy import fuzz, process

# set fuzzy score cutoof
score_cutoff = 50

# MacroSheds variable sheet
# sheet_id = "1zc1RydnVyAQBdrp-6wBuZl8-gemgIro5893czoGM7mw"
# sheet_name = "variables"
# url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
# variables = pd.read_csv(url)
# variables_names = sorted(list(variables.variable_code))
# var_low = [var.lower() for var in variables_names]

# MacroSheds variable synonyms sheet
sheet_id = "1N3NuJL1tzJTVhcI9O8EPV9nEOd2LYlJ7zra_k3cV6fM"
sheet_name = "column_matching_synonyms"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
variables = pd.read_csv(url)
# names, and lower case names
variables_names = sorted(list(variables.value))
var_low = [var.lower() for var in variables_names]
# synonyms and lower case synonyms
variables_synonyms = sorted(variables.synonyms.values.tolist())
variables_synonyms_low = [var.lower() for var in variables_synonyms]

# list of vars and var synonyms for fuzzy matching,
# with all strings < 2 chars removed
var_low_fz = variables_synonyms_low + var_low
var_low_fz_clean = [var for var in var_low_fz if len(var) > 2]

# NLP helpers
def var_text_reduce_noise(item):
    """ removing common clutter text from strings"""
    item = item.replace('conc', '')
    item = item.replace('collect', '')
    item = item.replace('sample', '')
    item = item.replace('wt', '')
    item = item.replace('ml', '')
    item = item.replace('conc', '')
    item = item.replace('flux', '')
    item = item.replace('grab', '')
    item = item.replace('measure', '')
    return item

def var_text_remove_non_alphanum(item):
    """ removing common non-alphanumeric symbols from strings"""
    item = item.replace('-', '')
    item = item.replace('.', '')
    item = item.replace(' ', '')

    # or, full blown
    item = re.sub(r'\W+', '', item)

    return item

def var_text_all_cleaners(item):
    item = var_text_reduce_noise(item)
    item = var_text_remove_non_alphanum(item)
    return item

# search algorithms
def binary_search(item_list, item):
    """
    binary search algorithm, predicated on alphabetical order of input, searches exact matches
    source: https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-1.php
    """
    first = 0
    last = len(item_list)-1
    found = False
    result = False

    while( first<=last and not found):
        mid = (first + last)//2
        # exact match
        if item_list[mid].lower() == item.lower():
            found = True
            result = item_list[mid]
        # exact match with "noise" reduced and non-alphanumeric symbols removed
        elif var_text_all_cleaners(item_list[mid].lower()) == var_text_all_cleaners(item.lower()):
            found = True
            result = item_list[mid]
        else:
            if item < item_list[mid]:
                last = mid - 1
            else:
               first = mid + 1
    return found, result

## PRE: exploring algorithm applicatin
# bring in raw example stream data
# Baltimore Raw Stream Chem
bmore = pd.read_csv('../../../data/raw/lter_raw/baltimore/raw/stream_chemistry__700/sitename_NA/BES-stream-chemistry.csv')
bmore_cols = sorted(list(bmore.columns))

# dummy Raw 'Stereotypical' Hydrochem Data, contains:
    # common words which need watershed sci dict matching
    # variables with weird versions of name (too long, mispel, etc.)
    # NOTE: should we add a watershed-sci-dict workflow step where
    # NO3 is swapped w Nitrate and re-matched, etc?
    # NOTE: remove 'sample' 'conc' 'collect' (noise tokens)
    # NOTE: remove 1-2 letter values from match pool?
    #       but still include element names
    # NOTE: any variables too scary to match?
    # NOTE: remove all non alphanumerics
dummy_cols = [
    'watershed', 'station_id', 'date', 'timeEST', 'ph', 'phaeopig',
    'streamflow', 'comment',
              'chlorophyll-A', 'escherria. coli - sample',
    'tempC_deg', 'discharge',
              'precipitation_mm', 'dateCollected', 'dateStart',
    'acidity', 'conductance',
    'Nitrate_N', 'Tot_Kjedhal_N',
    'Unfilt_TK_Nitrogen', 'NH4_NO3_N']

original_stdout = sys.stdout # Save a reference to the original standard output

with open('filename.txt', 'w') as f:
    sys.stdout = f
    test_cases = [bmore_cols, dummy_cols]

    for i in range(len(test_cases)):

        raw_cols = test_cases[i]

        unmatched = raw_cols.copy()
        matches = {}

        ## EXACT MATCHES
        # loop through column names, run search algorithms and fill dictionary
        for col in raw_cols:
            bs_match = binary_search(variables_names, col)

            # if exact match found
            if bs_match[0]:
                print('exact match:', col)
                # add match to dictionary
                matches[col] = bs_match[1]
                # remove from 'unmatched' list
                unmatched.remove(col)
            # else:
            #     print('match not found', col)

        pct_match = (len(matches)/len(raw_cols))*100
        print('binary search algorithm found exact matches for ', pct_match, 'of column names')

        ## EXACT MATCHES, SYNONYMS
        unmatched_synonym = unmatched.copy()
        for col in unmatched_synonym:
            bs_match = binary_search(variables_synonyms, col)

            # if exact match found
            if bs_match[0]:
                print('exact match (synonym):', col)
                # add match to dictionary
                matches[col] = variables[variables.synonyms == bs_match[1]].value.values[0]
                # remove from 'unmatched' list
                unmatched.remove(col)
            # else:
            #     print('match not found', col)

        pct_match = (len(matches)/len(raw_cols))*100
        print('binary search algorithm found exact matches for ', pct_match, 'of column names')

        ## FUZZY MATCHES
        # first, perform binary search algorithm for exact matches
        unmatched_fuzzy = unmatched.copy()

        for col in unmatched_fuzzy:
            if len(col) > 2:
                print('producing fuzzy matches', col)
                # clean before matching
                fz_match_raw = process.extract(var_text_all_cleaners(col.lower()),
                                            var_low_fz_clean,
                                            scorer = fuzz.ratio,
                                            limit = None)
                # if you don't want scores
                # fz_match = [r[0] for r in fz_match_raw if r[1] > score_cutoff]
                # if you DO want scores
                fz_match = [(r[0], r[1]) for r in fz_match_raw if r[1] > score_cutoff]

                # add match to dictionary
                matches[col] = fz_match
                # remove from 'unmatched' list
                unmatched.remove(col)
            else:
                print('-- warning: skipping', col, ', contains less than three characters')

        for key, value in matches.items():
            print('\n', key, ':')
            print('  ', value)

    sys.stdout = original_stdout

## POST: turning algorithms and application into a function which:
def ms_raw_column_reader(filepath,
                         fuzzy_threshold = 50,
                         sheet_id = "1N3NuJL1tzJTVhcI9O8EPV9nEOd2LYlJ7zra_k3cV6fM",
                         sheet_name = "column_matching_synonyms",
                         output_fp = 'matches.json',
                         suffix_rm = None,
                         prefix_rm = None):
    """
    function to read raw input data and match colmun names to macrosheds variables

    TODO:
        - add prefix/suffix cleaner (user input option? or auto-detect?)
    """

    # constants
    # set fuzzy score cutoff
    score_cutoff = fuzzy_threshold

    ## raw data
    # reads in the csv from given filepath
    raw = pd.read_csv(filepath)
    # reads in columns, list and sort (warning that cols must be row 1)
    raw_cols = sorted(list(raw.columns))
    # create simpe dictionary in which each column is a key to an empty list
    matches = {raw_cols[i]: [] for i in range(0, len(raw_cols))}

    ## macrosheds data
    # MacroSheds variable synonyms sheet
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    variables = pd.read_csv(url)
    # names, and lower case names
    variables_names = sorted(list(variables.value))
    var_low = [var.lower() for var in variables_names]
    # synonyms and lower case synonyms
    variables_synonyms = sorted(variables.synonyms.values.tolist())
    variables_synonyms_low = [var.lower() for var in variables_synonyms]
    # list of vars and var synonyms for fuzzy matching,
    # NOTE: with all strings < 2 chars removed
    var_low_fz = variables_synonyms_low + var_low
    var_low_fz_clean = [var for var in var_low_fz if len(var) > 2]

    # loop creates a JSON object from this list, of form:
    # user_columns_json = {'a_user_column': [('a_ms_match', matching_score, 'matching method'),
    #                                        ('a_different_ms_match', matching_score, 'matching method')],
    #                      'a_user_column': [('a_match_column', matching_score, 'matching method')]}

    # loop through raw_cols and apply search algorithms against macrosheds vars
    unmatched = raw_cols.copy()

    ## EXACT MATCHES
    # loop through column names, run search algorithms and fill dictionary
    for col in raw_cols:
        if prefix_rm:
            xcol = col.removeprefix(prefix_rm)
        elif suffix_rm:
            xcol = col.removesuffix(suffix_rm)
        else:
            xcol = col

        bs_match = binary_search(variables_names, xcol)

        # if exact match found
        if bs_match[0]:
            print('exact match:', col)
            # add match to dictionary
            matches[col] = matches[col] + [(bs_match[1], 100, 'binary')]
            # remove from 'unmatched' list
            unmatched.remove(col)
        # else:
        #     print('match not found', col)

    pct_match = (len(matches)/len(raw_cols))*100
    print('binary search algorithm found exact matches for ', pct_match, 'of column names')

    ## EXACT MATCHES, SYNONYMS
    unmatched_synonym = unmatched.copy()
    for col in unmatched_synonym:
        if prefix_rm:
            xcol = col.removeprefix(prefix_rm)
        elif suffix_rm:
            xcol = col.removesuffix(suffix_rm)
        else:
            xcol = col

        bs_match = binary_search(variables_synonyms, xcol)

        # if exact match found
        if bs_match[0]:
            print('exact match (synonym):', col)
            # add match to dictionary
            matches[col] = matches[col] + [(variables[variables.synonyms == bs_match[1]].value.values[0], 100, 'binary_synonym')]
            # remove from 'unmatched' list
            unmatched.remove(col)
        # else:
        #     print('match not found', col)

    pct_match = (len(matches)/len(raw_cols))*100
    print('binary search algorithm found exact matches for ', pct_match, 'of column names')

    ## FUZZY MATCHES
    # first, perform binary search algorithm for exact matches
    unmatched_fuzzy = unmatched.copy()

    for col in unmatched_fuzzy:
        if prefix_rm:
            xcol = col.removeprefix(prefix_rm)
        elif suffix_rm:
            xcol = col.removesuffix(suffix_rm)
        else:
            xcol = col

        if len(xcol) > 2:
            print('producing fuzzy matches', col)
            # clean before matching
            fz_match_raw = process.extract(var_text_all_cleaners(xcol.lower()),
                                        var_low_fz_clean,
                                        scorer = fuzz.ratio,
                                        limit = None)
            # if you don't want scores
            # fz_match = [r[0] for r in fz_match_raw if r[1] > score_cutoff]
            # if you DO want scores
            fz_match = [(r[0], r[1], 'fuzzy') for r in fz_match_raw if r[1] > score_cutoff]

            # add match to dictionary
            matches[col] = matches[col] + fz_match
            # remove from 'unmatched' list
            unmatched.remove(col)
        else:
            print('-- warning: skipping', col, ', contains less than three characters')

    # Serializing json
    json_object = json.dumps(matches, indent=4)

    # Writing to sample.json
    with open(output_fp, "w") as outfile:
        outfile.write(json_object)

    return matches
