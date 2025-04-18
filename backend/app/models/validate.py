from flask import abort

def black_scholes_input_validate(required_fields, data):
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
