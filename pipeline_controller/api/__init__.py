from flask import Flask
from api.routes import api
from flask_cors import CORS  #
def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(api, url_prefix="/api")

    return app
