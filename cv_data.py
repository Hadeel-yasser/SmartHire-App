# cvdata.py (Separate file)

class CvData:
    def __init__(self):
        self.cv_name_id_dict = {}
        self.txt_file_path_dict = {}
        self.cv_sentences_dict = {}
    def set_cv_name_id_dict(self, cv_name_id_dict):
        self.cv_name_id_dict = cv_name_id_dict

    def set_txt_file_path_dict(self, txt_file_path_dict):
        self.txt_file_path_dict = txt_file_path_dict

    def set_cv_sentences_dict(self, cv_chunks):
        self.cv_sentences_dict = cv_chunks

    def get_cv_name_id_dict(self):
        return self.cv_name_id_dict

    def get_txt_file_path_dict(self):
        return self.txt_file_path_dict
    
    def get_cv_sentences_dict(self):
        return self.cv_sentences_dict
