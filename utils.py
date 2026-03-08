import numpy as np
from typing import List, Dict
import sys
import matplotlib.pyplot as plt


VD_tax_w_brackets = [
    (0, 0.00024),
    (20000, 0.00035),
    (40000, 0.00050),
    (60000, 0.00070),
    (80000, 0.00097),
    (100000, 0.00115),
    (150000, 0.00145),
    (200000, 0.00175),
    (300000, 0.00210),
    (400000, 0.00230),
    (600000, 0.00260),
    (800000, 0.00285),
    (1000000, 0.00300),
    (1500000, 0.00315),
    (2000000, 0.00325),
    (3000000, 0.00330),
    (4000000, 0.00333),
    (6000000, 0.00336),
    (8000000, 0.00338),
    (10000000, 0.00339),
]

# ===============================
# ---- FUNCTION DEFINITIONS -----
# ===============================
# rates, taxes, and inflation, are all in percentage (3, not 0.03)


def real_rate(
    cg: float, dg: float, i: float, tax_div: float, tax_cg: float, tax_w: float
) -> float:
    """Real annual rate (given directly from spreadsheet)"""
    gross = dg * (1 - tax_div / 100) + cg * (1 - tax_cg / 100) - tax_w
    return ((1 + gross / 100) / (1 + i / 100) - 1) 


def value_initial_investment(W0: float, r_real: float) -> float:
    """Wealth from initial capital, monthly compounding"""
    return W0 * (1 + r_real ) 


def value_monthly_investments(P: float, r_real: float) -> float:
    """Wealth from monthly savings after a year"""
    r_m = yearly_to_monthly_compounding(r_real)
    if r_m != 0:
        res =  P * (((1 + r_m ) ** 12) - 1)/r_m
    else:
        res = 12*P
    return res


def yearly_to_monthly_compounding(r_yearly: float) -> float:
    """Converts yearly returns to monthly"""
    return (
        (1+r_yearly)**(1/12)-1
    )


def ROI_13th_salary(S13: float, r_real: float, num_years: int) -> float:
    """Wealth from yearly 13th salary, monthly compounding with payments at the end of the year"""
    nominal_return = (1 + r_real / 100) ** (1 / 12) - 1
    return (
        S13
        * ((1 + nominal_return) ** (12 * num_years) - 1)
        / ((1 + nominal_return) ** 12 - 1)
    )


def total_wealth(
    W0: float, S: float, S13: float, r_real: float
) -> float:
    """total accumulated wealth"""
    return (
        value_initial_investment(W0, r_real)
        + value_monthly_investments(S, r_real)
        + S13
    )


def calculate_tax_w(total_wealth: float, tax_w_brackets):
    """Return wealth tax rate (fraction, not %) for given total wealth in Vaud."""
    rate = tax_w_brackets[0][1]
    for threshold, r in tax_w_brackets:
        if total_wealth > threshold:
            rate = r
        else:
            break
    return 100 * rate


def make_time_series(N, stats):
    """
    Generate N random values bounded by min and max with given mean and std.
    stats = [mean, std, min, max]
    """
    mean, std, minv, maxv = stats
    values = np.random.normal(mean, std, N)
    # # truncate
    # values = np.clip(values, minv, maxv)
    return values


def stats_tot(data):
    """
    Return [mean, std, min, max] for a list of numbers.
    """
    data = np.array(data, dtype=float)
    return [np.mean(data), np.std(data, ddof=1), np.min(data), np.max(data)]


# ===============================
# ---- MAIN LOOP ----------------
# ===============================
def simulate(
    N: int,                 # Number of years
    inflation: List[float], # NOMINAL Inflation over the years
    cg: List[float],        # NOMINAL Capital Gains o.t.y
    dg: List[float],        # NOMINAL Dividend Gains o.t.y
    W0: float,              # Initial Wealth
    S: List[float],         # Yearly Salary o.t.y
    S13: List[float],       # 13th Salary o.t.y
    tax_div: float,         # dividend tax brackets
    tax_cg: float,          # capital gain tax brackets
) -> float:
    """Loop over years and compute results"""

    results = [0] * (N + 1)
    results[0] = W0

    for t in range(0, N):
        tax_w = calculate_tax_w(results[t], VD_tax_w_brackets)
        r_real = real_rate(cg[t], dg[t], inflation[t], tax_div, tax_cg, tax_w)
        results[t + 1] = total_wealth(results[t], S[t], S13[t], r_real)

    return results



