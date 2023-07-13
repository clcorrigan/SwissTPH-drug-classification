import pandas as pd
from Levenshtein import distance as lev
from math import floor, ceil 


global lev_thresh; global jar_thresh; global n_thresh; 
lev_thresh = 0.5
jar_thresh = 0.5
n_thresh = 0.5

jar_distances = []
lev_ratios = []
n_sim_values = [] 

def get_jaro_distances():
    return jar_distances 

def get_lev_ratios():
    return lev_ratios

def get_n_sim_values():
    return n_sim_values


def pass_fail(ratio, threshold):
    if(ratio >= threshold):
        return False 
    else: 
        return True
    
def get_lev_distance(string1, string2):
    """
    Calculates the distance between the two strings using the lev package. 
    """
    string1 = string1.lower() 
    string2 = string2.lower()
    dist = lev(string1, string2)
    max_len = max(len(string1),len(string2))
    ratio = dist/max_len
    lev_ratios.append(ratio)
    return ratio

def compare_with_lev(string1, string2):
    """
    Comparing the two strings with the Lev package/library. 
    Calls the pass/fail function and returns whether the value has passed or failed. 
    """
    ratio = get_lev_distance(string1, string2)
    return pass_fail(ratio, lev_thresh)

def get_jaro_distance(string1, string2):
    """
    Calculates the distance between two strings. 
    """
    s1 = string1.lower()
    s2 = string2.lower() 

    if(len(s1) == 0 or len(s2) == 0):
        print(s1, s2)
        return False 


    max_dist = floor(max(len(s1), len(s2))/2)-1
    match = 0

    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    for i in range(len(s1)):
        for j in range (max(0, i - max_dist), min(len(s2), i+max_dist + 1)):
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1 
                match += 1 
                break 
    if (match == 0):
        return False
    
    t = 0 
    point = 0 

    for i in range(len(s1)):
        if (hash_s1[i]):
            while(hash_s2[point] == 0):
                point += 1 
            if (s1[i] == s2[point]):
                t+=1
            point +=1
    t = t//2

    # getting the Jaro Similarity

    similarity = (match/len(s1) + match/len(s2) + (match-t)/match)/3.0

    # getting the Jaro Distance
    dist = 1 - similarity 
    return dist

def compare_with_jar(string1, string2):
    dist = get_jaro_distance(string1, string2) 
    return pass_fail(dist, jar_thresh)


def get_ngram_distance(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower() 

    s1_grams = string_to_grams(s1)
    s2_grams = string_to_grams(s2) 

    # Find the union and the intersection of the two sets
    grams_union = s1_grams.union(s2_grams)
    grams_intersection = s1_grams.intersection(s2_grams)

    # Calculate the n-gram similarity value from this 
    ngram_similarity = (len(grams_intersection))/(len(grams_union))
    ngram_distance = 1 - ngram_similarity 
    return ngram_distance


def string_to_grams(string):
    # Turns the String to a set of grams of a certain size 
    # The gram_size here is very changable. 
    gram_size = 3
    gram_set = set()
    for i in range(0, len(string)):
        if(i+gram_size <= len(string)):
            gram_set.add(string[i:i+gram_size])
    return gram_set



def compare_with_ngram(s1, s2):

    # Start by taking the two strings and converting them into sets of 3 letter areas. 
    # for the purposes of this algorithm, we are going to use 3 grams, this is something that is iterable to increase accuracy 
    ngram_distance = get_ngram_distance(s1, s2)
    n_sim_values.append(ngram_distance)
    return pass_fail(ngram_distance, n_thresh)
    
   
def get_sum_distances(s1, s2):
    jar_dist = get_jaro_distance(s1, s2)
    lev_dist = get_lev_distance(s1, s2)
    ngram = get_ngram_distance(s1, s2)
    return (jar_dist + lev_dist + ngram)
