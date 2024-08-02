import sys
import os
import gzip
import pickle

# Add the directory containing 'logic.py' to the Python path
sys.path.append('C:/Users/nguye/OneDrive/Desktop/Lab02_logic/Lab02_logic')

def load_pklz_file(filepath):
    with gzip.open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data

def print_pklz_contents(filepath):
    data = load_pklz_file(filepath)
    
    # Printing data, you might need to format it better depending on the structure
    if isinstance(data, dict):
        for key, value in data.items():
            print(f'{key}: {value}')
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(f'Item {index}: {item}')
    else:
        print(data)

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.pklz'):
            filepath = os.path.join(directory_path, filename)
            print(f'Contents of {filename}:')
            print_pklz_contents(filepath)
            print('\n' + '-'*40 + '\n')

# Provide the path to the directory containing your .pklz files
directory_path = 'C:/Users/nguye/OneDrive/Desktop/Lab02_logic/Lab02_logic/models/models'

# Process all .pklz files in the directory
process_directory(directory_path)
