"""
The purpose of this program is to update the data that is not in the health facility data. 
"""

import selectData
import fileReader
import sortFreeText

global multi; global single_select; global freetext; global updated_data; 

def set_var_names():
    global multi; global single_select; global freetext; 
    multi, single_select, freetext = selectData.get_db_names_to_sort() 
    return multi, single_select, freetext 

def get_var_names():
    return multi, single_select, freetext 

def run_sortFreeText():
    global updated_data; global multi; global single_select; global freetext; 
    set_var_names()
    updated_data = sortFreeText.update_data(multi, single_select, freetext)

def get_updated_data():
    return updated_data 

