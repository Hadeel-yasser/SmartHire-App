from flask import Flask, render_template, jsonify, request
from backend import create_core, embeddings, index_documents , extract_text , summarize_cvs, post_processing_cvs
from Post_solr import get_documents_in_folder
from flask_cors import CORS
from cv_data import CvData
import json


app = Flask(__name__)
cv_Data = CvData()
CORS(app)

@app.route('/return_core_name', methods=['POST'])
def return_core_name():
    data = request.json
    core_name = data.get('selectedValue')  
    create_core_view(core_name)
    return "Added  Core"


def create_core_view(selected_value):
    
    # Call your Python function with the selected_value
    result = create_core.create_cores(selected_value)
    folder_path = "E:\ITworx\CVs\Documents"+ "\\"+ result
    get_documents_in_folder(folder_path)
    print("Successfully index documents")


# step 0: check if we will add the function that will download the files to the corresponding dircetory based on core name or not.
# step 1: After importing documents call function get_documents_int_folder which will index documents to solr
# step 2: call function get top_ranked_cvs which will take the prompt entered in the search field + perecentage of cvs
# step 3: We need to populate the top applicants page by returning the candidate names
# step 4: call function that will get the matching cv chunks after clicking the button get relevant text
# route to get sentence embedding

# Define a route to render a template
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/acceptedresumes')
def acceptedresumes():
  return render_template('acceptedresumes.html')
@app.route('/candidates')
def candidates():
    return render_template('candidates.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/features')
def features():
    return render_template('features.html')
@app.route('/Login')
def Login():
    return render_template('Login.html')
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')
@app.route('/product')
def product():
    return render_template('product.html')
@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/startscreening')
def startscreening():
    return render_template('startscreening.html')
@app.route('/register')
def Register():
    return render_template('Register.html')


@app.route('/searchprompt', methods=['POST'])
def receive_input():
    
    data = request.get_json()
    searchQuery = data.get('searchQuery')
    core_name= data.get('selectedValue')
    
    percentage_of_cvs =float(data.get('percentageOfCvs'))

    print("Core Name: ", core_name, "Percentage: ", percentage_of_cvs , "Prompt: ", searchQuery)
    cv_name_id_dict, txt_file_path_dict , cv_sentences= post_processing_cvs.get_top_ranked_cvs(searchQuery, percentage_of_cvs ,core_name)
    
    # store the dictionaries for easier access later on
    cv_Data.set_cv_name_id_dict(cv_name_id_dict)
    cv_Data.set_txt_file_path_dict(txt_file_path_dict)
    cv_Data.set_cv_sentences_dict(cv_sentences)
    
   
    return cv_name_id_dict


@app.route('/get_button_ids_and_values', methods=['GET'])
def get_button_id():
    cv_name_id_dict = cv_Data.get_cv_name_id_dict()

    button_ids = list(cv_name_id_dict.keys())
    values = list(cv_name_id_dict.values())

    return jsonify(button_ids=button_ids, values=values)


# Function to handle view_summary action --> we can pass the dictionary for selected candidates and txt files dict to get to content
@app.route('/view_summary', methods=['POST'])
def view_summary():
    # Replace this with your actual code to handle view_summary
    data = request.get_json()
    candidateID= data.get('candidateId')
    txt_file_path_dict = cv_Data.get_txt_file_path_dict()
    summary = summarize_cvs.summarize_text(candidateID,txt_file_path_dict)
    return jsonify(summary=summary)
    #return summary

@app.route('/view_sentences', methods=['POST'])
def view_sentence(): # can pass dict for cv names and cv_chunks to get the matching sentences
    # Replace this with your actual code to handle view_sentence
    data = request.get_json()
    candidateID= data.get('candidateId')
    cv_sentences_dict = cv_Data.get_cv_sentences_dict()
    cv_matching_sentences= cv_sentences_dict[candidateID]
    print(cv_matching_sentences)
    #formatted_sentences = '\n'.join([str(sentence) for sentence in cv_matching_sentences])
    formatted_sentences = '\n'.join([sentence for inner_list in cv_matching_sentences for sentence in inner_list])

    return jsonify(formatted_sentences=formatted_sentences)

    
#<td>${candidate.resume_score}</td>
# prompt : select candidates that are experienced with python

if __name__ == '__main__':
    app.run(debug=True)
