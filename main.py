from flask import Flask, Blueprint
from flask_cors import CORS

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    return app
# CORS(create_app)

# if __name__ == "__main__":
#     app.run(debug=True)

#TODO: Add admission date, paid fees and age in get_student.