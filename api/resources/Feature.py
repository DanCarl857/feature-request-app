from flask import request
from flask_restful import Resource
from Model import db, Feature, FeatureSchema

features_schema = FeatureSchema(many=True)
feature_schema = FeatureSchema()

class FeatureResource(Resource):
    def get(self):
       features = Feature.query.all()
       features = features_schema.dump(features).data
       return {'status': 'Successfully gotten features', 'data': features}, 200 

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data: 
            return {'message': 'No payload provided'}, 400

        # Validate and deserialize input
        data, errors = feature_schema.load(json_data)
        if errors: 
            return errors, 422
        feature = Feature.query.filter_by(name=data['title']).first()
        if feature:
            return {'message': 'Feature request already exists'}, 400
        feature = Feature(name=json_data['title'])

        db.session.add(feature)
        db.session.commit()

        response = feature_schema.dump(feature).data
        return { 'status': 'Feature request created', 'data': response }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No payload provided'}, 400
        
        data, errors = feature_schema.load(json_data)
        if errors: 
            return errors, 422
        feature = Feature.query.filter_by(id=data['title']).first()
        if not feature:
            return {'message': 'Feature does not exist'}, 400
        feature.name = data['title']
        db.session.commit()

        response = feature_schema.dump(feature).data
        return { 'status': 'Feature request updated', 'data': response }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No payload provided'}, 400
        
        data, errors = feature_schema.load(json_data)
        if errors:
            return errors, 422
        feature = Feature.query.filter_by(id=data['id']).delete()
        db.session.commit()

        response = feature_schema.dump(category).data

        return { "status": 'Feature request deleted', 'data': response}, 204