import utils as ut
import numpy as np
import matplotlib.pyplot as plt

Year = list(range(1980, 2025 ))

# from: https://www.slickcharts.com/sp500/returns/details
historical_SP_capgain = [25.77, -9.73, 14.76, 17.27, 1.40, 26.33, 14.62, 2.03, 12.40, 27.25, -6.56, 26.31, 4.46, 7.06, -1.54, 34.11, 20.26, 31.01, 26.67, 19.53, -10.14, -13.04, -23.37, 26.38, 8.99, 3.00, 13.62, 3.53, -38.49, 23.45, 12.78, -0.00, 13.41, 29.60, 11.39, -0.73, 9.54, 19.42, -6.24, 28.88, 16.26, 26.89, -19.44, 24.23, 23.31]
historical_SP_div_yield = [6.65, 4.82, 6.79, 5.29, 4.87, 5.40, 4.05, 3.22, 4.21, 4.44, 3.46, 4.16, 3.16, 3.02, 2.86, 3.47, 2.70, 2.35, 1.91, 1.51, 1.04, 1.15, 1.27, 2.30, 1.89, 1.91, 2.17, 1.96, 1.49, 3.01, 3.01, 2.28, 2.79, 2.79, 2.30, 2.11, 2.42, 2.41, 1.86, 2.61, 2.14, 1.82, 1.33, 2.06, 1.71]
historical_SP_total_yield = [32.42, -4.91, 21.55, 22.56, 6.27, 31.73, 18.67, 5.25, 16.61, 31.69, -3.10, 30.47, 7.62, 10.08, 1.32, 37.58, 22.96, 33.36, 28.58, 21.04, -9.10, -11.89, -22.10, 28.68, 10.88, 4.91, 15.79, 5.49, -37.00, 26.46, 15.06, 1.38, 16.00, 32.39, 13.69, 1.36, 11.96, 21.83, -4.38, 31.49, 18.40, 28.71, -18.11, 26.29, 25.02]
# from: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2024&locations=CH&start=1980&utm_source=chatgpt.com
historical_inflation_CH = [4.022501, 6.49031, 5.655102, 2.949794, 2.931457, 3.435399, 0.75031, 1.440322, 1.872469, 3.158297, 5.403296, 5.862305, 4.043857, 3.293556, 0.846679, 1.799073, 0.809836, 0.519012, 0.023674, 0.810207, 1.556525, 0.993705, 0.640208, 0.639134, 0.795145, 1.169042, 1.057531, 0.725732, 2.428207, -0.479697, 0.692359, 0.22999, -0.6876, -0.220196, -0.014411, -1.143909, -0.434619, 0.533788, 0.936335, 0.362886, -0.725875, 0.581814, 2.835028, 2.135401, 1.06234]
historical_inflation_IT = [21.064168, 17.969299, 16.480415, 14.646577, 10.794496, 9.205991, 5.823547, 4.747285, 5.058247, 6.263654, 6.497099, 6.196416, 5.30431, 4.668349, 4.056104, 5.300492, 3.976029, 1.965913, 1.985009, 1.707662, 2.540394, 2.707384, 2.478374, 2.724932, 2.192028, 1.873754, 2.136789, 1.819951, 3.290849, 0.794177, 1.45353, 2.737964, 3.00866, 1.247937, 0.242814, 0.03879, -0.094017, 1.226533, 1.137488, 0.611247, -0.137708, 1.873783, 8.20129, 5.622194, 0.982373]
historical_inflation_US = [13.549202, 10.334715, 6.131427, 3.212435, 4.300535, 3.545644, 1.898048, 3.664563, 4.077741, 4.830557, 5.399547, 4.191931, 3.007945, 2.986976, 2.607531, 2.752342, 3.022415, 2.266706, 1.559073, 2.191274, 3.387632, 2.826065, 1.59082, 2.270747, 2.676444, 3.391277, 3.226346, 2.826363, 3.839128, -0.355857, 1.640909, 3.160993, 2.069306, 1.46481, 1.622278, 0.118627, 1.261583, 2.13011, 2.442583, 1.81221, 1.233584, 4.697859, 8.0028, 4.116338, 2.949525]

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

