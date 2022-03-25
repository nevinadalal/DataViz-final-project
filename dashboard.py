from msilib.schema import File
import streamlit as st
import pandas as pd
import pickle
import altair as alt


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


def filter_dataset(
    df: pd.DataFrame,
    index: str,
    countries: list,
    year: int):
    filter_index = df.loc[df.Indicator == index,:]
    filter_country = filter_index[filter_index.Country.isin(countries)]
    filter_year = filter_country[filter_country.Year == year]
    return filter_year



def wage_gap(data, year, countries):
    
    data = filter_dataset(data, index = "EMP9_5", year = year, countries = countries)
    
    new = pd.DataFrame(countries, columns = ["country"])
    new["value"] = value+value_0
    new["y"] = y
    new["icon"] = [man_icon]*len(value)+[woman_icon]*len(value_0)

    icons = alt.Chart(new).mark_image(width = 50,height = 50).encode(
        x = 'value',
        y = 'y',
        url = 'icon'
    )

    lines = alt.Chart(new).mark_line(
        width = 50,
        height = 50
    ).encode(
        x = "value",
        y="y",
        color=alt.Color("country:N")
    )

    return(lines+icons)


if __name__ == '__main__':
    df = load_full_data()

    st.markdown('## Wage Gap')
    countries = st.multiselect("Select the countries you want to visualize: ", countries)
    year = st.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)

    graph = wage_gap(df, year, countries)
    st.altair_chart(graph)

