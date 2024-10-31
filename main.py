import streamlit as st
import pandas as pd
from datetime import datetime
from src.produce_payroll_output import *
from src.format_date import *
from src.preprocess_files import *

st.title("Payroll automation")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])

#--------------------------------------------------------------------------------
# START AND END DATES FOR PAY PERIOD:
current_year = current_year = datetime.now().year
current_month = datetime.now().month

st.text("Select the start date of the pay period")
col11, col12, col13, col14 = st.columns([0.15, 0.15, 0.15, 0.55])
s_year = col11.number_input(label="Year", key="s_year",step = 1, value = current_year)
s_month = col12.number_input(label="Month",key="s_month", step = 1, value = current_month)
s_day = col13.number_input(label="Day",key="s_day",step = 1, value = 1)

start_date_string = " ".join([str(s_year), str(s_month), str(s_day)])

st.text("Select the end date of the pay period")
col21, col22, col23, col24 = st.columns([0.15, 0.15, 0.15, 0.55])

e_year = col21.number_input(label="Year", key="e_year", step = 1, value = current_year)
e_month = col22.number_input(label="Month", key="e_month", step = 1, value = current_month)
e_day = col23.number_input(label="Day", key="e_day", step = 1, value = 15)

end_date_string = " ".join([str(e_year), str(e_month), str(e_day)])

pay_period = [start_date_string, end_date_string]
#-----------------------------------------------------------------------------------------

#UPLOAD FILES AND PRE-PROCESS THEM

payroll_register = st.file_uploader("Upload the payroll register file")

timelock = st.file_uploader("Upload the timelock file")


def process_data(payroll, timelock, pay_period):
  payroll, timelock, empl_trio = preprocess_files(payroll=payroll_register, timelock=timelock)
  # Produce the output files:
  VTC, VTE = produce_payroll_output(payroll=payroll, time_file_path=timelock, empl_trio=empl_trio, pay_period=pay_period)
  VTC_excel = VTC.to_csv(index = False).encode("utf-8")
  VTE_excel = VTE.to_csv(index = False).encode("utf-8")
  return VTC_excel, VTE_excel
#-----------------------------------------------------------------------------------------
if payroll_register and timelock:

  run = st.button("Process files")

  if "processed" not in st.session_state:
    st.session_state.processed = False
    
  if run:
    st.session_state.processed = True
    
    VTC_excel, VTE_excel = process_data(payroll=payroll_register, timelock=timelock, pay_period=pay_period)
    st.session_state.VTC = VTC_excel
    st.session_state.VTE = VTE_excel

  if st.session_state.processed == True:
  
    st.download_button(
        label="Download the VTC_output",
        data=st.session_state.VTC,
        file_name=f"VTC_output_{current_year}_{current_month}_{str(s_day)}_to_{str(e_day)}.csv",
        mime="text/csv",
    )
    
    st.download_button(
        label="Download the VTE_output",
        data=st.session_state.VTE,
        file_name=f"VTE_output_{current_year}_{current_month}_{str(s_day)}_to_{str(e_day)}.csv",
        mime="text/csv",
    )
