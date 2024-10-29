import streamlit as st
import pandas as pd


st.header("Payroll automation")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])
col1.number_input(label="Year")
col2.number_input(label="Month")
col3.number_input(label="Day")
