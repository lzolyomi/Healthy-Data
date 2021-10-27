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
st.set_page_config(layout="wide", page_title='Healthy City',page_icon='src/logo.png')

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
    col1, col2, col3 = st.columns(3)
    ### here comes the plots for specific datasets
    if f == 'jobs_Brabant':
        y = col1.selectbox('Choose the sector you want to plot', obj.df.columns[2:])
        st.markdown('The plot shows the amount of jobs in the chosen sector per municipality')
        barfig = px.bar(obj.df, x='Municipality/Sector', y=y)
        st.plotly_chart(barfig, use_container_width=True)

    if f == 'youth_labour_participation':
        value = col1.selectbox('Select which value you want to plot', obj.df.columns[5:])
        period = col2.select_slider("Select the time you want to look at ", obj.df['Period'].unique())
        st.markdown('The plot shows distribution of young workers distribution by age, according to the selected criteria')
        piefig = px.pie(obj.df[obj.df['Period']==period], names='Age', values=value)
        st.plotly_chart(piefig)

    if f == 'Brabant_health':
        y2 = col1.selectbox('Select which health characteristic you want to look at', obj.df.columns[1:])
        st.markdown('The plot shows the percentage of people falling in the chosen characteristic per municipality')
        barf = px.bar(obj.df, x='Municipalities (2021)', y=y2)
        st.plotly_chart(barf, use_container_width=True)
    
    if f == 'renewable_electricity':
        wo_total = obj.df[obj.df['Source'] != 'Total']
        show_value = col1.selectbox('Choose column to show', obj.df.columns[4:])
        period2 = col2.select_slider('Select time period', obj.df['Periods'].unique())
        piefig2 = px.pie(wo_total[wo_total['Periods'] == period2], values=show_value, names='Source')
        st.plotly_chart(piefig2)