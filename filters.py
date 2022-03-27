import pandas as pd

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