import requests
import json
from Post_solr import get_total_document_count
from backend.embeddings import get_sentence_embedding
import re
from collections import Counter


def calculate_k(total_chunks, desired_coverage=0.5):
    """
    Calculate the value of k dynamically based on the total number of chunks in the Solr database.
    
    Args:
        total_chunks (int): The total number of chunks in the Solr database.
        desired_coverage (float): The desired coverage of results.

    Returns:
        int: The dynamically calculated value of k.
    """
    # You can define your equation or criteria here to calculate k based on total_chunks and desired_coverage.
    # k = int(total_chunks * desired_coverage)
    k = int(total_chunks * desired_coverage)
    return k

def search_with_sentence_embedding(embedding_vector,core_name, total_chunks): # takes as input the total amount of documents
    
    solr_url = "http://localhost:8983/solr/" + core_name 
    if len(embedding_vector) != 384:
        print(f"Error: The provided vector has dimension {len(embedding_vector)}, but {384} is expected.")
        return None
    k = calculate_k(total_chunks)
    print("K chunks =" + str(k))
    solr_query = {
        "query": f"{{!knn f=vector topK={k}}}[{', '.join(map(str, embedding_vector))}]", 
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{solr_url}/select?fl=id,text,score&rows=1000", data=json.dumps(solr_query), headers=headers)
    

    if response.status_code == 200:
        results = response.json()
        
        num_documents_returned = len(results.get("response", {}).get("docs", []))

        if num_documents_returned != k:
            print(f"Warning: Expected {k} documents, but only received {num_documents_returned} documents.")
    
        return results
    else:
        print(f"Solr request failed with status code: {response.status_code}")
        print(response.text)
        return None


def query_user_prompt(prompt):

    sentence_vector=get_sentence_embedding(prompt)
    
    # call method to get total amount of documents
    # the function should take as input also core_name
    total_document_count = get_total_document_count(core_name= 'software_engineer')
    search_results = search_with_sentence_embedding(sentence_vector,'software_engineer',total_document_count)

    return search_results

def get_cv_scores(search_results):
    
    if search_results:
        cv_scores ={}
       
        for doc in search_results['response']['docs']:
            output_string = re.sub(r'_.*', '', doc['id']) # CV1
            
            if output_string in cv_scores:
                cv_scores[output_string] += doc['score']
            else: 
                cv_scores[output_string]= doc['score']
    return cv_scores

def get_cv_chunks(search_results):
    if search_results:
        
        cv_chunks={}
        for doc in search_results['response']['docs']:
            output_string = re.sub(r'_.*', '', doc['id']) # CV1
            
            if output_string in cv_chunks:
                cv_chunks[output_string].append(doc['text'])
            else: 
                cv_chunks[output_string] =[]
                cv_chunks[output_string].append(doc['text'])
    return cv_chunks


    
        
    
    
        
