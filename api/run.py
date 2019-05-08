import os
from flask import Flask
from flask_cors import CORS

def create_app(config_filename, test_config=None):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Add CORS support to API
    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from models.Model import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)