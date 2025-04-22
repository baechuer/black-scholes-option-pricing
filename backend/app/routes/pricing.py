from flask import Blueprint, request, jsonify, abort
from app.models.option_models import *
from app.models.validate import black_scholes_input_validate
from app.routes.market import *
bp = Blueprint('pricing', __name__)

@bp.route("/option_price", methods=['POST', 'OPTIONS'])
def option_price():
    if request.method == 'OPTIONS':
        # Preflight request – return OK with headers
        return jsonify({'message': 'CORS preflight success'}), 200
    if not request.is_json:
        abort(400, description="Request must be in json format")
    data = request.get_json()

    required_fields = {
        'spot_price': (float, int),
        'strike': (float, int),
        'time_to_expiry': (float, int),
        'risk_free_rate': (float, int),
        'volatility': (float, int),
        'option_type': str
    }

    black_scholes_input_validate(required_fields, data)
    #Calculate
    price = black_scholes(
        data['spot_price'],
        data['strike'],
        data['time_to_expiry'],
        data['risk_free_rate'],
        data['volatility'],
        data['option_type']
    )
    return jsonify({'price': price})


@bp.route("/calc_greeks", methods=['POST', 'OPTIONS'])
def calc_greeks():
    if request.method == 'OPTIONS':
        # Preflight request – return OK with headers
        return jsonify({'message': 'CORS preflight success'}), 200
    
    if not request.is_json:
        abort(400, description="Request must be in json format")

    data = request.get_json()
    required_fields = {
        'spot_price': (float, int),
        'strike': (float, int),
        'time_to_expiry': (float, int),
        'risk_free_rate': (float, int),
        'volatility': (float, int),
    }

    black_scholes_input_validate(required_fields, data)
    return jsonify(calculate_greeks(
        data['spot_price'],
        data['strike'],
        data['time_to_expiry'],
        data['risk_free_rate'],
        data['volatility'],
        data['option_type']
    ))


@bp.route("/greeks-chart", methods=['POST', 'OPTIONS'])
def greeks_chart():
    if request.method == 'OPTIONS':
        # Preflight request – return OK with headers
        return jsonify({'message': 'CORS preflight success'}), 200
    
    if not request.is_json:
        abort(400, description="Request must be in json format")

    data = request.get_json()
    required_fields = {
        'spot_price': (float, int),
        'strike': (float, int),
        'time_to_expiry': (float, int),
        'risk_free_rate': (float, int),
        'volatility': (float, int),
        'option_type': str,
        'greek_type': str,
        'graph_x': str
    }
    black_scholes_input_validate(required_fields, data)

    return jsonify(plot_graph(
        data['spot_price'],
        data['strike'],
        data['time_to_expiry'],
        data['risk_free_rate'],
        data['volatility'],
        data['option_type'],
        data['greek_type'],
        data['graph_x']
    ))
