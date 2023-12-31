from query_solr import query_user_prompt, get_cv_chunks, get_cv_scores
import requests
import math
import pysolr
from Post_solr import get_cvs_names_in_folder

# function to get the top ranked cvs based on the calculated total score ...

def get_top_ranked_cvs(prompt,percentage_of_cvs,core_name):
    search_result=query_user_prompt(prompt)

    cv_scores=get_cv_scores(search_result)

    cv_chunks=get_cv_chunks(search_result)
    sorted_items = sorted(cv_scores.items(), key=lambda item: item[1], reverse=True)
    
    num_items = len(sorted_items)
    num_selected = int(num_items * percentage_of_cvs)
    top_items = sorted_items[:num_selected]
    
    top_keys = [item[0] for item in top_items]
    keep_only_selected_keys(cv_chunks,top_keys)
    
    folder_path = "E:\ITworx\CVs\Documents\\" + core_name
    cv_name_and_id_dict , txt_file_path_dict= get_cvs_names_in_folder(folder_path)
    keep_only_selected_keys(txt_file_path_dict,top_keys) # to pass the text file to the openAI function
    keep_only_selected_keys(cv_name_and_id_dict,top_keys) # to retrieve candidates names
    
    return cv_name_and_id_dict, txt_file_path_dict , cv_chunks


def keep_only_selected_keys(dictionary, keys_to_keep_order):
    # Sort the input dictionary based on the order of keys in keys_to_keep_order
    sorted_dict = {key: dictionary[key] for key in keys_to_keep_order if key in dictionary}

    # Update the input dictionary with the sorted_dict
    dictionary.clear()
    dictionary.update(sorted_dict)
