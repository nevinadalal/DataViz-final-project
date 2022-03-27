import streamlit as st
import pandas as pd
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
    year=None):
    filter_index = df.loc[df.Indicator == index,:]
    filter_country = filter_index[filter_index.Country.isin(countries)]
    if year !=None:
        filter_year = filter_country[filter_country.Year == year]
        return filter_year
    else:
        return filter_country



def wage_gap(data, countries):
    
    source = filter_dataset(data, index = "EMP9_5", countries = countries)
    
    #Selection that choosed the nearest point & selects based on x-value
    #nearest = alt.selection(type = 'single', nearest = True, on = 'mouseover', fields = ['Year'], empty = 'none')
    click = alt.selection_multi(fields=['Country'], bind = 'legend')

    #simple line chart
    line_chart = alt.Chart(source).mark_line(point=True).encode(
        x = alt.X("Year:O",title ="Year"),
        y = alt.Y("Value:Q",title = "Index"),
        color = alt.Color("Country:N", scale = alt.Scale(scheme = 'category20b')),
        opacity = alt.condition(click, alt.value(1), alt.value(0.2))   
    ).add_selection(
        click
    ).properties(
        width=600,
        height=300
    ).interactive()
    return line_chart


if __name__ == '__main__':
    df = load_full_data()

    st.markdown('## Wage Gap')
    countries = st.sidebar.multiselect("Select the countries you want to visualize: ", countries, default = ["France", "Greece","Italy", "Switzerland"])
    year = st.sidebar.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)

    graph = wage_gap(df, countries)
    st.altair_chart(graph,use_container_width=True)

