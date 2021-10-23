from typing import Tuple
import pandas as pd
import streamlit as st 


class Dataset:
    def __init__(self, filename, name, descr, health, water, living) -> None:
        self.filename = filename #filename WITHOUT .parquet extension
        self.name = name #Name to be displayed
        self.descr = descr #SHORT description of the data
        #Will hold True or False whether dataset can be used for given challenge
        self.health = health
        self.water = water
        self.living = living

    def open_file(self):
        self.df = pd.read_parquet(f'src/data/{self.filename}.parquet')

    def download(self): #returns a download button that contains the csv version of the dataframe
        """
        Returns a streamlit download button with the csv file attached
        NOTE only run after open_file, otherwise the dataframe is not there"""
        csv = self.df.to_csv().encode('utf-8')
        return st.download_button(
            label='Download csv',
            data = csv,
            file_name=f'{self.filename}.csv',
            mime='text/csv'
        )

    def display(self): #Displays the dataframe along with some description
        ret_elements = []
        ret_elements.append(st.markdown(f'## {self.name} \n #### {self.descr}'))
        self.open_file() #opens file as dataframe
        ret_elements.append(self.download()) 
        ret_elements.append(
            st.dataframe(self.df)
        )
        return ret_elements


    def __str__(self):
        return self.name