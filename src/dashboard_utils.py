from Data import Dataset 

"""This file contains extra assisting functions 
that help in the build of the dashboard"""

def create_obj(row, lst):
    """
    For a given row in the inventory dataframe, it creates a
    Dataset object and appends it to the lst passed as second argument"""
    lst.append(
        Dataset(
            row['filename'],
            row['name'],
            row['description'],
            bool(row['health']),
            bool(row['water']),
            bool(row['living']),
        )
    )