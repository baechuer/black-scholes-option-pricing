from math import log, sqrt, exp
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    # Standard Normal PDF and CDF
    N = norm.cdf  # Cumulative Distribution Function
    N_prime = norm.pdf  # Probability Density Function

    # Greeks
    delta = N(d1) if option_type == 'call' else N(d1) - 1
    gamma = N_prime(d1) / (S * sigma * sqrt(T))
    vega = S * sqrt(T) * N_prime(d1) * 0.01  # Vega per 1% change in volatility
    # Theta (per day)
    theta_call = (-(S * N_prime(d1) * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * N(d2)) / 365
    theta_put = (-(S * N_prime(d1) * sigma) / (2 * sqrt(T)) + r * K * exp(-r * T) * N(-d2)) / 365
    theta = theta_call if option_type == 'call' else theta_put

    # Rho (per 1% change in interest rate)
    rho_call = (K * T * exp(-r * T) * N(d2)) * 0.01
    rho_put = (-K * T * exp(-r * T) * N(-d2)) * 0.01
    rho = rho_call if option_type == 'call' else rho_put
    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,  # Daily time decay
        'rho': rho    
    }