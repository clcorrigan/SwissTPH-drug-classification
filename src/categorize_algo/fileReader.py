import re 
import csv 
from enum import Enum 

poss_fts = (".csv")
global filepath 
filepath = ""
global sheet_heads
global all_data_dict

def get_data():
    return all_data_dict 


def get_dict():
    file_type = get_ft()
    return validate_file(file_type)

def get_filepath():
    return filepath

def set_filepath(filepath_new):
    global filepath
    filepath = filepath_new


# takes in the path to the file that you want to clean up
# returns the file type as a string 
def get_ft():
    global filepath 
    if(filepath == ""):
        filepath = input("Insert the file path of the data to be sorted: ")
        end_pattern = ".[a-z]+$" 
    file_type = (re.search(end_pattern, filepath)).group()
    return file_type 


# reads the file based on the file type. Right now this only works with .csv files. 
# read_file takes in the file type and uses the global variable "filepath" to read the data into a dictionary. 
# returns the data as a dictionary. 
def read_file(file_type):
    global all_data_dict; 
    if(file_type == ".csv"):
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter= ",")
            all_data_dict = list(reader); 
            return all_data_dict


def validate_file(file_type):
    if(poss_fts.count(file_type) != 0):
        return read_file(file_type) 
    else:
        print("Not a valid file type. Only accepts files .csv")
        print("Please try again")
        get_ft()            

    