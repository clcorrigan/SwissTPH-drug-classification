# SwissTPH-drug-classification
A set of programs that are used to help automatically sort drug names that have been inserted as freetext rather than selected from a drop down menu


## Table of Contents 
1. Overview Explaination of Code 
2. Codebook and Data Requirements
3. Files Funcionality 
    - fileReader.py
    - readToCSV.py
    - sortFreeText.py
    - verifyData.py 
4. How to Install and Run the Project 
5. External Libraries 
6. Future Applications of the Code 
7. Common bugs and trouble shooting 

## 1. Overview Explaination of Code 

In this project, the goal of the code is to take in input:
- in one CSV file containing patient data, 
- one CSV file that is the code book
- the db_name (database name) of the freetext category that needs to be updated 

and output: 
- CSV file with more accurate drug data in the same format as the patient data input

The motivation behind this data was to more easily utilize the free text data. 
- As of 28 June, 2023, this proved significantly effective: 
    - On 500 randomly selected patients: 
        Before the running on the program, the freetext category was accounted for correctly 82.4% of the time 
        After running the program, the freetext category was accounted for correctly 95.8% of the time. 
        - There were 67 instances of the program correctly sorting freetext (going from incorrect to correct)
        - There were 0 instances of the program incorrectly sorting freetext (going from correct to incorrect)
        - There were 21 missed instances of sorting freetext (going from incorrect to incorrect)

## 2. Codebook and Data Requirements 

Because this project reads directly from the codebook and the patient data information, it requires these to be in a specific format. 

### Codebook Requirements 
    
Because this project originally was working with the TIMICI data from Kenya, the codebook from that data set is what the code knows how to read from. 

- A format of the code is included below 

| name | db_name | label | type | ref | value | category 
| --- | --- | --- | --- | ---| ---- | ------ | 
| amoxicillin | rx_amoxicillin | Amoxicillin \(Amox\) OR Amoxil | single | YESNO | 1 | YES | 
| | | | | | 0 | NO | 
| antimicrobials | rx_antibio_oth | k10\) Please indicate whether the following items are among the items listed on the drug prescriptions | multiple | ANTIMICROBIALS | 107 | Acylovir | 
| | | | | | 80 | Amikacin (AM) | 
| | | | | | 108 | Aminosidine OR Daboral | 
| | | | | | 81 | Cefezolin | 

**There are a few important things to note here** 
1. Each separate category has it's own row in the codebook. The format is not such that there is one cell that has all the data in one block. 
    - For Example: 
    > 75=Céfadroxil OU Oracéfal|55=Céfixime OU Oroken OU Ofiken OU Fixim|63=Doxycycline OU Vibra|64=Erythromycine (Ery)|65=Flucloxacilline OU Staphypen OU Flustaph|67=Isoniazide (sans rifampicine, etc) OU Rimifon|68=Mupirocine OU Bactroban|70=Phénoxyméthylpénicilline OU Ospen|71=Rifampicine (sans isoniazide etc) OU Rimactan|38=Rifampicine / Isoniazide (RH)|39=Rifampicine / Isoniazide / Pyrazinamide / Ethambutol (RHZE) OU Lamprène|74=Chlortétracycline OU Tétracycline OU Auréomycine|96=Aucun des éléments ci-dessus 
    - All being in the "value" category would not work and would lead to errors.  
2. For cells that hold multiple different drug names that apply to a specific category or value 
    - Each value needs to be seperated by an OR, either uppercase or lower case 
        - If you are using the codebook from a language is not English, you need to go and change the values between drugs to be OR 
        - This does not apply for drugs that are in parentheses, for example \(Amox\)
3. The headers that matter are db_name, label, type, value, and category
       - If the headers are not spelled this way exactly 
4. Drug name spellings matter, but things are not case sensitive
    - If you have drug names that are in an language that uses accents, go back in the drug information and include spellings both with and without accents
          - Example 
              - Change "Céfadroxil OR Oracéfal" to be "Céfadroxil OR Oracéfal OR Cefadroxil OR Oracefal"
    - If there are common acronyms or alternate spellings include those as well 
    - You do not need to account for capital or lowercase letters

