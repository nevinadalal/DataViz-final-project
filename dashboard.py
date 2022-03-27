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
        opacity = alt.condition(click, alt.value(1), alt.value(0.2))   
    ).add_selection(
        click
    ).properties(
        width=600,
        height=300
    ).interactive()

    #maternal leave
    maternal_leave = df.loc[df.Indicator== "EMP18_MAT", :]
    maternal_leave = maternal_leave[maternal_leave.Country.isin(countries)]
    maternal_leave = maternal_leave[maternal_leave.Year == year]
    maternal_leave["icon"]="data:image/png;base64,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"


    #paternal leave
    paternal_leave = df.loc[df.Indicator== "EMP18_PAT", :]
    paternal_leave = paternal_leave[paternal_leave.Country.isin(countries)]
    paternal_leave = paternal_leave[paternal_leave.Year == year]
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
        year = st.sidebar.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)

        graph = graphs2(df, countries, year)
        st.altair_chart(graph,use_container_width=True)

