import utils as ut
import numpy as np
import matplotlib.pyplot as plt


'''
# to compare with the excel sheet (constant inflation and returns over T)
historical_SP_capgain = [9]*45
historical_SP_div_yield = [2]*45
historical_SP_total_yield = [10]*45
historical_inflation_US  = [2.43]*45
historical_inflation_CH  = [2.43]*45
historical_inflation_IT  = [2.43]*45
'''


# input:
N   = 10
yearly_salary = 100         # yearly salary 
month_perc_savings = 0.3    # percentage of monthly salary invested
nr_y_s = 1                  # amount of yearly salaries for initial investment
Bonus = 10                  # End of year bonus (or 13th installment)
country = 'Switzerland'     # Country of residence for inflation and taxes
pl = False

total_wealth = ut.wrapper(N, yearly_salary,month_perc_savings,nr_y_s,Bonus,country,pl)
print(np.percentile(total_wealth, 10))
      



# YEARS TO FREEDOM
nr_y_s = 1                  # amount of yearly salaries for initial investment
Bonus = 0                 # End of year bonus (or 13th installment)
country = 'Switzerland'     # Country of residence for inflation and taxes
pl = False

yearly_salary = 100         # yearly salary 
percentage_savings = [i * 0.05 for i in range(1, 17)]    # percentage of monthly salary invested
years_to_freedom =   [-1]*len(percentage_savings) 

for ii in range(len(years_to_freedom)):
    #print(ii)
    no_fire = True
    N=0
    while N<35 and no_fire:
        N += 1
        total_wealth = ut.wrapper(N, yearly_salary,percentage_savings[ii],nr_y_s,Bonus,country,pl)
        no_fire = (0.04*np.percentile(total_wealth, 10)) < ((1-percentage_savings[ii])*yearly_salary)
    years_to_freedom[ii] = N      

print(years_to_freedom)
plt.figure(figsize=(10, 12))
plt.plot(percentage_savings, years_to_freedom)
plt.title("years to freedom")
plt.ylabel("Nr of years to work")
plt.xlabel("percentage of savings")
plt.show()


