import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import math
import pages
from PIL import Image

def home_page():
    image1 = 'Ritratto_Galileo.jpg'
    image2 = 'ML_brain.png'
    github_logo = Image.open('logo_github.png')
    linkedin_logo = Image.open('logo_linkedin.png')
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption='Ritratto di Galileo Galilei di Justus Sustermans (Galleria degli Uffizi, Firenze)',
                 width=200)
    with col2:
        st.image(image2, caption='By JPxG - DALL-E 3', width=200)

    st.title("A Modern Approach to Pendulum")
    st.subheader("What if...Galileo would have been born in 21st century?")
    st.subheader("by Giuseppe Sinatra")

    st.text('This idea originated from the following thought: \n'
            '"How would Galileo approach his research in the age of big data?" \n'
            'I realized that my computer held extensive laboratory data on \n '
            'pendulum experiments. By gathering part of this data, I was able to assemble a\n'
            'dataset with over 1,500.\n\n'
            "Throughout the analysis, I assumed no prior knowledge of Galileo's famous pendulum\n"
            'law, and I followed these step to develop the model:\n'
            '1. Importing the dataset and saving in a dataframe. \n'
            '2. Analyzing the structure of the data.\n'
            '   2A. Performing exploratory data analysis (EDA).\n'
            '3. Cleaning and further exploring data.\n'
            '4. Preprocessing data for the machine learning model.\n'
            '5. Buiding the model.\n'
            '6. Evaluating results.\n'
            '7. Deploying the model. \n'
            'This dashboard presents the deployment and outcomes of the model. The results allow\n'
            'for evaluating potential corrections to the classic pendulum law, considering\n'
            'that experiments are never conducted under in ideal conditions.\n'
            'Both the data and model consistently show period values slightly lower than\n'
            'theoretical predictions, hinting at a "systematic error".\n\n')

    col3, col4 = st.columns(2)
    with col3:
        if st.button('GitHub Repository', key='Git'):
            st.image(github_logo, width=200)
            st.markdown('[GitHub](https://github.com/Giuseppe86-lab/Personal_Projects/tree/main/4-Pendolum%20e%20ML)')
    with col4:
        if st.button('My Linkedin Profile', key='Linkedin'):
            st.image(linkedin_logo, width=200)
            st.markdown('[LinkedIn](http://www.linkedin.com/in/giuseppe-sinatra-phd-ba5835ab)')