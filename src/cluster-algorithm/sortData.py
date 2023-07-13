"""
This file was created to ransfer over some of the responsibility of sorting the data from the find threshold qmd file. 
"""

# Start by reading the file with the file path, in this case the file is included in the repository so the title is just the name 
import pandas as pd
import matplotlib.pyplot as plt
import classificationEquations as ce

global threshold; threshold = 0.5
global buckets

def set_threshold(new_threshold):
    global threshold
    threshold = new_threshold

def get_threshold():
    return threshold 


def read_file():
    # when reading this file, this choses the free text and the child_id columns. The child_id will serve as a unique key for each patient 
    filepath = "/Users/clairelichty/summer2023/SwissTPH/AutomatedClassification/02_timci_day0_data.csv"
    raw_df = pd.read_csv(filepath, low_memory=False)
    df = pd.DataFrame(raw_df, columns = ["dx_oth", "child_id"])
    df = df[(df.dx_oth.notnull())]
    return df


def initiate_buckets():
    global buckets; 
    buckets = {0: {"Ex ChildID" : "ExampleDx_oth_value", "ExSecondChildID" : "Example_DX_oth_value_2"}} 
    return buckets

def data_iterator(df):
    for row in df.itertuples():
        sort_patient(row.dx_oth, row.child_id)

def sort_patient(dx, id):
    # In this, cat_no is type dict, and patient is as well 
    # It returns a dictionary with the sorted data. 
    for cat_no, patient in buckets.items():
        sorted_dx = list(patient.values())[0]
        total_diff = ce.get_sum_distances(sorted_dx, dx)
        if(total_diff < get_threshold()):
            patient[id] = dx
            return; 
    next_cat_no = (max(buckets.keys()) + 1)
    buckets[next_cat_no] = {id:dx}
    return buckets

def get_buckets():
    return buckets

def clear_buckets():
    global buckets
    buckets = {}
    