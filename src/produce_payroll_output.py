import pandas as pd
import numpy as np
from datetime import datetime
from src.calculate_total_pay_for_employee import *
from src.time_string_to_float import *
from src.update_payroll_output import *

def produce_payroll_output(payroll, time_file_path, empl_trio, pay_period):

  pay_column = ["REG Hrs", "SBANK Amount"]
  pay_col_indexes = [payroll.columns.get_loc(col) for col in pay_column]
  tax_column = ["FITW Amount", "COPFL-EE Amount"]
  tax_col_indexes = [payroll.columns.get_loc(col) for col in tax_column]
  benefit_column = ["MDCL Amount", "KMED Amount"]
  benefit_col_indexes = [payroll.columns.get_loc(col) for col in benefit_column]
  employees = payroll["Employee"]
  VTC = {"Date":[], "Account":[], "Debits":[], "Credits":[], "Description":[], "Name":[], "Employee":[]}
  VTE = {"Date":[], "Account":[], "Debits":[], "Credits":[], "Description":[], "Name":[], "Employee":[]}
  date = datetime.today()
  i=0
  while i < len(employees):
    employee = employees[i]
    sheet = empl_trio[employee][0]
    cat = empl_trio[employee][1]
    time_df = pd.read_excel(time_file_path, sheet_name = sheet)
    cols = time_df.loc[0]
    time_df.columns = cols
    time_df = time_df.drop([0]).reset_index(drop=True)
    work_time_col =  time_df["Total Work Time"]
    total_work_time = 0
    job_hours = {}
    j=0
    #Calculate toal pay and get net pay:
    net_pay = payroll.loc[i, "Net"]
    #print("Earnings:")
    total_pay = calculate_total_pay_for_employee(payroll=payroll, idx=i, cols=pay_col_indexes)
    #Calculate money paid for taxes:
    total_tax = calculate_total_pay_for_employee(payroll=payroll, idx=i, cols=tax_col_indexes)
    MED = payroll.loc[i, "MED Amount"]
    SS = payroll.loc[i, "SS Amount"]
    taxes = [total_tax, MED, SS]
    #Calculate money paid for benefits:
    total_benefit = calculate_total_pay_for_employee(payroll=payroll, idx=i, cols=benefit_col_indexes)
    #Calculate work hours for each employee:
    while j < len(work_time_col):
      work_time = work_time_col[j]
      job = time_df.loc[j, "Job"]
      if pd.isna(job) == False and job != None:
        #print("Job:", job)
        work_hours = time_string_to_float(work_time)
        total_work_time+=work_hours
      
        if job not in job_hours:
          job_hours[job] = []
          job_hours[job].append(work_hours)
        else:
          job_hours[job].append(work_hours)
      j+=1
    #Calculate the percentage decicated to each job:
    job_percentages = {}
    for key in job_hours:
      subtotal = sum(job_hours[key])
      job_percentages[key] = subtotal/total_work_time
    #Calculate the pay gotten from each job using the percentages:
    job_pay = {}
    for key in job_percentages:
      subpay = total_pay * job_percentages[key]
      job_pay[key] = subpay
    #Update the correct dict with all the relevant info
    if cat == "VTC":
      VTC = update_payroll_output(employee=employee, net_pay=net_pay, job_pay=job_pay, taxes=taxes, benefits=total_benefit, VT=VTC, pay_period=pay_period)
    elif cat == "VTE":
      VTE = update_payroll_output(employee=employee, net_pay=net_pay, job_pay=job_pay, taxes=taxes, benefits=total_benefit, VT=VTE, pay_period=pay_period)
    i+=1

  return pd.DataFrame(VTC), pd.DataFrame(VTE)
