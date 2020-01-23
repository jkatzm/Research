from data_manipulation import *

import pandas as pd
import pickle

########################################################################
# PNC (Philadelphia Neurodevelopmental Cohort) dataset
########################################################################
penn_phenotype_file = '/Users/jordankatz/Documents/GEMS_Lab/Local_Penn_Analysis/DATA/pnc_phenotype_scores_697.csv'
penn_timecourse_dir = '/Users/jordankatz/Documents/GEMS_Lab/Local_Penn_Analysis/DATA/TimeCourses/'
penn_matrix_dir = '/Users/jordankatz/Documents/GEMS_Lab/Local_Penn_Analysis/DATA/Matrices/'
penn_graph_dir = '/Users/jordankatz/Documents/GEMS_Lab/Local_Penn_Analysis/DATA/Graphs/'

########################################################################
# dataframe and basic info
########################################################################

penn_df = pd.read_csv(penn_phenotype_file).sort_values('Subject')
penn_df = penn_df.drop(labels='Unnamed: 0', axis=1)
subject_ids = np.array(sorted(penn_df['Subject']))
num_subjects = len(subject_ids) #697

########################################################################
# READ/WRITE helper functions
# Note: especially used for reading/writing subject distribution dictionaries
########################################################################
def save_obj(obj, name):
    """
    Input: python object 'obj' to store, a string 'name' for the object's name
    Note: assumes "DATA/" is in the current working directory
    """
    with open('DATA/Dictionaries/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    Input: a string 'name' for the object's name
    Output: the object in question
    Note: assumes "DATA/" is in the current working directory
    """
    with open('DATA/Dictionaries/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


