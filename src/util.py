import pickle
import os

def get_project_home_dir():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"

def save_to_file(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_from_file(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

DIR_PATH = get_project_home_dir()
