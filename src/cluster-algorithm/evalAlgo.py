import sortData as sd
import classificationEquations as ce 
import compareToStandards as cs 
import statistics as stat

""" 
The purpose of this algorithm is to evaluate the efficency of the data sorting program and to adjust it as needed 
"""

# The "Score" for a given sorting will take the following factors into account: 

# METRIC 1: 
    # find the average range across all of the categories 
def avg_range(sorted_dict):
    ranges = []
    for category, patient in sorted_dict.items():
        ranges.append(cs.find_range_dict(patient))
    return stat.mean(ranges)
    
# METRIC 2: 
    # Find the number of categories that only have one value 
def count_singletons(sorted_dict):
    singletons = 0 
    for patient in sorted_dict.values():
        if(len(patient) == 1):
            singletons += 1
    return singletons

def find_len_stdv(dict):
    all_lens = []
    for patients in dict.values():
        all_lens.append(len(patients))
    return stat.stdev(all_lens)

def remove_singletons(dict):
    cleaned_dict = {}
    for cats, patients in dict.items():
        if(len(patients) != 1):
            cleaned_dict[cats] = patients
    return cleaned_dict 



# Find the high and low ends for the outliars.     
def find_len_fences_dict(dict):
    all_lens = []
    for patients in dict.values():
        all_lens.append(len(patients))
    return find_len_fences_list(all_lens)
    

def find_len_fences_list(list):
    med = stat.median(list)
    high_lens = []
    low_lens = []
    for len in list:
        if len >= med:
            high_lens.append(len)
        else: 
            low_lens.append(len)
    Q3 = stat.median(high_lens)
    Q1 = stat.median(low_lens)
    IQR = Q3 - Q1
    return (Q3 + (IQR * 1.5),  Q1 - (IQR * 1.5))    


# METRIC 3: 
    # Calcualte the number of outliars in the dataset in terms of number of items in a category. 
def find_outliars_dict(sorted_dict):
    sorted_dict = remove_singletons(sorted_dict)
    high, low = find_len_fences_dict(sorted_dict) 
    outliars = [] 
    for cat_no, patients in sorted_dict.items():
        if (len(patients) > high):
            outliars.append(cat_no)
        elif (len(patients) < low): 
            outliars.append(cat_no)
    return len(outliars)

def find_outliars_list(list):
    high, low = find_len_fences_list(list)
    outliars = [] 
    for item in list:
        if (item > high or item < low):
            outliars.append(item)
    return outliars


# METRIC 4: 
    # Get the range of each of the categories and then compare these values to each other, flagging any outliars. 
def find_range_outliars(dict):
    ranges = []
    for cat, patients in dict.items():
        ranges.append(cs.find_range_dict(patients))
    outliars = find_outliars_list(ranges)
    return len(outliars)


# Combine all the metrics into one value that works as a "Score" for the certain threshold 
    # adjust the threshold accordingly 
def sum_score(dict):
    singles = count_singletons(dict)
    outliar_count = find_outliars_dict(dict)
    count_range_outlairs = find_range_outliars(dict)
    return (singles + outliar_count + count_range_outlairs)

    