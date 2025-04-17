# Black-Scholes Option Pricing API

A modular Flask backend implementing the Black-Scholes model for option pricing, with market data integration and clean Blueprint architecture.

## Features

- 🚀 **RESTful API** with proper endpoint versioning
- 📊 **Black-Scholes pricing** for European options
- 📈 **Market data integration** via Yahoo Finance API
- 🔒 **Blueprint architecture** for scalable route management
- 🌐 **CORS support** for frontend integration
- ⚙️ **Configuration management** with environment variables

## Project Structure
backend/
├── app/
│ ├── init.py # Flask app factory
│ ├── routes/ # All API endpoints
│ │ ├── init.py # Blueprint registry
│ │ ├── pricing.py # Option pricing routes
│ │ ├── market.py # Market data routes
│ │ └── auth.py # Authentication routes
│ ├── models/ # Business logic
│ │ ├── init.py
│ │ └── option_models.py # Pricing calculations
│ ├── static/ # Static files
│ ├── templates/ # Jinja templates
│ └── config.py # App configuration
├── tests/ # Unit/integration tests
├── requirements.txt # Python dependencies
└── run.py # Application entry point

### Installation
Clone the repository:
- git clone https://github.com/yourusername/option-pricing-api.git
- cd option-pricing-api/backend

### Create and activate virtual environment:
- python -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate     # Windows

### Install dependencies:
pip install -r requirements.txt

### Running the Application
python run.py