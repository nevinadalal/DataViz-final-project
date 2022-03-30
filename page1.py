import altair as alt
from numpy import True_
import streamlit as st
import pandas as pd
from filters import filter_dataset
from vega_datasets import data

def compute_percentage(df, select_indicator, select_country,select_year):
    #select data from the dataset
    source = filter_dataset(df, index = select_indicator, countries = [select_country], year = select_year)

    if select_indicator=="EMP10":
        female = source.loc[source.Sex == "W", "Value"]
        male = source.loc[source.Sex =="M", "Value"]

        percentage_female = int((female/(female+male))*100)
    
    else:
        percentage_female = int(source["Value"])
    
    percentage_male = 100-percentage_female
    
    return percentage_female, percentage_male

def maps(df,select_indicator, select_year):

    board_members = df.loc[(df.Indicator == select_indicator) & (df.Year ==select_year),:]

    countries1 = alt.topo_feature(data.world_110m.url, 'countries')
    map_chart = alt.Chart(board_members).mark_geoshape()\
    .encode(color='Value:Q',
            tooltip=['Country:N', 'Value:Q']
           )\
    .transform_lookup(
        lookup='id',
        from_=alt.LookupData(countries1, key='id',
                             fields=["type", "properties", "geometry"])
    )\
    .project('mercator',
         scale=300,
         center=[20,50],
         clipExtent= [[0, 0], [400, 300]])\
    .properties(
        width=500,
        height=300
    )
    return map_chart

def infographic(df, select_indicator, select_country, select_year):
        
        percentage_female,percentage_male = compute_percentage(df, select_indicator, select_country,select_year)
        
        coordinates = pd.DataFrame([[i,j] for j in range(10) for i in range(10)], columns = ["row", "col"])
        coordinates["sex"] = ["Female"]*percentage_female+["Male"]*percentage_male

        person = (
            "M1.7 -1.7h-0.8c0.3 -0.2 0.6 -0.5 0.6 -0.9c0 -0.6 "
            "-0.4 -1 -1 -1c-0.6 0 -1 0.4 -1 1c0 0.4 0.2 0.7 0.6 "
            "0.9h-0.8c-0.4 0 -0.7 0.3 -0.7 0.6v1.9c0 0.3 0.3 0.6 "
            "0.6 0.6h0.2c0 0 0 0.1 0 0.1v1.9c0 0.3 0.2 0.6 0.3 "
            "0.6h1.3c0.2 0 0.3 -0.3 0.3 -0.6v-1.8c0 0 0 -0.1 0 "
            "-0.1h0.2c0.3 0 0.6 -0.3 0.6 -0.6v-2c0.2 -0.3 -0.1 "
            "-0.6 -0.4 -0.6z"
        )

        color_scale = alt.Scale(
            domain=["Female", "Male"],
            range=["rgb(255,102,102)", 'blue']
        )

        infographic = alt.Chart(coordinates).mark_point(
            filled=True,
            size=60
        ).encode(
            x=alt.X("col:O", axis=None),
            y=alt.Y("row:O", axis=None),
            shape=alt.ShapeValue(person),
            color = alt.Color('sex:N', legend = None,scale=color_scale)
        ).configure_view(
            strokeWidth=0
        ).properties(
        width=500,
        height=500
        )
        return infographic, percentage_female

def page1(df,df1, countries):
    indicators = {
    "EMP10": "Share of female managers", 
    "EMP17":"Female share of seats in national parliaments",
    "EMP11":"Female share of seats on boards"}
    ind = ["EMP10","EMP17","EMP11"]
    #define sidebar sliders

    
    select_country = st.sidebar.selectbox("Select the country you want to visualize", countries, index  = countries.index("France"))
    select_year = st.sidebar.slider(label = "Select the year", min_value=2010, max_value=2019, value=2019, step=1)
    select_indicator = st.sidebar.selectbox("Indicator you would like to visualize", ind, format_func  = lambda x: indicators[x])
    mapgraph = maps(df1,select_indicator,select_year)
    st.markdown(f"### {indicators[select_indicator]} in {select_country}")
    st.altair_chart(mapgraph,use_container_width = True)
    
    col1, col2 = st.columns([3,1])
    graph, percentage = infographic(df, select_indicator, select_country, select_year)
    mapgraph = maps(df1,select_indicator,select_year)
    col1.altair_chart(graph)
    percentage_female_lastyear = compute_percentage(df, select_indicator, select_country,select_year-1)[0] if select_year >2010 else 0
    delta = percentage-percentage_female_lastyear
    col2.markdown(f"Year : {select_year}")
    col2.metric(" ",str(percentage)+"%", delta)
    col2.markdown(f"with respect to {select_year-1}")
