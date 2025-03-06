import streamlit as st

st.title("Navigating the Business Landscape: Trends and Insights from 2020")
st.write(
    "Explore the geographic distribution and financial strength of the world’s leading companies")




import pandas as pd
import numpy as np
df = pd.read_csv("updated_data.csv")

# Display the first few rows of the dataframe
st.write(df.head())

