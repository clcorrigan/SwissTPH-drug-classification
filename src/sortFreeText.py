import re 
import csv
import fileReader
import selectData

global multi; global categorized_data; global freetext; 
multi, categorized_data, freetext = selectData.select_db_names_to_sort() 

print("running sortFreeText.py")

# print(freetext)

global multi_catch; global cat_catch; global no_catch; 
multi_catch = []; cat_catch = []; no_catch = []; 

global count; count = 0; 

def get_clean_data():
    clean_data = fileReader.get_dict()
    return clean_data

# read from free text and add that to a new dictionary 
def update_data():
    global updated_data; updated_data = get_clean_data()
    for item in updated_data:
        item = update_free_text(item)
    print("Total number of free text entries, " + str(count))
    # print(all_cat_opts())
    return updated_data 

def update_free_text(item):
    global count
    entry = item[freetext].lower()
    multi_opts = get_multi_options()
    all_values = clean_entry(entry)
    for value in all_values:
        if value in all_cat_opts():
            add_to_cat_data(item, value)
            count += 1
        elif value in multi_opts:
            item = add_to_multi_data(item, value)
            count +=1
        elif value != "":
            if value not in no_catch:
                no_catch.append(value)
                count += 1

    return item 


def clean_entry(entry):
    entry = entry.replace("sp", "")
    entry = entry.replace("sirop", "")
    entry = entry.strip()
    if("-" in entry):
        all_values = entry.split("-")
    else:
        all_values = entry.split(" ")
    i = 0
    for value in all_values:
        value = value.strip()
        i+=1
        if i == 10:
            break
    return all_values


def all_cat_opts():
    all_cat_opts = []
    for item in categorized_data.values():
        all_cat_opts += item
    return all_cat_opts


#coming into this, the "item" is one patient and the entry is derived from the  values in the free text category. 
def add_to_multi_data(item, entry): 
    global count
    for drug_name, dict in multi.items():
        for key, value in dict.items():
            if entry in value: 
                #This means that the "key" here is going to be the number that we are going to add to the updated data value. 
                # print(key); print(drug_name); print(type(item[drug_name]))
                if(item[drug_name] == "" or item[drug_name] == "96"):
                    item[drug_name] = key
                elif(item[drug_name] != key):
                    item[drug_name] += ", " + key
                else:
                    count -=1; 
                
    
    if entry not in multi_catch:
        multi_catch.append(entry)
    return item

def add_to_cat_data(item, entry):
    for drug_name, list in categorized_data.items():
        if entry in list:
            if(item[drug_name] == "0" | item[drug_name] == ""):
                item[drug_name] = "1"        
    if entry not in cat_catch:
        cat_catch.append(entry)
    return item 


def get_multi_options():
    all_multi_ops = []
    for query in multi:
        value_dict = multi[query] 
        for value in value_dict:
            all_multi_ops += value_dict[value]
    return all_multi_ops
