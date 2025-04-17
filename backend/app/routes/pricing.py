from flask import Blueprint, request, jsonify
from app.models.option_models import black_scholes

bp = Blueprint('pricing', __name__)

