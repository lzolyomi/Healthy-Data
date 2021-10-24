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

def return_objs(lst, objs):
    """
    Given a list of attributes, the type of the attribute and 
    another list with Dataset objects, it returns a list containing
    all objects that has a matching attribute name with the first 
    argument's list"""
    found_objects = []
    for elem in lst:
        for obj in objs:
            if elem == obj.name:
                found_objects.append(obj)

    return found_objects