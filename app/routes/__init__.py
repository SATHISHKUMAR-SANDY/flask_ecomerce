from flask import Blueprint

# Import all blueprints
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.cart_routes import cart_bp
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.cart_routes import cart_bp
from app.routes.main_routes import main_bp

# Optionally, you can create a main blueprint (if needed)
main_bp = Blueprint('main', __name__)

# Now you can import these in app/__init__.py and register all blueprints at once
