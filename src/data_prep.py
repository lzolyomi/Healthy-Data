from typing import Dict
import pandas as pd 
import os


def convert_parquet(filename):
    """
    The path to csv file is opened and converted to a .parquet file
    then saved to the exact same directory, also returns the opened dataframe"""
    df = pd.read_csv(os.getcwd() + '/src/data/' + filename)
    filename_wo_extension = filename.split('.')[0]
    df.to_parquet(filename_wo_extension + '.parquet')
    return df

def check_inv_file():
    #checks if inventory file exists, if yes returns it as dataframe, if not creates and returns
    #Make sure to specify path like /data/ as it needs to go IN the data folder
    if os.path.exists(os.getcwd() + '/src/data_inventory.csv'):
        #check if data inventory file exists
        inv = pd.read_csv('src/data_inventory.csv')
    else:
        colnames = ['filename', 'name', 'description', 'health', 'water', 'living']
        inv = pd.DataFrame({element:[] for element in colnames})
        inv.to_csv('src/data_inventory.csv')
    return inv

def assess_file(file, existing_files):
    """
    Given an existing (!) file checks if already in inventory, 
    if not offers to add it
    file is filename
    data_inv is the opened csv file for inventory"""
    filename = file.split('.')[0] #stores filename without extension
    if file.split('.')[-1] == 'csv':
        if filename not in existing_files:
            confirm = input(f'Dataset {filename} not in inventory, want to add? y/n ')
            if confirm == 'y':
                df = convert_parquet(file) #### warning this can overwrite .parquet files in the directory
                details = {
                    'file':file,
                    'name':input('Name of dataset: '),
                    'description':input('Description of dataset '),
                    'health':input('Can it be used for health challenge? '),
                    'water':input('Can it be used for water challenge? '),
                    'living':input('Can it be used for living environment? ')
                    }
                return details



def update_datainv(path):
    """
    given a path to the DATA folder it checks for new csv files and 
    offers to update them, at the end it saves the updated inventory.csv file"""
    data_inv = check_inv_file()
    existing_filenames = list(data_inv['filename'].values) #filenames in inventory
    for file in os.listdir(os.getcwd() + path):
        abs_path = os.getcwd() + path + file
        if os.path.isfile(abs_path): #checks if its not a folder
            new_row = assess_file(file, existing_filenames)
            print(new_row)
            if type(new_row) == dict: #check if we actually want to add
                data_inv = data_inv.append(new_row, ignore_index=True)
    print(data_inv.shape)
    data_inv.to_csv('src/data_inventory.csv')
                


if __name__ == '__main__':
    update_datainv('/src/data/')
