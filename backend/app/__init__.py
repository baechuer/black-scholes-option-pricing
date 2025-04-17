from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Initialize extensions (e.g., SQLAlchemy, LoginManager)
    # db.init_app(app)
    # login_manager.init_app(app)

    # Register blueprints
    from app.routes import pricing_bp, market_bp, auth_bp
    app.register_blueprint(pricing_bp, url_prefix='/api/pricing')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app