#--------------Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

#--------------Import custom functions, objects
from Data import Dataset 
from dashboard_utils import create_obj, filter_quarters, return_objs
from plotting import display_plot

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
st.set_page_config(layout="wide", page_title='Healthy City',page_icon='src/logo.png')

#---------------Layout of the app
### Filtering
tops = st.sidebar.selectbox("Select challenge you are interested in:", topics)
objs_filtered = [d for d in data_objs if tops in d.topics]
data_display = st.sidebar.multiselect("Directly select datasets to display:", [d.name for d in objs_filtered])
objs_display = return_objs(data_display, objs_filtered)

### Dashboard introduction
if data_display!=[]:
    my_expander = st.expander("Dashboard introduction", expanded=False)
    with my_expander:
        st.markdown('**Welcome to the dashboard for the Healthy Brabantine City Deal Challenge!**')
        st.text('')
        st.markdown('This dashboard will guide you through the several datasets that are collected for you to use in your projects.\
        To help you get started, a short explanation about how to interact with the dashboard will follow.')
        st.text('') 
        st.markdown('On the left you can see\
        two menus, one to choose a challenge and another to choose datasets. You can select the challenge you want to look into by choosing\
        one of the three challenges in the top select menu. Now, in the lower select menu you can choose which datatsets belonging\
        to the chosen challenge you want to see. Each dataset contains an explanation, an option to download it as a csv to your computer\
        and the table showing what data is in it. Some of the datasets also have explanatory plots to help you understand better what the\
        data is about.')

else:
    st.image('src/banner.jpg', width=1100)
    st.markdown('**Welcome to the dashboard for the Healthy Brabantine City Deal Challenge!**')
    st.text('')
    st.markdown('This dashboard will guide you through the several datasets that are collected for you to use in your projects.\
    To help you get started, here is a short explanation on how to interact with the dashboard.')
    st.text('') 
    st.markdown('On the left you can see\
    two menus, one to choose a challenge and another to choose datasets. You can select the challenge you want to look into by choosing\
    one of the three challenges in the top select menu. Now, in the lower select menu you can choose which datatsets belonging\
    to the chosen challenge you want to see, and you can choose as many as you want to view at the same time. Each dataset contains an explanation, an option to download it as a csv to your computer\
    and the table showing what data is in it. Some of the datasets also have explanatory plots to help you understand better what the\
    data is about. You can use the interactive tools to change the graphics.')

###------------ Displaying data
for obj in objs_display:

    # Loop through each data object
    f = obj.filename
    obj.display()
    col1, col2, col3 = st.columns(3)
    
    display_plot(obj, [col1, col2, col3]) #displays interactive plots
        
    
