#--------------Import libraries
import pandas as pd
import streamlit as st
import numpy as np
import os
from os import listdir
import platform

#--------------Import custom functions, objects
from Data import Data 

#-------------Preparations for dashboard initiation
if platform.system() == 'Windows':  # checks for the system to get the paths right
    path = os.getcwd()+"\src\data"
else:
    path = os.getcwd()+"/src/data"

onlyfiles = [f for f in listdir(path) if f.split('.')[-1] == 'parquet'] #only include parquet files

topics = ['Water', 'Health', 'Living environment']
datasets = [i.split('.')[0] for i in onlyfiles]

#---------------Start Dashboard
st.set_page_config(layout="wide")

#---------------Layout of the app
### Filtering
tops = st.sidebar.selectbox("Select the topic you are interested in:", topics)
data_display = st.sidebar.multiselect("Directly select one of the datasets to look at:", datasets)

data_objs = [] #will store the data objects
for dataset in data_display:
    data_objs.append(Data(dataset, f'{dataset} this is name', 'This is the DESCRIPTION'))

for obj in data_objs:
    obj.display() #call display method on each Data object created previously

if tops=='Water':
    st.markdown("This is the central page for the topic water. Blablablabla, update select menu to only show water datasets")

if tops=='Health':
    st.markdown("This is the central page for the topic health. Blablablabla, update select menu to only show health datasets")

if tops=='Living environment':
    st.markdown("This is the central page for the topic living environment. Blablablabla, update select menu to only show living environment datasets")