W0      = yearly_salary * nr_y_s                    # Initial investment
S13     = [yearly_salary/13]*N                      # Once a year investment
Net_S   = [month_perc_savings*yearly_salary/13]*N   # Monthly investment
tax_cg = 0                                          # Capital gain tax
tax_dg = 30                                         # dividend gain tax

realization = [0]*(len(Year)-N)
endowment = [0]*(len(Year)-N)
for ii in range(0,len(Year)-N):
    cg = historical_SP_capgain[ii:(ii+N)]
    dg = historical_SP_div_yield[ii:(ii+N)]
    inflation = historical_inflation_CH[ii:(ii+N)]

    # ===============================
    Total_wealth = ut.simulate(N,inflation,cg,dg,W0,Net_S,S13,tax_dg,tax_cg)
    # ===============================
    endowment[ii] = 0.04*Total_wealth[-1]/12
    realization[ii] = Total_wealth[-1]




###################################################
#''' Distribution monthly endowment
###################################################
plt.hist(endowment, bins=14, edgecolor='black')
plt.title("1980-2024 10Y Rolling window, inflation CH")
plt.xlabel("Monthly endowment [% yearly income]")
plt.ylabel("Frequency")

median = np.median(endowment)
p10 = np.percentile(endowment, 10)
p90 = np.percentile(endowment, 90)
plt.axvline(median, color='red', linestyle='--', label=f'Median = {median:.2f}')
plt.axvline(p10, color='green', linestyle=':', label=f'10th % = {p10:.2f}')
plt.axvline(p90, color='blue', linestyle=':', label=f'90th % = {p90:.2f}')

plt.legend()
plt.show()



###################################################
#''' starting year dependence
###################################################
#'''
# Create figure with 2 vertical subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), height_ratios=[1, 2])

# --- SCATTER PANEL (top) ---
start_years = Year[0:len(realization)]   # gli anni di inizio finestra
ax1.scatter(start_years, np.array(realization) )
ax1.set_title("Wealth outcome vs starting year of 10Y window")
ax1.set_ylabel("Total wealth [% yearly income]")
ax1.grid(True)

# --- HISTOGRAM PANEL (bottom) ---
ax2.hist(realization, bins=12, edgecolor='black')
#ax2.set_title("1980–2024 10Y Rolling window, inflation CH")
ax2.set_xlabel("Total wealth [% yearly income]")
ax2.set_ylabel("Frequency")
#ax2.set_xlim([0,8000])

median = np.median(realization)
p10 = np.percentile(realization, 10)
p90 = np.percentile(realization, 90)

ax2.axvline(median, color='red', linestyle='--', label=f'Median = {median:.2f}')
ax2.axvline(p10, color='green', linestyle=':', label=f'10th % = {p10:.2f}')
ax2.axvline(p90, color='blue', linestyle=':', label=f'90th % = {p90:.2f}')
ax2.legend()

plt.tight_layout()
plt.show()

#'''


###################################################
#''' historical data
###################################################
data = {
    "SP_capgain": historical_SP_capgain,
    "SP_total_yield": historical_SP_total_yield,
    "SP_div_yield": historical_SP_div_yield,
    "infl_CH": historical_inflation_CH,
    "infl_US": historical_inflation_US,
    "infl_IT": historical_inflation_IT,
}

plt.figure(figsize=(10, 12))

for i, (name, series) in enumerate(data.items(), 1):
    plt.subplot(3, 2, i)
    plt.hist(series, bins=10)
    plt.title(name)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 12))

for i, (name, series) in enumerate(data.items(), 1):
    plt.subplot(3, 2, i)
    plt.scatter(Year, series)
    plt.title(name)

plt.tight_layout()
plt.show()
#'''