#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 13:58:41 2024

@author: giuseppesinatra
"""

"""
Created on Wed Nov 6 2024

@author: Giuseppe Sinatra
"""

import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
from PIL import Image



add_sidebar = st.sidebar.selectbox('Menu', ('Home', 'Make a prediction','Prediction on a Dataset','Show result of the Analylis'))

image1 = 'Ritratto_Galileo.jpg'
image2 = 'ML_brain.png'
github_logo = Image.open('logo_github.png')
linkedin_logo = Image.open('logo_linkedin.png')

if add_sidebar == 'Home':
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

elif add_sidebar == 'Make a prediction':
    st.title("Make a prediction")
    length = st.number_input('Enter length in meters', key="length_input")
    mass = st.number_input('Enter mass in kilograms', key="mass_input")
    angle = st.number_input('Enter angle in degres (0°-90°)', key="angle_input")
    angle_rd = angle * math.pi / 180
    if (length < 0 or mass < 0 or angle < 0 or angle > 90):
        st.write('Wrong input please try again')
    if st.button('Calcola'):
        if angle > 20:
            df = pd.read_csv('coefficients.csv')
            intercept = df.at[0, 'Intercept']
            first_param = df.at[0, 'First Parameter(L)']
            second_param = df.at[0, 'Second Parameter (A)']
            prediction = 10 ** intercept * (length) ** first_param * (angle_rd) ** second_param
            th_prediction = 2 * math.pi * (length / 9.8) ** 0.5 * (1 + angle_rd ** 2 / 16)
            st.success(f'Model Prediction: {prediction:.2f} s')
            st.success(f'Theoretical Prediction: {th_prediction:.2f} s')
            st.text('Equation of the ML model:')
            st.markdown('$$T=10^{0.316}\cdot L^{0.516}\cdot \Theta^{0.031}$$')

        else:
            df = pd.read_csv('coefficients_sa.csv')
            intercept = df.at[0, 'Intercept']
            slope = df.at[0, 'Slope']
            prediction = 10 ** intercept * (length) ** slope
            th_prediction = 2 * math.pi * (length / 9.8) ** 0.5
            st.success(f'Model Prediction for Small Angles: {prediction:.2f} s')
            st.success(f'Theoretical Prediction Small Angles: {th_prediction:.2f} s')
            st.text('Equation of the ML model:')
            st.markdown('$$ T = 10^{0.292}\cdot L^{0.509} $$')


elif add_sidebar == 'Prediction on a Dataset':
    st.title('Prediction on a Dataset')
    st.text('The CSV file has to have follow this example:')
    example_df = pd.DataFrame({'Period (s)':[1.716,1.676,1.673],
                               'Length (m)':[0.8,0.7,0.66], 'Mass (kg)': [0.2668,0.2668,0.2668],
                               'Angle (deg)':[10, 30, 20]})
    st.write(example_df)
    uploaded_file = st.file_uploader("Load a CSV file", type="csv")
    if uploaded_file is not None:
        data_df = pd.read_csv(uploaded_file)
        st.write(data_df.head())

        filtered_df = data_df[data_df['Angle (deg)'] <= 20]
        Sorted_filtered_df = filtered_df.sort_values(by='Length (m)', ascending=True)
        df = pd.read_csv('coefficients_sa.csv')
        intercept = df.at[0, 'Intercept']
        slope = df.at[0, 'Slope']
        X = Sorted_filtered_df['Length (m)']
        y = Sorted_filtered_df['Period (s)']
        y_fit = 10 ** intercept * (Sorted_filtered_df['Length (m)']) ** slope
        y_teo = 2 * math.pi * (Sorted_filtered_df['Length (m)'] / 9.8) ** 0.5

        plt.scatter(X, y, label='Data')
        plt.plot(X, y_fit, color='red', label='Best Fit')
        plt.plot(X, y_teo, color='black', label='Th. function')

        plt.title('Comparison between Theory and ML model')
        plt.xlabel('Length (m)')
        plt.ylabel('Period (s)')
        plt.legend()
        plt.grid(True)
        plt.savefig('prediction_on_dataset_sa.jpg')
        st.image('prediction_on_dataset_sa.jpg', use_column_width=True)
        st.text('Equation of the ML model:')
        st.markdown('$$ T = 10^{0.292}\cdot L^{0.509} $$')

        data_df['Angle (rad)']=data_df['Angle (deg)']*math.pi/180
        Sorted_df = data_df.sort_values(by='Length (m)', ascending=True)
        df = pd.read_csv('coefficients.csv')
        intercept = df.at[0, 'Intercept']
        first_param = df.at[0, 'First Parameter(L)']
        second_param = df.at[0, 'Second Parameter (A)']
        X = Sorted_df['Length (m)']
        Y = Sorted_df['Angle (rad)']
        z = Sorted_df['Period (s)']
        z_fit = (10**intercept)*(X**first_param)*(Y**second_param)
        z_teo = 2*math.pi*(X/9.8)**0.5*(1+Y**2/16)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.scatter(X, Y, z, color='blue', label='Data', alpha=0.5)
        ax.scatter(X, Y, z_fit, color='yellow', label='Best Fit', alpha=0.5)
        ax.scatter(X, Y, z_teo, color='red', label='Th. function', alpha=0.5)

        ax.set_title('Comparison between Theory and ML model (Small Angles)')
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Angle (rad)')
        ax.set_zlabel('Period (s)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('prediction_on_dataset.jpg')
        st.image('prediction_on_dataset.jpg', use_column_width=True)
        st.text('Equation of the ML model:')
        st.markdown('$$T=10^{0.316}\cdot L^{0.516}\cdot \Theta^{0.031}$$')


elif add_sidebar == 'Show result of the Analylis':
    st.title("Show result of the Analylis")
    st.image("plots_by_angles.jpg", caption="Plots and correlation matrix to data visualization", use_column_width=True)
    st.image("sp_with_constant_length.jpg", caption="Ploths with fixed length")
    st.subheader("Result of the analysis for angle smaller than 20°")
    st.text('Equation of the ML model:')
    st.markdown('$$ T = 10^{0.292}\cdot L^{0.509} $$')
    st.image("LR_small_angles.jpg", caption="Log Best fit", use_column_width=True)
    st.image("Comparison_plot_small_angles.jpg", caption="Interesting comparison between the Model and the Theory", use_column_width=True)
    with open('results_sa.txt', 'r') as file:
        info_sa = file.readlines()

    st.write(info_sa[0])
    st.write(info_sa[1])
    st.write(info_sa[2])
    st.subheader("Result of the analysis for all the angle values")
    st.text('Equation of the ML model:')
    st.markdown('$$T=10^{0.316}\cdot L^{0.516}\cdot \Theta^{0.031}$$')
    st.image("Comparison_3D_plot.jpg", caption='3D comparison between data, model and theory')

    with open('results.txt', 'r') as file:
        info = file.readlines()

    st.write(info[0])
    st.write(info[1])
    st.write(info[2])
