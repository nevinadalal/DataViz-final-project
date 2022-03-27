import streamlit as st
import pandas as pd
import altair as alt
from page2 import graphs2

#pictures

#countries available
countries = ['Austria',
 'Belgium',
 'Czech Republic',
 'Denmark',
 'France',
 'Germany',
 'Greece',
 'Hungary',
 'Iceland',
 'Ireland',
 'Italy',
 'Luxembourg',
 'Netherlands',
 'Norway',
 'Poland',
 'Portugal',
 'Slovak Republic',
 'Spain',
 'Sweden',
 'Switzerland',
 'United Kingdom',
 'Estonia',
 'Slovenia',
 'Latvia',
 'Lithuania']

@st.cache
def load_full_data():
    df = pd.read_csv("data.csv", index_col = 0)
    return df

if __name__ == '__main__':
    df = load_full_data()

    
    page = st.select_slider('Navigate across the pages',['Homepage', 'Page 1', 'Page 2'])
    
    if page == 'Homepage':
        st.markdown("## Visualization of Gender Equality in Europe \nTeam: PowerPuff Girl")
        st.image("https://www.ilprimatonazionale.it/wp-content/uploads/2019/06/gender-gap.jpg")
    
    if page =="Page 1":
        st.markdown("## Woman in Decision Making")

    if page == "Page 2":
        st.markdown('## Wage Gap and Parental Leave')
        countries = st.sidebar.multiselect("Select the countries you want to visualize: ", countries, default = ["France", "Greece","Italy", "Switzerland"])
        year = st.sidebar.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)

        graph = graphs2(df, countries, year)
        st.altair_chart(graph,use_container_width=True)

