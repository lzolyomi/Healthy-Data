from typing import Dict
import pandas as pd
import os

challenge_categories = ["health", "water", "living"]  # NOTE: not in use yet


def convert_parquet(filename):
    """
    The path to csv file is opened and converted to a .parquet file
    then saved to the exact same directory, also returns the opened dataframe"""
    df = pd.read_csv(os.getcwd() + "/src/data/" + filename)
    filename_wo_extension = filename.split(".")[0]
    df.to_parquet("src/data/" + filename_wo_extension + ".parquet")
    return df


def check_inv_file():
    # checks if inventory file exists, if yes returns it as dataframe, if not creates and returns
    # Make sure to specify path like /data/ as it needs to go IN the data folder
    if os.path.exists(os.getcwd() + "/src/data_inventory.csv"):
        # check if data inventory file exists
        inv = pd.read_csv("src/data_inventory.csv")
    else:
        colnames = ["filename", "name", "description", "health", "water", "living"]
        inv = pd.DataFrame({element: [] for element in colnames})
        inv.to_csv("src/data_inventory.csv", index=False)
    return inv


def assess_file(file, existing_files):
    """
    Given an existing (!) file checks if already in inventory,
    if not offers to add it
    file is filename
    data_inv is the opened csv file for inventory"""
    filename = file.split(".")[0]  # stores file name without extension
    if file.split(".")[-1] == "csv":
        if filename not in existing_files:
            confirm = input(
                f">> Dataset {filename} not in inventory, want to add? y/n "
            )
            if confirm == "y":
                df = convert_parquet(
                    file
                )  #### warning this can overwrite .parquet files in the directory
                print(file)
                details = {
                    "filename": filename,
                    "name": input(">>>> Name of dataset: "),
                    "description": input(">>>> Description of dataset "),
                    "health": input(">>>> Can it be used for health challenge? 1/0 "),
                    "water": input(">>>> Can it be used for water challenge? 1/0 "),
                    "living": input(">>>> Can it be used for living environment? 1/0 "),
                }
                return details


def delete_datasets(filename):
    """
    Deletes inventory entry for a dataset with given filename"""
    inv = pd.read_csv("src/data_inventory.csv")
    inv.set_index("filename", inplace=True)
    inv.drop(filename, inplace=True)
    inv.to_csv("src/data_inventory.csv", index=False)


def update_datainv(path):
    """
    given a path to the DATA folder it checks for new csv files and
    offers to update them, at the end it saves the updated inventory.csv file"""
    data_inv = check_inv_file()
    existing_filenames = list(data_inv["filename"].values)  # filenames in inventory
    for file in os.listdir(os.getcwd() + path):
        abs_path = os.getcwd() + path + file
        if os.path.isfile(abs_path):  # checks if its not a folder
            new_row = assess_file(file, existing_filenames)
            if type(new_row) == dict:  # check if we actually want to add
                data_inv = data_inv.append(new_row, ignore_index=True)
    data_inv.to_csv("src/data_inventory.csv", index=False)


if __name__ == "__main__":
    function = input("// You want to add data? (y/n)? ")
    if function == "y":
        update_datainv("/src/data/")
    else:
        still_delete = True
        while still_delete:
            ans = input("Give filename to delete from inventory, or n to exit>> ")
            if ans == "n":
                break
            else:
                delete_datasets(ans)
