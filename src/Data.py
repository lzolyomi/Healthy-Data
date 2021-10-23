from typing import Tuple
import pandas as pd
import streamlit as st 


class Data:
    def __init__(self, filename, name, descr) -> None:
        self.filename = filename #filename WITHOUT .parquet extension
        self.name = name #Name to be displayed
        self.descr = descr #SHORT description of the data
        self.df = pd.read_parquet(f'src/data/{self.filename}.parquet')

    def download(self):
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
        ret_elements.append(self.download()) 
        ret_elements.append(
            st.dataframe(self.df)
        )
        
        return ret_elements

