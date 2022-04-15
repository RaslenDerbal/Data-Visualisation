
#All the imports to do

import numpy as np
import streamlit as st 
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
from functools import wraps
import time
import seaborn as sns
import os

#Opening and loading the data
@st.cache
def open_data(nrows):
    return pd.read_csv('data_vis.csv',nrows=nrows)


#Settings of the visualisation
st.set_page_config(page_title="Data Visualisation Rattrapages", layout="centered", initial_sidebar_state="expanded")

#Open the data
agri = open_data(50)
st.title('French agriculture vizualisation tool')
st.markdown("""Here is a simple visualization the data obtained on datagouv.fr """)

if st.checkbox('Do you want to see the dataset?'):
    st.subheader('Here it is')
    st.write(agri.sample(frac= 0.5,replace = True, random_state=1))


#I want to know for how much time the function has run
def function_time(fonction):
    @wraps(fonction)
    def temps(*args, **kwargs):
        debut =time()
        try:
            return fonction(*args, **kwargs)
        finally:
            fin = time() - debut
            with open("logs.txt","a") as o:
                o.write('Total time of execution: {end}s')
            print(f'Total time of execution: {fin}s')
    return temps

#Plot the data in multiple forms

#Adding the filters on the dataset
st.sidebar.header('Choose what to show')
slide = st.slider('Linear graph or Map graph here :',min_value= 0 , max_value= 2)
graph = st.sidebar.selectbox(label ="Choose what graph to use",options=['','Pie','Bar'])
colonnes = agri.select_dtypes(['float','int','object']).columns

#Coordonates for the bar
scat1 = {"":"","Culture Code" : agri['CODE_CULTU'],"Culture Library" : agri['LBL_CULTU']}
scat2 = {"":"","Surface" : agri['SURFACE_HA']}

#Add the figures
@function_time
def figure(dataset):
    
    #Pie chart
    if graph == 'Pie':
        camembert = px.pie(data_frame=dataset, values='GRP_CULTU', names='Cultures', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(camembert)
        
    #Bar chart
    if graph == 'Bar':
        st.sidebar.subheader('Choose values to show')
        abscissa = st.sidebar.selectbox('Abscissa', options=scat1)
        ordonate =  st.sidebar.selectbox('Ordonate', options=scat2)
        barre = px.scatter(data_frame=dataset, x=abscissa ,y=ordonate, color_discrete_sequence=px.colors.sequential.RdBu)
        barre.show()
      
