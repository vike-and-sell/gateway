from .auth import auth_bp
from .users import user_bp
from .listings import listings_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(listings_bp, url_prefix='/listings')