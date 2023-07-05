import fileReader 
import fileReaderCB 
import selectData
import sort_non_hf
import combine_hf.sort_hf
import combine_hf.combine_hf_data
import readToCSV


fileReader.get_dict() 
fileReaderCB.get_dict() 

selectData.select_db_names_to_sort() 
selectData.get_codebook()

combine_hf.sort_hf.sort_freetext_hf() 
sort_non_hf.run_sortFreeText()
combine_hf.combine_hf_data.create_updated_dict()

print(combine_hf.combine_hf_data.get_updated_dict())

readToCSV.set_updated_data(combine_hf.combine_hf_data.get_updated_dict())
readToCSV.write_csv_file()

