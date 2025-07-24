from .auth import auth_bp

def init_routes(app):
    # auth.py: for login/register
    # orders.py: for order-related endpoints
    # items.py: for item-related endpoints
    app.register_blueprint(auth_bp)