import streamlit as st
import altair as alt
from vega_datasets import data

source = data.cars()

fig = alt.Chart(source).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).properties(
    width=500,
    height=500
).interactive()

st.write(fig)