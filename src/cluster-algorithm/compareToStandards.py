"""
The purpose of this program is to compare the IMCI and IDC-11 
standards to the categories that are created by the three thresholds as they are now. 
"""

import csv
import pandas as pd 
import classificationEquations

global sorting_count; global standards; global count_reduced; 
sorting_count = {}
count_reduced = 0 


# Creating A Dataframe with the IMCI/ICD-11 standards: 
def readfile():
    global standards
    standards = pd.read_csv("IMCI-ICD.csv")
    return standards 

def get_standards():
    global standards
    return standards 

def get_sorting_count():
    print(count_reduced)
    return sorting_count


def compare_with_df(dataframe):
    """
    Intention of this is to iterate through the dataframes that are already sorted and to assign one of the classifications to each existing dataframe. 
    """
    global count_reduced
    for row_stand in standards.itertuples():
        dx_value = row_stand._2
        for row in dataframe.itertuples():
            comp_value = row.dx_oth
            jar_comp = classificationEquations.compare_with_jar(comp_value, dx_value)
            lev_comp = classificationEquations.compare_with_lev(comp_value, dx_value)
            n_comp = classificationEquations.compare_with_ngram(comp_value, dx_value)
            if(sum([jar_comp, lev_comp, n_comp]) >= 2):
                sorting_count[dx_value] = dataframe
                count_reduced += len(dataframe)
                return True
            


def find_range_df(dataframe):
    first_val = dataframe.iloc[0].dx_oth
    max_dist = 0
    for row in dataframe.itertuples():
        jar_comp = classificationEquations.get_jaro_distance(row.dx_oth, first_val)
        var_comp = classificationEquations.get_lev_distance(row.dx_oth, first_val)
        ngram_comp = classificationEquations.get_ngram_distance(row.dx_oth, first_val)
        total_dist = (jar_comp + var_comp + ngram_comp)
        print(str(total_dist), first_val, row.dx_oth)

        if total_dist > max_dist:
            max_dist = total_dist 
    return max_dist


def find_range_dict(dict):
    first_val = list(dict.values())[0]
    max_dist = 0
    for word in dict.values():
        jar_comp = classificationEquations.get_jaro_distance(word, first_val)
        var_comp = classificationEquations.get_lev_distance(word, first_val)
        ngram_comp = classificationEquations.get_ngram_distance(word, first_val)
        total_dist = (jar_comp + var_comp + ngram_comp)
        if total_dist > max_dist:
            max_dist = total_dist 
    return max_dist
    