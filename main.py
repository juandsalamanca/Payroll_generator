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

#------------------

# Get the dict to map the employees to the sheets and the department they belong to
sheet_names = pd.ExcelFile(excel_file).sheet_names
name_pairs = {}
# Loop through each sheet and read its contents
employees = payroll["Employee"]
for sheet in sheet_names:
  for employee in employees:
    spl = employee.split()
    cnt = 0
    for word in spl:
      word = word.replace(",", "")
      if word in sheet:
        cnt += 1
    if cnt > 1:
      name_pairs[employee] = sheet.strip()

empl_categories = {"Rowlee, Adam G.":"VTC", "Stinson, Spencer A.":"VTC", "Russell, Bryan T.":"VTC", "Fant, Ashley L.":"VTC", "Heim, Christian": "VTC", "Connor, Connor J.":"VTE", "Smith, Der":"VTC", "Fife, Devon N.":"VTC", "Moore, Elijah J.":"VTC", "Harvey, Elliott J.":"VTE", "Hegreness, Eric D.":"VTC", "Rice, Eric":"VTC", "Edwards, RJ L.":"VTC"}
empl_trio = {}
for key in name_pairs:
  s_key = key.strip()
  empl_trio[key] = [name_pairs[key], empl_categories[s_key]]

#-----------------------
#Read payroll file and asjust columns
payroll = pd.read_excel(payroll_register)
cols = column_names = ["Conan", "nan", "Location", "nan", "Employee", "nan", "ID", "nan", "Process", "nan", "Chk Date", "nan", "Chk/Vchr", "nan", "Net", "nan", "REG Hrs", "REG Amount", "OT Hrs", "OT Amount", "PTOSK Hrs", "PTOSK Amount", "SICK Hrs", "SICK Amount", "ESICK Hrs", "ESICK Amount", "HSTIP Hrs", "HSTIP Amount", "SBANK Hrs", "SBANK Amount", "nan", "FITW Amount", "nan", "MED Amount", "nan", "SS Amount", "nan", "CO Amount", "nan", "COPFL-EE Amount", "nan", "MDCL Amount","nan", "REIMB Amount", "nan", "4ROTH Amount","nan", "DNTL Amount", "nan", "KMED Amount"]
payroll.columns = cols
payroll = payroll.drop([0,1,2]).reset_index(drop=True)

#-----------------------------------------------------------------------------------------

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
