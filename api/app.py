from flask import Blueprint
from flask_restful import Api
from resources.Feature import FeatureResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(FeatureResource, '/feature')