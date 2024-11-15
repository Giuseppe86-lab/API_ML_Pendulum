#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 6 2024

@author: Giuseppe Sinatra
"""

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import math
import pages
from PIL import Image

add_sidebar = st.sidebar.selectbox('Menu', ('Home', 'Make a prediction','Prediction on a Dataset','Show result of the Analysis'))

if add_sidebar == 'Home':
    pages.home_page()


elif add_sidebar == 'Make a prediction':
    st.title("Make a prediction")
    length = st.number_input('Enter length in meters', key="length_input")
    mass = st.number_input('Enter mass in kilograms', key="mass_input")
    angle = st.number_input('Enter angle in degres (0°-90°)', key="angle_input")
    angle_rd = angle * math.pi / 180
    if (length < 0 or mass < 0 or angle < 0 or angle > 90):
        st.write('Wrong input please try again')
    if st.button('Calculate'):
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
        # Create the figure
        fig = go.Figure()

        # Scatter plot for actual data
        fig.add_trace(go.Scatter(x=X, y=y, mode='markers', name='Data', marker=dict(color='blue')))

        # Line plot for the best fit line
        fig.add_trace(go.Scatter(x=X, y=y_fit, mode='lines', name='Best Fit', line=dict(color='red')))

        # Line plot for the theoretical function
        fig.add_trace(go.Scatter(x=X, y=y_teo, mode='lines', name='Th. function', line=dict(color='black')))

        # Set titles and labels
        fig.update_layout(
            title="Comparison between Theory and ML model (Small Anglese)",
            xaxis_title="Length (m)",
            yaxis_title="Period (s)",
            showlegend=True,
            template="plotly_white"
        )

        # Show grid
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)
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

        # Crea il grafico 3D con Plotly
        fig = go.Figure()

        # Dati originali
        fig.add_trace(go.Scatter3d(
            x=X, y=Y, z=z,
            mode='markers',
            marker=dict(size=5, color='blue', opacity=0.6),
            name='Data'
        ))

        # Modello ML
        fig.add_trace(go.Scatter3d(
            x=X, y=Y, z=z_fit,
            mode='markers',
            marker=dict(size=5, color='yellow', opacity=0.6),
            name='Best Fit'
        ))

        # Funzione teorica
        fig.add_trace(go.Scatter3d(
            x=X, y=Y, z=z_teo,
            mode='markers',
            marker=dict(size=5, color='red', opacity=0.6),
            name='Th. Function'
        ))

        # Layout del grafico
        fig.update_layout(
            title='Comparison between Theory and ML model',
            scene=dict(
                xaxis_title='Length (m)',
                yaxis_title='Angle (rad)',
                zaxis_title='Period (s)'
            ),
            legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.1),
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        st.text('Equation of the ML model:')
        st.markdown('$$T=10^{0.316}\cdot L^{0.516}\cdot \Theta^{0.031}$$')


elif add_sidebar == 'Show result of the Analysis':
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


