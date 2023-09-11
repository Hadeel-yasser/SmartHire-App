import sys
import pysolr



def index_documents(documents_filename, embedding_filename,core_name,cv_number):
        ## Solr configuration.
    SOLR_ADDRESS = 'http://localhost:8983/solr/'+ core_name
    # Create a client instance.
    solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)
    BATCH_SIZE = 100
    # Open the file containing text.
    with open(documents_filename, "r") as documents_file:
        # Open the file containing vectors.
        with open(embedding_filename, "r") as vectors_file:
            documents = []
            counter =0
            # For each document creates a JSON document including both text and related vector. 
            for index, (document, vector_string) in enumerate(zip(documents_file, vectors_file)):
                #print(counter)
                vector = [float(w) for w in vector_string.split(",")]
                doc = {
                    "id": cv_number+'_'+str(index),
                    "text": document,
                    "vector": vector
                }
                counter+=1
                # Append JSON document to a list.
                documents.append(doc)
                # To index batches of documents at a time.
                if index % BATCH_SIZE == 0 and index != 0:
                    # How you'd index data to Solr.
                    solr.add(documents)
                    documents = []
                    print("==== indexed {} documents ======"
                    .format(index))
        # To index the rest, when 'documents' list < BATCH_SIZE.
            if documents:
                solr.add(documents)     
            print("finished")

def index_extracted_documents(extracted_texts, embedding_filename, core_name):
    SOLR_ADDRESS = 'http://localhost:8983/solr/' + core_name
    solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

    BATCH_SIZE = 100
    documents = []

    # Open the file containing vectors.
    with open(embedding_filename, "r") as vectors_file:
        # For each extracted text and vector, create a JSON document.
        for index, (extracted_text, vector_string) in enumerate(zip(extracted_texts, vectors_file)):
            vector = [float(w) for w in vector_string.split(",")]
            doc = {
                "id": str(index),
                "text": extracted_text,
                "vector": vector
            }
            documents.append(doc)

            # To index batches of documents at a time.
            if index % BATCH_SIZE == 0 and index != 0:
                solr.add(documents)
                documents = []
                print("==== indexed {} documents ======".format(index))
    
    # To index the remaining documents when 'documents' list < BATCH_SIZE.
    if documents:
        solr.add(documents)
    print("Finished indexing")
