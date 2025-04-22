from math import log, sqrt, exp
from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np
from typing import Union
import math
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def black_scholes_price(S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type.lower() == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def calculate_implied_volatility(
    S: float, K: float, T: float, r: float, 
    market_price: float, option_type: str
) -> float:
    print(S, market_price)
    def objective_function(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price

    try:
        # Search in a reasonable range [1e-5, 5] (0.001% to 500% volatility)
        iv = brentq(objective_function, 1e-5, 5.0, maxiter=1000, xtol=1e-6)
        return iv
    except ValueError:
        print("Erroed")
        raise ValueError("Implied volatility not found in the range 0.00001 to 5.0")
    

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

def plot_graph(S, K, T, r, sigma, option_type='call', greek_type='delta', graph_x='spot'):
    N = norm.cdf
    N_prime = norm.pdf  # Probability Density Function
    if graph_x == 'strike':
        upper_limit = K * 1.5
        lower_limit = K / 2
        horizontal = np.linspace(lower_limit, upper_limit, 100)
        d1 = (np.log(S / horizontal) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)    
    elif graph_x == 'spot':
        upper_limit = S * 1.5
        lower_limit = S / 2
        horizontal = np.linspace(lower_limit, upper_limit, 100)
        d1 = (np.log(horizontal / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

    elif graph_x == 'rf':
        upper_limit = r * 2
        lower_limit = 0
        horizontal = np.linspace(lower_limit, upper_limit, 100)
        d1 = (np.log(S / K) + (horizontal + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
    else:
        upper_limit = sigma * 2
        lower_limit = 0.0001
        horizontal = np.linspace(lower_limit, upper_limit, 100)

        d1 = (np.log(S / K) + (r + 0.5 * horizontal ** 2) * T) / (horizontal * sqrt(T))
        d2 = d1 - horizontal * sqrt(T)



    if greek_type == 'delta':
        delta = N((d1)) if option_type == 'call' else N(d1) - 1
        print(delta.tolist())
        return {
            'horizontal': horizontal.tolist(),
            'data':  delta.tolist()
        }
    elif greek_type == 'gamma':
        gamma = N_prime(d1) / (S * sigma * sqrt(T))
        return {
            'horizontal': horizontal.tolist(),
            'data':  gamma.tolist()
        }
    elif greek_type == 'rho':
        # Rho (per 1% change in interest rate)
        if option_type == 'call':
            rho = (K * T * exp(-r * T) * N(d2)) * 0.01
        else:
            rho = (-K * T * exp(-r * T) * N(-d2)) * 0.01
        return {
            'horizontal': horizontal.tolist(),
            'data':  rho.tolist()
        }
    elif greek_type == 'theta':
        if option_type == 'call':
            theta = (-(S * N_prime(d1) * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * N(d2)) / 365
        else:
            theta = (-(S * N_prime(d1) * sigma) / (2 * sqrt(T)) + r * K * exp(-r * T) * N(-d2)) / 365
        return {
            'horizontal': horizontal.tolist(),
            'data':  theta.tolist()
        }
    else:
        vega = S * sqrt(T) * N_prime(d1) * 0.01  # Vega per 1% change in volatility
        return {
            'horizontal': horizontal.tolist(),
            'data':  vega.tolist()
        }
