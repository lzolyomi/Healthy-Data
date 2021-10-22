import pandas as pd 
import os

def convert_parquet(csv_path):
    """
    The path to csv file is opened and converted to a .parquet file
    then saved to the exact same directory, also returns the opened dataframe"""
    df = pd.read_csv(csv_path)
    filename_wo_extension = csv_path.split('.')[0]
    df.to_parquet(filename_wo_extension + '.parquet')
    return df


def convert_all(path):
    """
    converts all csv files to a parquet file in the directory passed by the argument
    ATTENTION path should be defined only relative to current working directory
    It can be checked by running os.getcwd() as the function adds this to path"""
    nr_converted = 0
    for file in os.listdir(os.getcwd() + path):
        abs_path = os.getcwd() + path + '/' + file
        if os.path.isfile(abs_path): #checks if its not a folder
            if file.split('.')[-1] == 'csv': #checks if csv
                nr_converted+=1
                df = convert_parquet(abs_path) #### warning this can overwrite .parquet files in the directory
    print(f"### CONVERSION DONE, {nr_converted} files have been converted")
    

if __name__ == '__main__':
    convert_all('/src/data')