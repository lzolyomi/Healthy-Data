#--------------Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

#--------------Import custom functions, objects
from Data import Dataset 
from dashboard_utils import create_obj, return_objs

#-------------Preparations for dashboard initiation

#data_objs = [f for f in listdir(path) if f.split('.')[-1] == 'parquet'] #only include parquet files
inventory = pd.read_csv('src/data_inventory.csv')
data_objs = []#list of Dataset objects from the inventory
for index, row in inventory.iterrows():
    create_obj(row, data_objs)

for d in data_objs:
    d.return_topics()
topics = ['Water', 'Health', 'Living environment']

#---------------Start Dashboard
st.set_page_config(layout="wide")

#---------------Layout of the app
### Filtering
tops = st.sidebar.selectbox("Select challenge you are interested in:", topics)
objs_filtered = [d for d in data_objs if tops in d.topics]
data_display = st.sidebar.multiselect("Directly select datasets to display:", [d.name for d in objs_filtered])
objs_display = return_objs(data_display, objs_filtered)

###------------ Displaying data
for obj in objs_display:
    # Loop through each data object
    f = obj.filename
    obj.display()
    obj.display_plots()
    col1, col2, col3 = st.columns(3)
    if f == 'jobs_Brabant':
        y = col1.selectbox('Choose the sector you want to plot', obj.filename.columns[2:])
        barfig = px.bar(obj.df, x='Municipality/Sector', y=y)
        st.plotly_chart(barfig)
