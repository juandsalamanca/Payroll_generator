import streamlit as st
import pandas as pd
from src.produce_payroll_output import *
from src.format_date import *
from src.preprocess_files import *

st.header("Payroll automation")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])

#--------------------------------------------------------------------------------
# START AND END DATES FOR PAY PERIOD:

st.text("Select the start date of the pay period")
s_year = col1.number_input(label="Year", key="s_year")
s_month = col2.number_input(label="Month",key="s_month")
s_day = col3.number_input(label="Day",key="s_day")

start_date_string = " ".join([str(s_year), str(s_month), str(s_day)])

st.text("Select the end date of the pay period")
e_year = col1.number_input(label="Year", key="e_year")
e_month = col2.number_input(label="Month", key="e_month")
s_day = col3.number_input(label="Day", key="s_day")

end_date_string = " ".join([str(e_year), str(e_month), str(e_day)])

pay_period = [start_date_string, end_date_string]
#-----------------------------------------------------------------------------------------

#UPLOAD FILES AND PRE-PROCESS THEM

payroll_register = st.file_uploader("Upload the payroll register file")

timelock = st.file_uploader("Upload the timelock file")

@st.cache_data
def process_data(payroll, timelock, pay_period):
  payroll, timelock, empl_trio = preprocess_files(payroll=payroll_register, timelock=timelock)
  # Produce the output files:
  VTC, VTE = produce_payroll_output(payroll=payroll, time_file_path=timelock, empl_trio=empl_trio, pay_period=pay_period)
  VTC_excel = VTC.to_excel().encode("utf-8")
  VTE_excel = VTE.to_excel().encode("utf-8")
  return VTC_excel, VTE_excel
#-----------------------------------------------------------------------------------------
if payroll_register and timelock:

  VTC_excel, VTE_excel = process_data(payroll=payroll_register, timelock=timelock, pay_period=pay_period)

  st.download_button(
      label="Download the VTC_output",
      data=VTC_excel,
      file_name="VTC_output.csv",
      mime="text/csv",
  )
  
  st.download_button(
      label="Download the VTE_output",
      data=VTE_excel,
      file_name="VTE_output.csv",
      mime="text/csv",
  )
