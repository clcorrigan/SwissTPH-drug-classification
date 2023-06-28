# SwissTPH-drug-classification
A set of programs that are used to help automatically sort drug names that have been inserted as freetext rather than selected from a drop down menu


## Table of Contents 
1. Overview Explaination of Code 
2. Codebook and Data Requirements
3. Files Funcionality 
    - errorRate.py
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
As of 28 June, 2023, this proved significantly effective: 
    On 500 randomly selected patients: 
        Before the running on the program, the freetext category was accounted for correctly 82.4% of the time 
        After running the program, the freetext category was accounted for correctly 95.8% of the time. 
        - There were 67 instances of the program correctly sorting freetext (going from incorrect to correct)
        - There were 0 instances of the program incorrectly sorting freetext (going from correct to incorrect)
        - There were 21 missed instances of sorting freetext (going from incorrect to incorrect)

