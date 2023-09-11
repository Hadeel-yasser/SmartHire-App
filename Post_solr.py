from urllib.request import urlopen
from backend.embeddings import batch_encode_to_vectors
from backend.index_documents import index_documents, index_extracted_documents
from backend.extract_text import extract_text_from_pdf, preprocess_text_and_extract_name
import os
import csv
import pysolr
import requests
import json
cv_name_and_id_dict={}
txt_file_path_dict={}

def get_documents_in_folder(folder_path):

    #folder_path = 'E:\ITworx\CVs\Documents'  # replace with the path to your folder...
    file_list = os.listdir(folder_path)
    
    cv_name = 'CV'
    counter =0
    
    for file_name in file_list:
        
        if file_name.endswith('.pdf'):  # replace '.txt' with the file extension you want to read
            counter+=1
            cv_name += str(counter)
            
            file_path = os.path.join(folder_path, file_name)
            
            core_name= os.path.basename(folder_path)
            core_name_no_extenstion= os.path.splitext(core_name)[0]

            basename = os.path.basename(file_name)
            name_without_extension = os.path.splitext(basename)[0]

            name_for_csv = name_without_extension +'.csv'

            csv_file_path= create_csv(core_name_no_extenstion,name_for_csv)

            # extract the text from pdf
            extracted_text= extract_text_from_pdf(file_path)
            # remove extra spaces and preprocess the extracted text
            prepocessed_text,name = preprocess_text_and_extract_name(extracted_text)
            cv_name_and_id_dict[cv_name]= name
            # create text file to store the extracted text
            name_for_text = name_without_extension + '.txt'
            txt_file_path=save_text_to_file(prepocessed_text,name_for_text,folder_path) # pass the text, name for the text file, and the folder path of the to be created file
            txt_file_path_dict[cv_name]=txt_file_path
            # call def batch_encode_to_vectors
            
            batch_encode_to_vectors(txt_file_path,csv_file_path)
            print("Encoded documents")
            # index the extracted text to solr
            index_documents(txt_file_path,csv_file_path,core_name,cv_name)
            cv_name = 'CV'
    return "Successfully indexed documents"

def get_cvs_names_in_folder(folder_path):
    #folder_path = 'E:\ITworx\CVs\Documents'  # replace with the path to your folder...
    file_list = os.listdir(folder_path)
    
    cv_name = 'CV'
    counter =0
    
    for file_name in file_list:
        
        if file_name.endswith('.pdf'):  # replace '.txt' with the file extension you want to read
            counter+=1
            cv_name += str(counter)
            
            file_path = os.path.join(folder_path, file_name)
            
            #core_name= os.path.basename(folder_path)
            #core_name_no_extenstion= os.path.splitext(core_name)[0]

            basename = os.path.basename(file_name)
            name_without_extension = os.path.splitext(basename)[0]

            # extract the text from pdf
            extracted_text= extract_text_from_pdf(file_path)
            # remove extra spaces and preprocess the extracted text
            prepocessed_text,name = preprocess_text_and_extract_name(extracted_text)
            cv_name_and_id_dict[cv_name]= name
            
            # create text file to store the extracted text
            name_for_text = name_without_extension + '.txt'
            txt_file_path = os.path.join(folder_path, name_for_text)
            #txt_file_path=save_text_to_file(prepocessed_text,name_for_text,folder_path) # pass the text, name for the text file, and the folder path of the to be created file
            txt_file_path_dict[cv_name]=txt_file_path
            
            cv_name = 'CV'
    return cv_name_and_id_dict, txt_file_path_dict
    
def save_text_to_file(text_lines, output_filename, directory):
    file_path = os.path.join(directory, output_filename)
    with open(file_path, "w", encoding="utf-8") as file:
        for line in text_lines:
            # Write each line of text as a separate line in the file
            file.write(line + '\n')
    return file_path


def create_csv(core_name,file_name):
    directory = 'E:\ITworx\CVs\Documents'+"\\" + core_name
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, file_name)

    with open(os.path.join(directory, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])  
    return filepath  
   

def get_total_document_count(core_name):
    solr_url = f"http://localhost:8983/solr/{core_name}/select?q=*:*&rows=0"
    response = requests.get(solr_url)
    
    if response.status_code == 200:
        result = response.json()
        total_documents = result.get('response', {}).get('numFound', 0)
        return total_documents
    else:
        print(f"Solr request failed with status code: {response.status_code}")
        return None
    
if __name__ == "__main__":
    pass
    # replace with the file directory for the generated core
    #get_documents_in_folder('E:\ITworx\CVs\Documents\software_engineer')   