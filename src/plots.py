import plotly.express as px
import streamlit as st

################################## DEPRECATED #################################


def get_plots(data):
    f = data.filename
    if f == "jobs_Brabant":
        plot_lst = [
            st.selectbox("Select variable to plot", data.df.columns[2:]),
            st.plotly_chart(
                px.bar(data.df, x="Municipality/Sector", y="Industry - Fulltime")
            ),
        ]
    elif f == "vacancies_brabant":
        plot_lst = [
            px.bar(data.df, x="Period/Sector-region - ", y="Total - West-Brabant")
        ]
    else:
        plot_lst = []

    return plot_lst
