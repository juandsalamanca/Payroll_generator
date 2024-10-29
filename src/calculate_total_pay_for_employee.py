import pandas as pod

def calculate_total_pay_for_employee(payroll, idx, cols):
  pay = 0
  for index in range(cols[0], cols[1]+1):
    col_name = payroll.columns[index]
    if "Amount" in col_name:
      payment = payroll.loc[idx, col_name]
      if pd.isna(payment) == False and payment != None:
        pay += payment
  return pay
