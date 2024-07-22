from .auth import auth_bp
from .users import users_bp
from .listings import listings_bp
from .rating import rating_bp
from .review import review_bp
from .search import search_bp
from .recommendations import recommendations_bp
from .chats import chats_bp
from .messages import messages_bp
from .charity import charity_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(listings_bp, url_prefix='/listings')
    app.register_blueprint(rating_bp, url_prefix='/rating')
    app.register_blueprint(review_bp, url_prefix='/review')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(recommendations_bp, url_prefix='/recommendations')
    app.register_blueprint(chats_bp, url_prefix='/chats')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(charity_bp, url_prefix='/charity')