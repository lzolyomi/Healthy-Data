#--------------Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

#--------------Import custom functions, objects
from Data import Dataset 
from dashboard_utils import create_obj, filter_quarters, return_objs

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

    ### here comes the plots for specific datasets
    if f == 'jobs_Brabant':
        y = col1.selectbox('Choose the sector you want to plot', obj.df.columns[2:])
        st.markdown('The plot shows the amount of jobs in the chosen sector per municipality')
        barfig = px.bar(obj.df, x='Municipality/Sector', y=y)
        barfig.update_traces(marker_color='#cb1337')
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
        barf.update_traces(marker_color='#cb1337')
        st.plotly_chart(barf, use_container_width=True)
    
    if f == 'renewable_electricity':
        wo_total = obj.df[obj.df['Source'] != 'Total']
        show_value = col1.selectbox('Choose column to show', obj.df.columns[4:])
        period2 = col2.select_slider('Select time period', obj.df['Periods'].unique())
        piefig2 = px.pie(wo_total[wo_total['Periods'] == period2], values=show_value, names='Source')
        st.plotly_chart(piefig2)
    
    if f == 'consumer_expenses':
        category = col1.selectbox('Select a category', obj.df['Category'].unique())
        df_filtered = obj.df[obj.df['Category'] == category]
        df_quarters = filter_quarters(df_filtered, 'Periods')
        barfig2 = px.bar(df_quarters, y='Change_baseline', x='Periods')
        barfig2.update_traces(marker_color='#cb1337')
        st.plotly_chart(barfig2, use_container_width=True)

    if f == 'municipality_data':
        feature = col1.selectbox('Select a feature', obj.df.columns[3:])
        municip = col2.multiselect('Select a municipality', obj.df['Name of municipality'].unique(), default=["'s-Hertogenbosch"])
        filtered = obj.df[obj.df['Name of municipality'].isin(municip)]
        fig4 = px.bar(filtered, x='year', y=feature, color='Name of municipality')
        fig4.update_traces(marker_color='#cb1337')
        st.plotly_chart(fig4,use_container_width=True)

    if f=='water_treatment':
        feat = col1.selectbox('Select a feature', obj.df.columns[4:])
        year = col2.select_slider('Choose the year', obj.df['Periods'].unique())
        filt = obj.df[(obj.df['Periods'] == year) & (obj.df['Regions'] != 'Nederland')] 
        barchart = px.bar(filt, y=feat, x='Regions')
        barchart.update_traces(marker_color='#cb1337')
        st.plotly_chart(barchart, use_container_width=True)

    if f=='bankruptcy':
        only_total = obj.df[obj.df['TypeOfBankruptcy'] == 'Total natural persons']
        sel_region = col1.selectbox('Select region', only_total['Regions'].unique())
        region_filter = only_total[only_total['Regions'] == sel_region]
        quarterly = filter_quarters(region_filter, 'Periods')
        fig5 = px.bar(quarterly, x='Periods', y='PronouncedBankrupcies_1')
        fig5.update_traces(marker_color='#cb1337')
        st.plotly_chart(fig5, use_container_width=True)

    if f=='student_debt':
        char = col1.selectbox('Select a characteristic', obj.df['Characteristic'].unique())
        feature2 = col2.selectbox('Select a feature', obj.df.columns[3:])
        filtered2 = obj.df[obj.df['Characteristic'] == char]
        fig6 = px.bar(filtered2, x='Period', y=feature2)
        fig6.update_traces(marker_color='#cb1337')
        st.plotly_chart(fig6, use_container_width=True)

    if f=='housing_stock':
        #NEED FIX for piechart
        feat2 = col1.selectbox('Choose a feature', obj.df.columns[3:])
        pie3 = px.pie(obj.df, names='municipalities_Brabant', values=feat2,title='Distribution of selected feature in municipalities')
        pie3.update_traces(textinfo='none')
        st.plotly_chart(pie3, use_container_width=True)

    if f=='land_usage':
        municip = col1.selectbox('Choose municipality', obj.df['municipalities_Brabant'])
        filt3 = obj.df[obj.df['municipalities_Brabant'] == municip]
        vals = list(filt3.values[0])[1:]
        cols = filt3.columns[1:]
        newdf = pd.DataFrame({'Value':vals, 'feature':cols})
        fig7 = px.pie(newdf, names='feature', values='Value')
        st.plotly_chart(fig7)
        
    
