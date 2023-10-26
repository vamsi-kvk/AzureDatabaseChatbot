import pandas as pd
import streamlit as st

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    if is_dataframe(df):
        return df.to_csv().encode('utf-8')
    else:
        return df

def is_dataframe(variable):
    return isinstance(variable, pd.DataFrame)

