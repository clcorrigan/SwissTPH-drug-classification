import re
import csv
import fileReader
import fileReaderCB

global multi; global categorized_data; global freetext
multi = {}
categorized_data = {}

def get_db_names_to_sort():
    """
    Simply a getter for other files in the program to use. Returns the multi, categorized_data, and freetext categories 
    Will return nothing select_db_names_to_sort hasn't been used yet.  
    """
    return multi, categorized_data, freetext


def get_codebook():
    """
    Works as a getter for the codebook in dictionary form. 
    """
    codebook = fileReaderCB.get_data() #gets the codebook from the codebook file reader. 
    return codebook #returns the codebook

def select_db_names_to_sort():
    """
    Looks through the codebook and selects all the drug categories. 
    27-06-23: Does not account for the _hf information 
    """
    global freetext
    cb, cats = codebook_and_db_names()
    sort_cats_auto(cb, cats)
    freetext = get_freetext_db_name()
    return multi, categorized_data, freetext

def codebook_and_db_names():
    """
    Performs two function calls to get the information that is needed to call sort_cats_auto
    """
    db_names = select_cats() 
    cb = get_codebook()
    return cb, db_names


def select_cats(cat_type = "^rx_", exclude = "_hf$"):
    """
    Takes in the category type, the default of this is 'rx', or drug types. 
    Returns a list of db_names, such as ['rx_amoxicillin', 'rx_penicillinG']
    """
    data_table = fileReader.get_data()
    db_name_categories = []
    for attribute in data_table[0]:
        if(re.search(cat_type, attribute) != None):
            if(re.search(exclude, attribute) == None):
                db_name_categories.append(attribute)
    return(db_name_categories)



def sort_cats_auto(codebook, cats):
    """
    Looks through the codebook and calls one of two functions
    Either single_select or multi_select, which operates as a dropdown menu. 
    """
    i = 0
    for item in codebook:
        if(item["db_name"] in cats):
            if(item["type"] == "single"):
                single_select(item)
            elif(item["type"] == "multiple"):
                multi[item["db_name"]] = {}
                multi_select(codebook, i, item)
            else:
                print(item)
        i+=1
    
    
def get_freetext_db_name():
    """
    Gets the name of of the category that is the free text category that contains the data that is being sorted. 
    """
    freetext = input("What is the 'db_name' for the freetext category you are trying to sort: ")
    return freetext


def multi_select(codebook, i, label):
    """
    Takes in the codebook and the index in the codebook that the multi_select options. 
    Returns the dictionary multi -- which is a dictionary with all the multi_select_options 
    Ex. Format: 
        {rx_antibio_oth = {75: [Cefadroxil, Oracefal], 55: [Cefixime, Oroken, Ofiken, Fixim]}, 
        rx_misc = {100: [Albendazole, Alben], 103: [Cetirizine, Genset], 23: [Diazepam, Valium]}}
    """
    all_cats, all_values = list_categories_and_values(codebook)
    # 10:36 28/06/23: In instances when 96 is not the last option, you need to fix this in the codebook, as of right now. 
    while (all_values[i] != "96"): #Uses the value 96 because that is the value that is used to indicate "None of the above"
         multi[label["db_name"]][all_values[i]] = clean_cats(all_cats[i])
         i+=1

def list_categories_and_values(codebook):
    """
    Goes through the codebook and returns all the categories and values in a list form. 
    """
    all_cats = []; all_values = []
    for item in codebook:
        all_cats.append(item["category"]); all_values.append(item["value"])
    return all_cats, all_values 


def single_select(item):
    """
    This handles the categories in the data that are single select options 
    It returns the dictionary "categorized_data"
    categorized_data.keys() = database_names
    categorized_data.values() = lists of real drug names -- returned by clean_cats 
    """
    label = item["label"]
    categorized_data[item["db_name"]] = clean_cats(label)



def clean_cats(label):
    """
    Takes in the "label" data from the code book
    Example label = "Amoxicilline (Amox) OR Clamoxyl OR Bactox OR Alfamox OR Teramox OR Hiconcil"
    Returns a list of all of the drugs separated, Ex. ["Amoxicilline", "Amox", "Clamoxyl", "Bactox", "Alfamox", "Teramox", "Hiconcil"]
    """
    alt_drugs = []; drug_names_reg = []; 
    label = label.lower()
    alt_names = re.findall("\(.*\)", label)
    for alt in alt_names:
        label = label.replace(alt, "")
        alt = alt.strip("()")
        if "/" in alt:
            alt_drugs = alt.split(" / ")
        else: 
            alt_drugs = [alt]
    drug_names_reg = label.split(" or ")
    return (drug_names_reg + alt_drugs)
