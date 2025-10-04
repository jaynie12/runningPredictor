#https://folium.streamlit.app/draw_support

import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium

st.header('Running route predictor')
st.text('Please plot your route below and enter to recieve a predicted time')

m = folium.Map(location=[50.7365,  -3.5344], zoom_start=5)
Draw(export=True).add_to(m)

c1, c2 = st.columns(2)
with c1:
    output = st_folium(m, width=700, height=500)

with c2:
    st.write(output)