import numpy as np
from typing import List, Dict


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

    print('Hello')
    print(res)
    print(r_real)
    print(r_m)

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
    inflation: List[float], # NOMINAML Inflation over the years
    cg: List[float],        # NOMINAML Capital Gains o.t.y
    dg: List[float],        # NOMINAML Dividend Gains o.t.y
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
