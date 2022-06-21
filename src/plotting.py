# --------------Import libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# --------------Import custom functions, Objects
from Data import Dataset
from dashboard_utils import filter_quarters


def display_plot(obj: Dataset, lst: list):
    """Stores a list of plots and interactive widgets
    that are dataset specific

    """
    f = obj.filename
    col1, col2, col3 = lst
    if f == "jobs_Brabant":
        y = col1.selectbox("Choose the sector you want to plot", obj.df.columns[2:])
        st.markdown(
            "The plot shows the amount of jobs in the chosen sector per municipality"
        )
        barfig = px.bar(obj.df, x="Municipality/Sector", y=y)
        barfig.update_traces(marker_color="#cb1337")
        st.plotly_chart(barfig, use_container_width=True)

    elif f == "youth_labour_participation":
        value = col1.selectbox(
            "Select which value you want to plot", obj.df.columns[5:]
        )
        period = col2.select_slider(
            "Select the time you want to look at ", obj.df["Period"].unique()
        )
        st.markdown(
            "The plot shows distribution of young workers distribution by age, according to the selected criteria"
        )
        piefig = px.pie(obj.df[obj.df["Period"] == period], names="Age", values=value)
        st.plotly_chart(piefig)

    elif f == "Brabant_health":
        y2 = col1.selectbox(
            "Select which health characteristic you want to look at", obj.df.columns[1:]
        )
        st.markdown(
            "The plot shows the percentage of people falling in the chosen characteristic per municipality"
        )
        barf = px.bar(obj.df, x="Municipalities (2021)", y=y2)
        barf.update_traces(marker_color="#cb1337")
        st.plotly_chart(barf, use_container_width=True)

    elif f == "renewable_electricity":
        wo_total = obj.df[obj.df["Source"] != "Total"]
        show_value = col1.selectbox("Choose column to show", obj.df.columns[4:])
        period2 = col2.select_slider("Select time period", obj.df["Periods"].unique())
        piefig2 = px.pie(
            wo_total[wo_total["Periods"] == period2], values=show_value, names="Source"
        )
        st.plotly_chart(piefig2)

    elif f == "consumer_expenses":
        category = col1.selectbox("Select a category", obj.df["Category"].unique())
        df_filtered = obj.df[obj.df["Category"] == category]
        df_quarters = filter_quarters(df_filtered, "Periods")
        barfig2 = px.bar(df_quarters, y="Change_baseline", x="Periods")
        barfig2.update_traces(marker_color="#cb1337")
        st.plotly_chart(barfig2, use_container_width=True)

    elif f == "municipality_data":
        feature = col1.selectbox("Select a feature", obj.df.columns[3:])
        municip = col2.multiselect(
            "Select a municipality",
            obj.df["Name of municipality"].unique(),
            default=["'s-Hertogenbosch"],
        )
        filtered = obj.df[obj.df["Name of municipality"].isin(municip)]
        fig4 = px.bar(filtered, x="year", y=feature, color="Name of municipality")
        fig4.update_traces(marker_color="#cb1337")
        st.plotly_chart(fig4, use_container_width=True)

    elif f == "water_treatment":
        feat = col1.selectbox("Select a feature", obj.df.columns[4:])
        year = col2.select_slider("Choose the year", obj.df["Periods"].unique())
        filt = obj.df[(obj.df["Periods"] == year) & (obj.df["Regions"] != "Nederland")]
        barchart = px.bar(filt, y=feat, x="Regions")
        barchart.update_traces(marker_color="#cb1337")
        st.plotly_chart(barchart, use_container_width=True)

    elif f == "bankruptcy":
        only_total = obj.df[obj.df["TypeOfBankruptcy"] == "Total natural persons"]
        sel_region = col1.selectbox("Select region", only_total["Regions"].unique())
        region_filter = only_total[only_total["Regions"] == sel_region]
        quarterly = filter_quarters(region_filter, "Periods")
        fig5 = px.bar(quarterly, x="Periods", y="PronouncedBankrupcies_1")
        fig5.update_traces(marker_color="#cb1337")
        st.plotly_chart(fig5, use_container_width=True)

    elif f == "student_debt":
        char = col1.selectbox(
            "Select a characteristic", obj.df["Characteristic"].unique()
        )
        feature2 = col2.selectbox("Select a feature", obj.df.columns[3:])
        filtered2 = obj.df[obj.df["Characteristic"] == char]
        fig6 = px.bar(filtered2, x="Period", y=feature2)
        fig6.update_traces(marker_color="#cb1337")
        st.plotly_chart(fig6, use_container_width=True)

    elif f == "housing_stock":
        # NEED FIX for piechart
        feat2 = col1.selectbox("Choose a feature", obj.df.columns[3:])
        pie3 = px.pie(
            obj.df,
            names="municipalities_Brabant",
            values=feat2,
            title="Distribution of selected feature in municipalities",
        )
        pie3.update_traces(textinfo="none")
        st.plotly_chart(pie3, use_container_width=True)

    elif f == "land_usage":
        municip = col1.selectbox(
            "Choose municipality", obj.df["municipalities_Brabant"]
        )
        filt3 = obj.df[obj.df["municipalities_Brabant"] == municip]
        vals = list(filt3.values[0])[1:]
        cols = filt3.columns[1:]
        newdf = pd.DataFrame({"Value": vals, "feature": cols})
        fig7 = px.pie(newdf, names="feature", values="Value")
        st.plotly_chart(fig7)

    else:
        col1.markdown("This dataset has no plot available currently")
