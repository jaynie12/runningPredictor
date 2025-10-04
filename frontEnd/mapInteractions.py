#https://folium.streamlit.app/draw_support

import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
st.set_page_config(layout="wide") # Ensures the layout spans the full page
st.header('Running route predictor')
st.text('Please plot your route below and enter to recieve a predicted time')

m = folium.Map(location=[50.7365,  -3.5344], zoom_start=500)
Draw(export=True).add_to(m)

#0.7 and 0.3 show the relative size of the columns so one is 70& and the other is 30%
col1, col2 = st.columns([4,1], width=100000 )

with col1:
    with st.form("my_form"):
        output = st_folium(m, width=2000 , height = 500) #OUTPUTTING THE MAP
        age_group = st.selectbox('Age Group', ['18-34','35 - 54','55+'])
        gender = st.selectbox('Gender', ['Female','Male'])
        st.form_submit_button('Submit Route')
with col2:
    total_distance= st.text_input('Total Distance', value="" , disabled=False, label_visibility="visible", width="stretch")
    total_elevation =st.text_input('Total Elevation', value="" , disabled=False, label_visibility="visible", width="stretch")
    st.text('If you are happy with the distance and elevation, press below to calculate the predicted time')
    predict_button =st.button('Predict Time')
    st.text_input('Predicted time', value="" , disabled=False, label_visibility="visible", width="stretch")





