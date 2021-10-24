#--------------Import libraries
import pandas as pd
import streamlit as st
import numpy as np
import os
from os import listdir
import platform

#--------------Import custom functions, objects
from Data import Dataset 
from dashboard_utils import create_obj, return_objs

#-------------Preparations for dashboard initiation

#data_objs = [f for f in listdir(path) if f.split('.')[-1] == 'parquet'] #only include parquet files
inventory = pd.read_csv('src/data_inventory.csv')
data_objs = []#list of Dataset objects from the inventory
for index, row in inventory.iterrows():
    create_obj(row, data_objs)

topics = ['Water', 'Health', 'Living environment']

#---------------Start Dashboard
st.set_page_config(layout="wide")

#---------------Layout of the app
### Filtering
tops = st.sidebar.selectbox("Select challenge you are interested in:", topics)
data_display = st.sidebar.multiselect("Directly select datasets to display:", [d.name for d in data_objs])

objs_display = return_objs(data_display, data_objs)

for obj in objs_display:
    obj.display() #call display method on each Data object created previously

if len(objs_display) < 1:
    if tops=='Water':
        st.markdown("This is the central page for the topic water. Blablablabla, update select menu to only show water datasets")

    if tops=='Health':
        st.markdown("This is the central page for the topic health. Blablablabla, update select menu to only show health datasets")

    if tops=='Living environment':
        st.markdown("This is the central page for the topic living environment. Blablablabla, update select menu to only show living environment datasets")