import streamlit as st
import pandas as pd
from src.produce_payroll_output import *


st.header("Payroll automation")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])

st.text("Select the start date of the pay period")
s_year = col1.number_input(label="Year", key="s_year")
s_month = col2.number_input(label="Month",key="s_month")
s_day = col3.number_input(label="Day",key="s_day")

st.text("Select the end date of the pay period")
e_year = col1.number_input(label="Year", "key=e_year")
e_month = col2.number_input(label="Month", key="e_month")
s_day = col3.number_input(label="Day", key="s_day")

payroll_register = st.file_uploader("Upload the payroll register file")

timelock = st.file_uploader("Upload the timelock file")

payroll = pd.read_excel(payroll_register)
cols = column_names = ["Conan", "nan", "Location", "nan", "Employee", "nan", "ID", "nan", "Process", "nan", "Chk Date", "nan", "Chk/Vchr", "nan", "Net", "nan", "REG Hrs", "REG Amount", "OT Hrs", "OT Amount", "PTOSK Hrs", "PTOSK Amount", "SICK Hrs", "SICK Amount", "ESICK Hrs", "ESICK Amount", "HSTIP Hrs", "HSTIP Amount", "SBANK Hrs", "SBANK Amount", "nan", "FITW Amount", "nan", "MED Amount", "nan", "SS Amount", "nan", "CO Amount", "nan", "COPFL-EE Amount", "nan", "MDCL Amount","nan", "REIMB Amount", "nan", "4ROTH Amount","nan", "DNTL Amount", "nan", "KMED Amount"]
payroll.columns = cols
payroll = payroll.drop([0,1,2]).reset_index(drop=True)

VTC, VTE = produce_payroll_output(payroll=payroll, time_file_path=timelock, empl_trio=empl_trio, pay_period=pay_period)
