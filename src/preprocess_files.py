import pandas as pd

def preprocess_files(payroll, timelock):  

  #Read payroll file and asjust columns
  payroll = pd.read_excel(payroll)
  cols = column_names = ["Conan", "nan", "Location", "nan", "Employee", "nan", "ID", "nan", "Process", "nan", "Chk Date", "nan", "Chk/Vchr", "nan", "Net", "nan", "REG Hrs", "REG Amount", "OT Hrs", "OT Amount", "PTOSK Hrs", "PTOSK Amount", "SICK Hrs", "SICK Amount", "ESICK Hrs", "ESICK Amount", "HSTIP Hrs", "HSTIP Amount", "SBANK Hrs", "SBANK Amount", "nan", "FITW Amount", "nan", "MED Amount", "nan", "SS Amount", "nan", "CO Amount", "nan", "COPFL-EE Amount", "nan", "MDCL Amount","nan", "REIMB Amount", "nan", "4ROTH Amount","nan", "DNTL Amount", "nan", "KMED Amount"]
  payroll.columns = cols
  payroll = payroll.drop([0,1,2]).reset_index(drop=True)
  #------------------------------------------
  # Get the dict to map the employees to the sheets and the department they belong to
  sheet_names = pd.ExcelFile(timelock).sheet_names
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


  return payroll, timelock, empl_trio
