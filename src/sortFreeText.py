import fileReader
import selectData

# def main():
#     global multi; global single_select; global freetext; 
#     multi, single_select, freetext = selectData.select_db_names_to_sort() 
#     return update_data(multi, single_select, freetext)

global multi; global single_select; global freetext; 

# read from free text and add that to a new dictionary 
def update_data(multi_ext, single_select_ext, freetext_ext):
    global multi; global single_select; global freetext; 
    multi = multi_ext; single_select = single_select_ext; freetext = freetext_ext; 
    """
    The main function to run -- updates all the data and returns the updated data. 
    """
    global updated_data; updated_data = fileReader.get_data()
    for patient in updated_data:
        patient = update_patient_data(patient)
    return updated_data 

def update_patient_data(patient):
    """
    This updates the data for each specific patient. 
    first it gets the free text entry in the correct format, and then sorts them, 
    returning the updated patient data to be replaced in the updated_data dictionary. 
    """
    freetext_entry = patient[freetext].lower()
    all_values_in_entry = clean_entry(freetext_entry) # all_values is a list that is the entry split into the individual drug names in the data. 
    return sort_values(all_values_in_entry, patient) # returns the updated patient data in the original format. 

def sort_values(all_values_in_entry, patient_data):
    """
    Goes through the drug names in the free text entry 
    updates the patient data using this information. 
    """
    for drug_name_in_entry in all_values_in_entry:
        patient_data = update_data_with_freetext(patient_data, drug_name_in_entry)
    return patient_data 

def update_data_with_freetext(patient_data, entry_drug_name):
    """
    Decides if the free text entry is a categorical option, that is a single_select
    or if it's a multi_select option 
    Calls the correct data call accordingly. 
    """
    if entry_drug_name in all_cat_opts():
        patient_data = add_to_cat_data(patient_data, entry_drug_name)
    elif entry_drug_name in get_multi_options():
        patient_data = add_to_multi_data(patient_data, entry_drug_name)
    return patient_data



def clean_entry(ft_entry):
    """
    Takes in the original freetext entry and removes 
    - all the common additional entries
    - strips the data to remove leading or trailing spaces. 

    This hard coding is not ideal, but it is hard to automate this. 
    - to add another common word to remove, just add it to the list. 
    """
    common_words = ["sp", "sirop", "cream", "lotion", "eye drops"]
    for word in common_words:
        ft_entry = ft_entry.replace(word, "")
    ft_entry = ft_entry.strip()
    return split_ft_entry(ft_entry) # returns to update_patient_data()
    

def split_ft_entry(ft_entry):
    """
    If the doctor uses a hyphen to split different drug names, the code will split on that 
        - In looking at the data, there were few instances that involved a hyphen splitting on drug name 
    If not, things were split on spaces. 
    All data was stripped of leading and trailing spaces. 
    """
    if("-" in ft_entry):
        all_values = ft_entry.split("-")
    else:
        all_values = ft_entry.split(" ")
    for value in all_values:
        value = value.strip()
    return all_values # returns to clean_entry()


def all_cat_opts():
    """
    Gets all the categorical data options as a list
    """
    all_cat_opts = []
    for item in single_select.values():
        all_cat_opts += item
    return all_cat_opts


def add_to_multi_data(patient_data, entry_drug_name): 
    """
    For multi select options, traverses the multi dictionary, and adds the correct values to the patient data. 
    Returns the patient data. 
    The variable names "value" and "category" correlate directly to those from the data codebooks. 
    """
    for drug_name, value_category_dict in multi.items():
        for value, category in value_category_dict.items():
            if entry_drug_name in category: 
                if(patient_data[drug_name] == "" or patient_data[drug_name] == "96"): 
                    patient_data[drug_name] = value
                elif(patient_data[drug_name] != value):
                    patient_data[drug_name] += ";" + value 
    return patient_data

def add_to_cat_data(patient_data, freetext_entry):
    """
    Updates the patient data to correctly account for the freetext_entry. 
    """
    for drug_name, list in single_select.items():
        if freetext_entry in list:
            if((patient_data[drug_name] == "0" )| (patient_data[drug_name] == "")):
                patient_data[drug_name] = "1"        
    return patient_data 


def get_multi_options():
    """
    gets the drop down options in list form. 
    """
    all_multi_ops = []
    for query in multi:
        value_dict = multi[query] 
        for value in value_dict:
            all_multi_ops += value_dict[value]
    return all_multi_ops
