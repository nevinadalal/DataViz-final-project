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



def graphs2(data, countries, year):
    
    source = filter_dataset(data, index = "EMP9_5", countries = countries)
    
    #Selection that choosed the nearest point & selects based on x-value
    #nearest = alt.selection(type = 'single', nearest = True, on = 'mouseover', fields = ['Year'], empty = 'none')
    click = alt.selection_multi(fields=['Country'], bind = 'legend')

    #simple line chart
    line_chart = alt.Chart(source).mark_line(point=True).encode(
        x = alt.X("Year:O",title ="Year"),
        y = alt.Y("Value:Q",title = "Index"),
        color = alt.Color("Country:N"),
        tooltip=['Year', 'Country', 'Value'],
        opacity = alt.condition(click, alt.value(1), alt.value(0.2))   
    ).add_selection(
        click
    ).properties(
        width=600,
        height=300
    )

    #maternal leave
    maternal_leave = filter_dataset(data, index = "EMP18_MAT", countries = countries, year = year)
    maternal_leave["icon"]="data:image/png;base64,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"


    #paternal leave
    paternal_leave = filter_dataset(data, index = "EMP18_PAT", countries = countries, year = year)
    paternal_leave["icon"]="data:image/png;base64,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"

    bars1 = alt.Chart(maternal_leave).mark_bar().encode(
    y='Country:N',
    x='Value:Q',
    color=alt.Color("Country:N"),
    opacity = alt.condition(click, alt.value(1), alt.value(0.2)) 
    ).properties(
        width=250,
        height=250
    )

    icons1 = alt.Chart(maternal_leave).mark_image(
        width = 60,
        height = 60
    ).encode(
        y='Country:N',
        x='Value:Q',
        url = 'icon',
        opacity = alt.condition(click, alt.value(1), alt.value(0.2)) 
    ).properties(
        width=250,
        height=250
    )

    maternal = bars1 + icons1

    bars2 = alt.Chart(paternal_leave).mark_bar().encode(
        y='Country:N',
        x='Value:Q',
        color=alt.Color("Country:N"),
        opacity = alt.condition(click, alt.value(1), alt.value(0.2)) 
    ).properties(
        width=250,
        height=250
    )

    icons2 = alt.Chart(paternal_leave).mark_image(
        width = 50,
        height = 50
    ).encode(
        y='Country:N',
        x='Value:Q',
        url = 'icon',
        opacity = alt.condition(click, alt.value(1), alt.value(0.2)) 
    ).properties(
        width=250,
        height=250
    )

    paternal = bars2+icons2

    leaves = alt.hconcat(maternal,paternal)

    return alt.vconcat(line_chart,leaves)
    

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
        year = st.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)

        graph = graphs2(df, countries, year)
        st.altair_chart(graph,use_container_width=True)

