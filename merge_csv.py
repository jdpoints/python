#!/usr/bin/env python
import csv
import copy
import argparse

def main():
    
def csv_to_dict(in_csv):
    """
    opens a csv file and returns a list of dicts
    
    in_csv file in csv format to be converted
    """
    out_list = []
    
    with open(in_csv, 'rb') as f:
        reader = csv.reader(f)
        
        #get the header row of the csv
        header = csv.next()
        
        #iterate through reader (csv as object)
        for row in reader:
            temp_dict = {}
            
            #map items to dictionary
            for i,item in enumerate(row):
                temp_dict[header[i]] = item
            
            #add dictionary to list
            temp_dict['Merged'] = False
            out_list.append(temp_dict)
    
    #return list of dictionary items
    return out_list

def csv_merge(list_1, list_2, merge_on_list):
	"""
	search list_2
    
    list_1  list to iterate through
    list_2  list to search for matches
    merge_on_list list containing keys to determine merge
	"""
    out_list = []
    
    for i in list_1:
        for j in list_2:
            for item in merge_on_list:
                if i[item].upper() == j[item].upper():
                    out_list.append(row_merge(i, j))
                    break #end item loop when match found
            else: 
                continue #goto next j in list_2 if match not found
            break #ends list_2 loop when merge_on_list match found
        else: 
            out_list.append(null_merge(i, list_2[0]))
        break
        
    #add unmerged items from list_2 to out_list
    for i in list_2:
        if i["Merged"] == True:
            continue #goto next loop if Merged
        else:
            out_list.append(null_merge(i, list_1[0]))
    
    return out_list

def dict_merge(dict_1, dict_2):
    """
    copy dict_1 and add unique data from dict_2 and return copy
    
    dict_1   dict to copy
    dict_2   dict to add to row_1
    """
    out_dict = copy.deepcopy(dict_1)
    
    for key,val in dict_2.items():
        #ignore "Merged" key
        if key == "Merged":
            continue
        elif key in out_dict:
            #if same skip otherwise combine into single entry
            if out_dict[key].upper() == val.upper():
                continue
            else:
                #use ; as a separator
                out_dict[key] = ";".join([out_dict[key],val])
        else:
            out_dict[key] = val
    
    #set "Merged" flags to True
    dict_1["Merged"] = True
    dict_2["Merged"] = True
    
    return out_dict
    
def null_merge(dict_1, dict_2):
    """
    add key/value pairs to a copy of dict_1 so that all keys are in one dict
    
    dict_1 dict to add values to
    dict_2 dict to copy keys from
    """
    out_dict = copy.deepcopy(dict_1)
    
    for key,val in dict_2.items():
        #ignore keys already in dict_1
        if key in out_dict:
            break
        else:
            #add None if key doesn't exist
            out_dict[key] = None    
    
    return out_dict
                
if __name__ == "__main__":
    main()