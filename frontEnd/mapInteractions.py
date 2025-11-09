#https://folium.streamlit.app/draw_support

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from businessLogic.calculateDistance import calculateDistanceClass
from businessLogic.machineLearningActivites import machineLearningUtils
from businessLogic.weather import weatherClass

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

if 'route_data' not in st.session_state:
    st.session_state.route_data = None
if 'age_group' not in st.session_state:
    st.session_state.age_group = None
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'predicted_time_input' not in st.session_state:
    st.session_state.predicted_time_input = None
if 'total_distance' not in st.session_state:
    st.session_state.total_distance = None
if 'weather' not in st.session_state:
    st.session_state.weather = None
if 'elevation' not in st.session_state:
    st.session_state.elevation = None

def set_total_distance(total_distance,age_group,gender):
    st.session_state["route_data"] = total_distance
    if gender=='Male':
        gender_label = 'M'
    else:
        gender_label = 'F'
    st.session_state["gender"]=gender
    st.session_state['age_group']=age_group
    if st.session_state["route_data"]['all_drawings'] == None:
        st.write('Please plot a route before submitting')
    else:
        distanceElevation = calculateDistanceClass(total_distance['all_drawings']).calculateDistanceEvaluate()
        st.session_state["total_distance"] = str(round(int(distanceElevation[0]), 2)) + ' km'
        if str(distanceElevation[1]) == None:
            elevation = 0
        else:
            elevation = str(round(int(elevation[0]), 2))
        st.session_state["elevation"] = elevation + ' m'
        predictedTime = machineLearningUtils(distanceElevation[0],age_group,gender_label).predictModel()
        st.session_state["predicted_time_input"] = str(round(int(predictedTime[0]), 2)) + '  minutes'
        feedback = st.feedback(options="thumbs",width="content")
        if feedback == 1:
            machineLearningUtils.addToDB(distanceElevation[0],age_group,gender_label,predictedTime)
        st.session_state["weather"] = weatherClass().runEvent()
        

def refresh_data():
    pass
with col1:
    with st.form("my_form"):
        output = st_folium(m, width=2000 , height = 500) #OUTPUTTING THE MAP
        age_group = st.selectbox('Age Group', ['18 - 34','35 - 54','55 +'])
        gender = st.selectbox('Gender', ['Female','Male'])
        st.form_submit_button('Submit Route' , key='Submit', on_click=set_total_distance, args=[output,age_group,gender])
with col2:
    total_distance= st.text_input('Total Distance', key="total_distance" , disabled=True, label_visibility="visible", width="stretch")
    weather= st.text_input('Weather information', key="weather" , disabled=True, label_visibility="visible", width=200)
    elevation= st.text_input('Route Elevation', key="elevation" , disabled=True, label_visibility="visible", width=200)
    predicted_time_input =st.text_input('Predicted time', key="predicted_time_input" , disabled=True, label_visibility="visible", width="stretch")
    st.button( "Pull recent Strava data",key="refresh",help="Pull the latest records from your Strava account",
              use_container_width=True, on_click=refresh_data, args=(True),kwargs={"limit": 500},)