### Data Requirements 
Most of the time the codebook already matches the data so everything should be good.
- Currently in the data there will be two different versions of drug data
      1. One that has "_hf" at the end. This comes from the health facility as opposed to from the drug information. 
              - As of 28 June 2023: These scripts ignore the health facility data, hopefully by the end of the summer this shoudl be different
      2. One that does not have the "_hf" data, this is the data that is manipulated by this program. 

## 3. File Functionality 

### a. fileReader.py


**functions included in fileReader.py**

|function name|return value|
| --- | --- |
| get_filepath() | string, path to the .csv file of the data|
| get_ft() | string of the file_type|
| read_file(file_type) | returns a dictionary containing all of the data from the csv file| 
| validate_file(file_type) | either reads the file and returns the dictionary or throws an error| 

**use case of code**

Used to read the csv file and return a dictionary. 
As of right now it is only called in the selectData.py and sortFreeText.py python files. 

**Common Bugs**
- Not having the data in the correct format, a comma separated values 
- Having errors in the filepath. The file path should be in the format with Users/username/downloads/.../file.csv 
- Make sure to copy the entire file path. 

### b. readToCSV.py

**functions included in readToCSV**

| function name | return value | notes | 
| --- | --- | --- | 
| establish_file_path() | string of filepath | function to take user input of the file path to the location they want the file stored in | 
| establish_file_name() | string of filename | function of the file name, not including the .csv ending | 
| write_csv_file() | NA | calls est_file_path/name and uses these to write the dictionary of updated values to a CSV file and saves it in that location | 


**use case of code**

This is the main file. Just running this file effectively runs all other files. 

**Common Bugs**

- Not having the correct format for the location 
- As of 29, June 2023: This doesn't check for/throw exceptions if there is an error in the path, will go to the end and then have an error in the code. Will break the process. 

### c. sortFreeText.py 

**Functions Included**

|function name| return value| notes | 
| --- | --- | --- |
| update_data() | returns a dictionary of the updated data | This is the main function of this script. It contains all the others and calling it in another file effectively sort all the data and return it. | 
| update_patient_data(patient) | updated patient data (dict) | |
| sort_values(all_values_in_entry, patient_data) | updated patient data | in all subsequent functions, "entry" is used to refer to the freetext entry|
| update_data_with_freetext(patient_data) | returns patient data | | 
| clean_entry(ft_entry) | returns the entry, split into the different drugs | | 

**Use Case**

This code is used to categorize the freetext information. 
- It starts by reading the information in the freetext category and storing it in a variable freetext_entry (also called ft_entry)
- It takes this information and then cleans the string and splits it into a list of strings, with each option on the list representing one of the drugs in the list. 
- Then it looks through this list, and for any option that is also included in either the list of single select drugs or the list of multi-select drugs, it updates the patient data to represent those datatypes. 
- This program includes a call to the selectData.py program (below), which is necessary because it needs to know which categories to look for when sorting the drug data. 

**Common Bugs**

This code has not proved to be very buggy as of right now. There are a few central areas that might need attention. 
- In the list of "common_words" in the clean_data(ft_entry) function, some can be added or removed to tinker with this data to make it more accurate. 
    - As of 29 June, 2023: the list of "common words" is ["sp", "sirop", "cream", "lotion", "eye drops"]. These are words that are commonly added by the doctors in the freetext categories, but are not included in the codebook. 
    - So far, there has not been reduction in accuracy by adding words to the list, but there *has* been accuracy reduction in removing them. 
    - Additionally, the more words are on this list, the faster the program will run, however right now it is still pretty accurate. 
- Some text that should be sorted is slipping through the cracks. 
    - As of 29 June, 2023: Some things that should be matching and getting categorized are slipping through the cracks. This is a bug that I am actively working on, and should be fixed soon. 

### d. selectData.py 

**Major Functions** 
|Function| Return Value | notes | 
| --- | --- | --- | 
| select_db_names_to_sort(): | returns the dictionary of the multi-select options, a dict of the categorized_data, and a string representing the freetext category| This serves as the main function of this file  | 
| codebook_and_db_names() | returns the codebook in a dictionary format, and a list of all the database names that freetext data should be sorted into |  |
| sort_cats_auto(codebook, cats)| NA | "cats" is a shorter version of "categories
 -- will be true for all subsequent functions | 
| clean_cats(label) | returns a list of all the different spellings and classifications that one label of drug can have | | 

**Use Case** 

This program is used in preparation for the the 