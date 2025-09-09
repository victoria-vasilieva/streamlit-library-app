import streamlit as st
import pandas as pd


"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40], 
  'third column': [100, 200, 300, 400]
    })

df

tab1, tab2, tab3 = st.tabs(['eng', 'ger', 'spa'])
with tab1:
    st.write('hello')
with tab2:
    st.write('hallo')
with tab3:
    st.write('hola')