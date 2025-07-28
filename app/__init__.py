from flask import Flask
from flask_cors import CORS
from . import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    db.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app