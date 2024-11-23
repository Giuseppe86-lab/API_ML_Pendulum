import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import math
from PIL import Image

def small_angles_plot(data):
    Sorted_filtered_df = data.sort_values(by='Length (m)', ascending=True)
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
        title="Comparison between Theory and ML model (Small Angles)",
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

def all_angles_plot(data):
    Sorted_df = data.sort_values(by='Length (m)', ascending=True)
    df = pd.read_csv('coefficients.csv')
    intercept = df.at[0, 'Intercept']
    first_param = df.at[0, 'First Parameter(L)']
    second_param = df.at[0, 'Second Parameter (A)']
    X = Sorted_df['Length (m)']
    Y = Sorted_df['Angle (rad)']
    z = Sorted_df['Period (s)']
    z_fit = (10 ** intercept) * (X ** first_param) * (Y ** second_param)
    z_teo = 2 * math.pi * (X / 9.8) ** 0.5 * (1 + Y ** 2 / 16)

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

def my_analysis():
    st.title("Show result of the Analysis")
    st.image("plots_by_angles.jpg", caption="Plots and correlation matrix to data visualization", use_column_width=True)
    st.image("sp_with_constant_length.jpg", caption="Ploths with fixed length")
    st.subheader("Result of the analysis for angle smaller than 20°")
    st.image("LR_small_angles.jpg", caption="Log Best fit", use_column_width=True)
    data_analysis = pd.read_csv('dataset_pendulum.csv')
    filtered_df = data_analysis[data_analysis['Angle (deg)'] <= 20]
    small_angles_plot(filtered_df)
    with open('results_sa.txt', 'r') as file:
        info_sa = file.readlines()

    st.write(info_sa[0])
    st.write(info_sa[1])
    st.write(info_sa[2])
    st.subheader("Result of the analysis for all the angle values")
    data_analysis['Angle (rad)'] = data_analysis['Angle (deg)'] * math.pi / 180
    all_angles_plot(data_analysis)

    with open('results.txt', 'r') as file:
        info = file.readlines()

    st.write(info[0])
    st.write(info[1])
    st.write(info[2])

def ds_prediction():
    st.title('Prediction on a Dataset')
    st.text('The CSV file has to have follow this example:')
    example_df = pd.DataFrame({'Period (s)': [1.716, 1.676, 1.673],
                               'Length (m)': [0.8, 0.7, 0.66], 'Mass (kg)': [0.2668, 0.2668, 0.2668],
                               'Angle (deg)': [10, 30, 20]})
    st.write(example_df)
    uploaded_file = st.file_uploader("Load a CSV file", type="csv")
    if uploaded_file is not None:
        data_df = pd.read_csv(uploaded_file)
        st.write(data_df.head())

        filtered_df = data_df[data_df['Angle (deg)'] <= 20]
        small_angles_plot(filtered_df)

        data_df['Angle (rad)'] = data_df['Angle (deg)'] * math.pi / 180
        all_angles_plot(data_df)


def a_prediction():
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

def home_page():
    image1 = 'Ritratto_Galileo.jpg'
    image2 = 'ML_brain.png'
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
        st.link_button('GitHub Repository', 'https://github.com/Giuseppe86-lab/API_ML_Pendulum')

    with col4:
        st.link_button('My Linkedin Profile', 'http://www.linkedin.com/in/giuseppe-sinatra-phd-ba5835ab')
