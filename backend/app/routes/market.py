from flask import Blueprint, request, jsonify, abort
import yfinance as yf
from app.models.option_models import calculate_implied_volatility
bp = Blueprint('market', __name__)
import datetime

from scipy.stats import norm
from scipy.optimize import brentq
import math
@bp.route('volatility_smile_by_ticket', methods=['POST'])
def get_volatility_smile_by_ticker():
    if request.method == 'OPTIONS':
        # Preflight request – return OK with headers
        return jsonify({'message': 'CORS preflight success'}), 200
    
    if not request.is_json:
        abort(400, description="Request must be in json format")
    
    data = request.get_json()
    ticker = data['ticket']
    risk_free_rate = float(data['risk_free_rate'])
    try:
        stock = yf.Ticker(ticker)
        option_dates = stock.options
        expiry = option_dates[0]  # Use nearest expiry

        opt_chain = stock.option_chain(expiry)
        calls = opt_chain.calls
        puts = opt_chain.puts

        # Current stock price
        spot_price = stock.history(period='1d')['Close'].iloc[-1]
        
        # Time to expiry in years
        expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d")

        today = datetime.datetime.now()
        T = (expiry_date - today).days / 365.0

        def bs_price(S, K, T, r, sigma, option_type):
            d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
            d2 = d1 - sigma * math.sqrt(T)
            if option_type == 'call':
                return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
            else:
                return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        def implied_volatility(market_price, S, K, T, r, option_type):
            try:
                return brentq(
                    lambda sigma: bs_price(S, K, T, r, sigma, option_type) - market_price,
                    1e-5, 5.0, maxiter=500, xtol=1e-6
                )
            except ValueError:
                return None

        result = {
            "call_data": [],
            "put_data": [],
            "spot_price": spot_price
        }
        for _, row in calls.iterrows():
            K = row['strike']
            price = row['lastPrice']
            iv = implied_volatility(price, spot_price, K, T, risk_free_rate, 'call')
            if iv is not None:
                result["call_data"].append({"strike": K, "implied_vol": iv})

        for _, row in puts.iterrows():
            K = row['strike']
            price = row['lastPrice']
            iv = implied_volatility(price, spot_price, K, T, risk_free_rate, 'put')
            if iv is not None:
                result["put_data"].append({"strike": K, "implied_vol": iv})
        return jsonify(result), 200

    except Exception as e:
        abort(500, description=f"Failed to process ticker {ticker}: {str(e)}")