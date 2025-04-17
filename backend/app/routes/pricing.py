from flask import Blueprint, request, jsonify, abort
from app.models.option_models import black_scholes

bp = Blueprint('pricing', __name__)

@bp.route("/option_price", methods=['POST', 'OPTIONS'])
def option_price():
    if request.method == 'OPTIONS':
        # Preflight request – return OK with headers
        return jsonify({'message': 'CORS preflight success'}), 200
    if not request.is_json:
        abort(400, description="Request must be in json format")
    data = request.get_json()
    print(data)
    required_fields = {
        'spot_price': (float, int),
        'strike': (float, int),
        'time_to_expiry': (float, int),
        'risk_free_rate': (float, int),
        'volatility': (float, int),
        'option_type': str
    }

    for field, types in required_fields.items():
        if field not in data:
            abort(400, description=f"Missing required field: {field}")
        if not isinstance(data[field], types):
            abort(400, description=f"Field {field} is not in format")

    # Validate numerical ranges
    if data['spot_price'] <= 0:
        abort(400, description="Spot price must be positive")
    if data['strike'] <= 0:
        abort(400, description="Strike price must be positive")
    if data['time_to_expiry'] <= 0:
        abort(400, description="Time to expiry must be positive")
    if data['volatility'] <= 0:
        abort(400, description="Volatility must be positive")
    if data['option_type'] not in ['call', 'put']:
        abort(400, description="Option can only be call and put")

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