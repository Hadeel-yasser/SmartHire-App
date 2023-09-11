import pdfplumber
import re
import spacy
import nltk

# Load the spaCy model for NER (Named Entity Recognition)
nlp = spacy.load("en_core_web_sm")


# function to extract text from pdf and save them in a list of strings
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_lines = []
        for page in pdf.pages:
            text = page.extract_text()
            # Append each line of text as a separate element in a list
            text_lines += text.split('\n')
            
    return text_lines


def preprocess_text_modified(text_lines):
    # Join the list of text lines into a single string
    text = ' '.join(text_lines)
    
    # Remove non-alphanumeric characters and extra whitespaces
    # except characters used in emails, GPAs, "high-fin", and website links
    pattern = r'[^\w\s@.#+-]|(?<=\d)\s+(?=\d)|(?<=high-fin)\W|(?<=[\w\s])[-]'
    
    # Apply the regular expression pattern to the text
    text = re.sub(pattern, ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespaces and line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Use spaCy to split the preprocessed text into sentences
    doc = nlp(text)
    preprocessed_text_lines = [sent.text for sent in doc.sents]
    return preprocessed_text_lines


# Load the spaCy model for NER (Named Entity Recognition)
nlp = spacy.load("en_core_web_sm")

# Download the "names" dataset from nltk
#nltk.download("names")

# Get a set of common English words from nltk
common_words_set = set(nltk.corpus.names.words())

def preprocess_text_and_extract_name(text_lines):
    # Join all text lines into a single string
    text = ' '.join(text_lines)

    # Remove non-alphanumeric characters and extra whitespaces
    # except characters used in emails, GPAs, "high-fin", and website links
    pattern = r'[^\w\s@.#+-]|(?<=\d)\s+(?=\d)|(?<=high-fin)\W|(?<=[\w\s])[-]'

    # Apply the regular expression pattern to the entire text
    text = re.sub(pattern, ' ', text)

    # Convert to lowercase
    text = text.lower().strip()

    # Extract the candidate's name from the first line
    first_line = text_lines[0] if text_lines else ""
    first_line = re.sub(pattern, ' ', first_line)  # Apply preprocessing to the first line
    first_line = first_line.lower().strip()
    first_line_words = [token.text for token in nlp(first_line)]
    candidate_name = None
    if not any(word.lower() in common_words_set for word in first_line_words):
        candidate_name = first_line

    # If spaCy's NER didn't find a name in the first line, try custom logic based on capitalization
    if not candidate_name:
        # Search for capitalized words in the original first line
        potential_names = re.findall(r'\b[A-Z][a-zA-Z]*\b', first_line)
        # Check if there are potential names and filter out common words
        potential_names = [name for name in potential_names if name.lower() not in common_words_set]
        if potential_names:
            # Assuming the first name is the first capitalized word and the last name is the last capitalized word
            first_name = potential_names[0]
            last_name = potential_names[-1]
            candidate_name = f"{first_name} {last_name}"

    # Use spaCy to split the preprocessed text into sentences
    doc = nlp(text)
    preprocessed_text_lines = [sent.text for sent in doc.sents]

    return preprocessed_text_lines, candidate_name


