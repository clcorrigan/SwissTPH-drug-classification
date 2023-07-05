import selectData
import sortFreeText

def set_vars():
    global multi; global single_select; global freetext; global updated_data; 
    multi, single_select, freetext = selectData.get_db_names_to_sort()

def get_updated_hf_data():
    return updated_data 

def sort_freetext_hf():
    global updated_data
    set_vars()
    updated_data = sortFreeText.update_data(multi, single_select, freetext)
    return updated_data


def update_names():
    """
    updates the names of the values that we are looking at, so that it looks at the health facility information as opposed to the non-health facility data. 
    """
    add_hf_to_dict_keys(multi)
    add_hf_to_dict_keys(single_select)
    freetext += "_hf"


def add_hf_to_dict_keys(dict_name):
    """
    This updates the values from the original data sort so that they have the health facility ending. 
    This one works on multi and single_select options as of right now. 
    """
    for item in dict_name.keys():
        hf_item = item + "_hf" 
        dict_name[hf_item] = dict_name[item]
        dict_name.pop(item)

