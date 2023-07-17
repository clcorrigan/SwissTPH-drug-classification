import re 
import csv 
import sortFreeText
import selectData
import fileReader

global updated_data; updated_data = sortFreeText.update_data()
global original_data; original_data = selectData.dict
global freetext; global clean_data; 
global categorized_data; global multi_data; multi, categorized_data,freetext,clean_data = selectData.select()


print(categorized_data.keys())


def filter_patients():
    valid_count = 0
    total_count = 0
    for i in range(0, len(updated_data)):
        patient_diff = 0
        for value in categorized_data.keys():
            if(patient_diff == 0):
                if((updated_data[i][value] != clean_data[i][value])):
                    patient_diff = 1
                    print(str(value) + str(updated_data[i][value]) + str(updated_data[i][freetext]))
                    print(clean_data[i][value])
                    ver = input("Is this update valid? Y/n")
                    if(ver == "Y"):
                        valid_count += 1 
                        total_count +=1
                    elif(ver == "n"):
                        total_count+=1
                patient_diff = 1 
        print("", end = "")
    print(valid_count)
    print(total_count)

filter_patients() 
