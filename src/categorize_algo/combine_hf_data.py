import sort_hf 
import sort_non_hf 

global hf_data; global non_hf_data; global combined_data; 

combined_data_db_names = ["child_id"]
old_data_names = []
combined_data = []

def get_updated_dict():
    return combined_data


def set_data_sets():
    global hf_data; global non_hf_data; 
    hf_data = sort_hf.get_updated_hf_data()
    non_hf_data = sort_non_hf.get_updated_data()

def create_updated_dict():
    set_data_sets()
    make_new_db_names()
    check_hf_and_reg()
        
def make_new_db_names():
    """
    Similar to past functions that take in these dictionaries and create a list of all the names that you are looking for, this one goes through and adds them to the list wiht the _new ending to
    distinguish them from the original _hf and non _hf data. 
    """
    multi_select, single_select, freetext = sort_non_hf.get_var_names()
    global combined_data_db_names; global old_data_names; 
    for db_name in multi_select.keys():
        combined_data_db_names.append(db_name + "_new")
        old_data_names.append(db_name)
    for db_name in single_select.keys():
        combined_data_db_names.append(db_name + "_new")
        old_data_names.append(db_name)
    combined_data_db_names.append(freetext + "_new")
    old_data_names.append(freetext)

    # combined_data.append(combined_data_db_names)


def check_hf_and_reg():
    """
    this function iterates through the options from both the hf and non hf data, and then checks if there is a difference in the marking of these categories. 
    """
    for patient_data in hf_data:
        new_patient_data = {"child_id": patient_data["child_id"]}
        for db_name in patient_data.keys():
            if db_name in old_data_names:
                try:
                    hf_value = patient_data[db_name + "_hf"] 
                    reg_value = patient_data[db_name]
                    check_null_and_add(hf_value, reg_value, db_name, new_patient_data)
                except KeyError:
                    add_data_to_new_cat(db_name, new_patient_data, patient_data[db_name])
                # This is checking if any of the values, either the hf or regular value isn't null
                
        combined_data.append(new_patient_data)

def check_null_and_add(hf, reg, db_name, new_patient_data):
    if values_are_not_null(hf, reg):
        new_val = combine_data(hf, reg, db_name)
        add_combined_data_to_new_cat(db_name, new_patient_data, new_val)
    else:
        add_data_to_new_cat(db_name, new_patient_data, reg)

        

def values_are_not_null(hf, reg):
    """
    This checks the hf_values and the reg values 
    """
    return ((hf!= "0" ) or (reg != "0") or (hf == "" ) or (reg == "") or (reg == "96") or (reg == "96"))


def combine_data(hf, reg, db_name):
    multi, single, free = sort_non_hf.get_var_names()
    new_val = ""
    """
    Combine data between the hf_value and the reg_values by being "greedy" 
    Returns the value to the function that called it. 
    Right now causes an error where it mischaracterizes data as being "1"
    """
    if(hf == reg):
        new_val = hf
    elif ((hf == "1" or reg == "1") and db_name in single):
        new_val = "1"
    else: 
        # In this case, the hf and reg are in an additional category and there are certain values that are not in it. 
        hf_set = set(hf.split(";"))
        reg_set = set(reg.split(";"))
        all_vals = list(hf_set.union(reg_set))
        new_val = ""
        for val in all_vals:
            new_val += val + ";"
    return new_val
        

def add_data_to_new_cat(db_name, new_patient_data, reg_value):
    """
    Adding the data as is to the category in the data. 
    """
    new_db_name = db_name + "_new"
    new_patient_data[new_db_name] = reg_value


def add_combined_data_to_new_cat(db_name, new_patient_data, new_value):
    """
    Combining the data and adding it to the new category
    """
    new_db_name = db_name + "_new"
    new_patient_data[new_db_name] = new_value 

