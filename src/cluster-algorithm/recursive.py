import evalAlgo as eval 
import sortData as sd 
import csv 

df = sd.read_file() 
# sd.initiate_buckets()
# sd.data_iterator(df)
# sorted_data = sd.get_buckets()


## Evaluate the sorting of the algorithm 

# scores = []
# for i in range (0, 20):
#     thresh = sd.set_threshold(0.5 + (i * 0.1)) 
#     sd.data_iterator(df)
#     sorted_data = sd.get_buckets()
#     scores.append(eval.find_outliars_dict(sorted_data))
# print(scores)

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

print(dict_to_convert)

file_name = "/Users/clairelichty/summer2023/SwissTPH/SwissTPH-ClusterAlgo/Sorted_Values/Threshold_10.csv"
with open(file_name, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ["category", "child_id", "dx_oth"])
    writer.writeheader()
    writer.writerows(dict_to_convert)
