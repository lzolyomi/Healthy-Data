#--------------Import libraries
import pandas as pd
import streamlit as st
import numpy as np
import os
from os import listdir
import platform

#-------------Preparations for dashboard initiation
if platform.system() == 'Windows':  # checks for the system to get the paths right
    path = os.getcwd()+"\src\data"
else:
    path = os.getcwd()+"/src/data"

onlyfiles = [f for f in listdir(path)]

topics = ['Water', 'Health', 'Living environment']
datasets = [i.split('.')[0] for i in onlyfiles]

#---------------Start Dashboard
st.set_page_config(layout="wide")

#---------------Layout of the app
tops = st.sidebar.selectbox("Select the topic you are interested in:", topics)
datasets = st.sidebar.selectbox("Directly select one of the datasets to look at:", datasets)