import evalAlgo as eval 
import sortData as sd 
import csv 

def main():
    df = sd.read_file() 

    sd.clear_buckets()
    sd.initiate_buckets()
    sd.set_threshold(1.0)
    sd.data_iterator(df)
    sorted_data = sd.get_buckets()


    ## Converting this dictionary one that will be able to convert to a CSV file 

    dict_to_convert = []
    for category, patient_data in sorted_data.items():
        for child_id, dx_oth in patient_data.items():
            new_patient = {}
            new_patient["category"] = category; 
            new_patient["child_id"] = child_id; 
            new_patient["dx_oth"] = dx_oth; 
            dict_to_convert.append(new_patient)


    ## Update the file name 
    file_name = "/Users/clairelichty/summer2023/SwissTPH/SwissTPH-ClusterAlgo/Sorted_Values/Threshold_10.csv"
    with open(file_name, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["category", "child_id", "dx_oth"])
        writer.writeheader()
        writer.writerows(dict_to_convert)
        
    return confirm_categories(sorted_data)

def confirm_categories(sorted_data):
    labeled_data = {}
    for category, patient_data in sorted_data.items():
        print(list(patient_data.values())[0])
        action = input("(1): Assign ICD-11 Code \n (2): Assign Other Code \n (3) Ignore")
        if(action == "2" or action == "1"):
            label = input("Please enter the associated code:")
            for id, data in patient_data.items():
                labeled_data[id]= {"Child_id": id, "dx_oth" : data, "label": label}
        elif(action != "3"):
            print("Please select either 1, 2, or 3, from the dataset")
    return labeled_data


labeled_data = main()
