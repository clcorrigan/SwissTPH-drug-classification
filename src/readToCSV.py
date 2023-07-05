import csv 
import re

global updated_data; 
global dest_file_name; 

def set_updated_data(new_data):
    global updated_data
    updated_data = new_data

def establish_file_path():
    dest_file_path = input("Please copy the path to the file where you would like to include the updated data: ")
    return dest_file_path

def establish_dest_file_name():
    global dest_file_name; 
    dest_file_name = input("Please type the name that you want the file to be named: ")
    return dest_file_name 

def write_csv_file():
    full_file_name = establish_file_path() + "/" + establish_dest_file_name()
    with open(full_file_name+".csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames= make_headers())
        writer.writeheader()
        writer.writerows(updated_data)


def make_headers():
    headers = updated_data[0]
    return headers; 