def wrapper(
        N: int,                     # Window length
        yearly_salary: float,       # yearly salary
        month_perc_savings: float,  # percentage of monthly or yearly savings
        nr_y_s: float,              # amount of yearly salarys to start
        Bonus: float,               # end of year bonus or 13th installment
        country: str,               # country (for taxes and inflation)
        plot: bool                  # do you want the plots?
        ):

    Year = list(range(1980, 2025 ))

    # from: https://www.slickcharts.com/sp500/returns/details
    historical_SP_capgain = [25.77, -9.73, 14.76, 17.27, 1.40, 26.33, 14.62, 2.03, 12.40, 27.25, -6.56, 26.31, 4.46, 7.06, -1.54, 34.11, 20.26, 31.01, 26.67, 19.53, -10.14, -13.04, -23.37, 26.38, 8.99, 3.00, 13.62, 3.53, -38.49, 23.45, 12.78, -0.00, 13.41, 29.60, 11.39, -0.73, 9.54, 19.42, -6.24, 28.88, 16.26, 26.89, -19.44, 24.23, 23.31]
    historical_SP_div_yield = [6.65, 4.82, 6.79, 5.29, 4.87, 5.40, 4.05, 3.22, 4.21, 4.44, 3.46, 4.16, 3.16, 3.02, 2.86, 3.47, 2.70, 2.35, 1.91, 1.51, 1.04, 1.15, 1.27, 2.30, 1.89, 1.91, 2.17, 1.96, 1.49, 3.01, 3.01, 2.28, 2.79, 2.79, 2.30, 2.11, 2.42, 2.41, 1.86, 2.61, 2.14, 1.82, 1.33, 2.06, 1.71]
    historical_SP_total_yield = [32.42, -4.91, 21.55, 22.56, 6.27, 31.73, 18.67, 5.25, 16.61, 31.69, -3.10, 30.47, 7.62, 10.08, 1.32, 37.58, 22.96, 33.36, 28.58, 21.04, -9.10, -11.89, -22.10, 28.68, 10.88, 4.91, 15.79, 5.49, -37.00, 26.46, 15.06, 1.38, 16.00, 32.39, 13.69, 1.36, 11.96, 21.83, -4.38, 31.49, 18.40, 28.71, -18.11, 26.29, 25.02]
    # from: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2024&locations=CH&start=1980&utm_source=chatgpt.com
    historical_inflation_CH = [4.022501, 6.49031, 5.655102, 2.949794, 2.931457, 3.435399, 0.75031, 1.440322, 1.872469, 3.158297, 5.403296, 5.862305, 4.043857, 3.293556, 0.846679, 1.799073, 0.809836, 0.519012, 0.023674, 0.810207, 1.556525, 0.993705, 0.640208, 0.639134, 0.795145, 1.169042, 1.057531, 0.725732, 2.428207, -0.479697, 0.692359, 0.22999, -0.6876, -0.220196, -0.014411, -1.143909, -0.434619, 0.533788, 0.936335, 0.362886, -0.725875, 0.581814, 2.835028, 2.135401, 1.06234]
    historical_inflation_IT = [21.064168, 17.969299, 16.480415, 14.646577, 10.794496, 9.205991, 5.823547, 4.747285, 5.058247, 6.263654, 6.497099, 6.196416, 5.30431, 4.668349, 4.056104, 5.300492, 3.976029, 1.965913, 1.985009, 1.707662, 2.540394, 2.707384, 2.478374, 2.724932, 2.192028, 1.873754, 2.136789, 1.819951, 3.290849, 0.794177, 1.45353, 2.737964, 3.00866, 1.247937, 0.242814, 0.03879, -0.094017, 1.226533, 1.137488, 0.611247, -0.137708, 1.873783, 8.20129, 5.622194, 0.982373]
    historical_inflation_US = [13.549202, 10.334715, 6.131427, 3.212435, 4.300535, 3.545644, 1.898048, 3.664563, 4.077741, 4.830557, 5.399547, 4.191931, 3.007945, 2.986976, 2.607531, 2.752342, 3.022415, 2.266706, 1.559073, 2.191274, 3.387632, 2.826065, 1.59082, 2.270747, 2.676444, 3.391277, 3.226346, 2.826363, 3.839128, -0.355857, 1.640909, 3.160993, 2.069306, 1.46481, 1.622278, 0.118627, 1.261583, 2.13011, 2.442583, 1.81221, 1.233584, 4.697859, 8.0028, 4.116338, 2.949525]

    W0      = yearly_salary * nr_y_s                    # Initial investment
    S13     = [Bonus]*N                                 # Once a year investment
    Net_S   = [month_perc_savings*yearly_salary/12]*N   # Monthly investment
    if country=='Switzerland':
        tax_cg = 0                                          # Capital gain tax
        tax_dg = 30                                         # dividend gain tax
        historical_inflation = historical_inflation_CH
    else:
        print('Undefined country parameters')
        sys.exit(1)
        
    realization = [0]*(len(Year)-N)
    endowment = [0]*(len(Year)-N)
    if plot:
        plt.figure(figsize=(10, 12))

    for ii in range(0,len(Year)-N):
        cg = historical_SP_capgain[ii:(ii+N)]
        dg = historical_SP_div_yield[ii:(ii+N)]
        inflation = historical_inflation[ii:(ii+N)]

        # ===============================
        Total_wealth = simulate(N,inflation,cg,dg,W0,Net_S,S13,tax_dg,tax_cg)
        # ===============================
        endowment[ii] = 0.04*Total_wealth[-1]/12
        realization[ii] = Total_wealth[-1]

        if plot:
            plt.plot(range(10), Total_wealth[1:11],color='black')
            plt.title("Total Wealth year by year")
            plt.xlabel("Year")
            plt.ylabel("Total Wealth [% yearly salary]")

    if plot:
        plt.show()

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
        # '''


        ###################################################
        #''' starting year dependence
        ###################################################
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





    return realization