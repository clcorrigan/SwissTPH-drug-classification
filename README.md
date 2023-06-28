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
              - As of 28 June 2023: These scripts ignore the health facility data. 
