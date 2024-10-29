def update_payroll_output(employee, net_pay, job_pay, taxes, benefits, VT, pay_period):

  #Job pay
  for job in job_pay:
    VT["Date"].append(pay_period[1])
    VT["Account"].append("5000 Direct - Labor")
    VT["Debits"].append(job_pay[job])
    VT["Credits"].append("-")
    VT["Description"].append(f"Payroll {pay_period[0]} to {pay_period[1]}")
    VT["Name"].append(job)
    VT["Employee"].append(employee)

  #Payroll taxes
  VT["Date"].append(pay_period[1])
  VT["Account"].append("6362 Payroll Taxes")
  VT["Debits"].append(taxes[1]+ taxes[2])
  VT["Credits"].append("-")
  VT["Description"].append(f"Payroll {pay_period[0]} to {pay_period[1]}")
  VT["Name"].append("ER Portion of Payroll Taxes")
  VT["Employee"].append(employee)
  #Benefits
  VT["Date"].append(pay_period[1])
  VT["Account"].append("6363 Employee Benefits")
  VT["Debits"].append("-")
  VT["Credits"].append(benefits)
  VT["Description"].append(f"Payroll {pay_period[0]} to {pay_period[1]}")
  VT["Name"].append("")
  VT["Employee"].append(employee)
  
  #Accrued payroll
  VT["Date"].append(pay_period[1])
  VT["Account"].append("2101 Accrued Payroll")
  VT["Debits"].append("-")
  VT["Credits"].append(net_pay)
  VT["Description"].append(f"Payroll {pay_period[0]} to {pay_period[1]}")
  VT["Name"].append("")
  VT["Employee"].append(employee)

  #Accrued payroll taxes
  VT["Date"].append(pay_period[1])
  VT["Account"].append("2102 Accrued Payroll Taxes")
  VT["Debits"].append("-")
  VT["Credits"].append(sum(taxes))
  VT["Description"].append(f"Payroll {pay_period[0]} to {pay_period[1]}")
  VT["Name"].append("")
  VT["Employee"].append(employee)

  return VT