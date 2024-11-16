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
    pages.a_prediction()

elif add_sidebar == 'Prediction on a Dataset':
    pages.ds_prediction()

elif add_sidebar == 'Show result of the Analysis':
    pages.my_analysis()



