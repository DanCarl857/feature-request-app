from flask import Flask
from flask_cors import CORS

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Add CORS support to API
    CORS(app)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from Model import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)