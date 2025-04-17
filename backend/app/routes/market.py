from flask import Blueprint, jsonify
import yfinance as yf

bp = Blueprint('market', __name__)

