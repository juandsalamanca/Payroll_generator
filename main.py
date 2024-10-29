import streamlit as st
import pandas as pd
from src.produce_payroll_output import *
from format_date import *

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
e_year = col1.number_input(label="Year", "key=e_year")
e_month = col2.number_input(label="Month", key="e_month")
s_day = col3.number_input(label="Day", key="s_day")

end_date_string = " ".join([str(e_year), str(e_month), str(e_day)])

pay_period = [start_date_string, end_date_string]
#-----------------------------------------------------------------------------------------

UPLOAD FILES AND PRE-PROCESS THEM

payroll_register = st.file_uploader("Upload the payroll register file")

timelock = st.file_uploader("Upload the timelock file")

  #-----------------------------------------------------------------------------------------
if payroll_register and timelock:
  # Produce the output files:
  VTC, VTE = produce_payroll_output(payroll=payroll, time_file_path=timelock, empl_trio=empl_trio, pay_period=pay_period)
  
  @st.cache_data
  def convert_df(df):
      # IMPORTANT: Cache the conversion to prevent computation on every rerun
      return df.to_excel().encode("utf-8")
  
  VTC_csv = convert_df(VTC)
  VTE_csv = convert_df(VTE, "VTE_output")
  
  st.download_button(
      label="Download the VTC_output",
      data=VTC_csv,
      file_name="VTC_output.csv",
      mime="text/csv",
  )
  
  st.download_button(
      label="Download the VTE_output",
      data=VTE_csv,
      file_name="VTE_output.csv",
      mime="text/csv",
  )
