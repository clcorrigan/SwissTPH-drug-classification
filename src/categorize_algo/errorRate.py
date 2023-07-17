import selectData
import fileReader 
import sortFreeText

global errorText; errorText = sortFreeText.no_catch

i = 0
for item in errorText:
    item = item.strip()
    i+=1
print(i)

