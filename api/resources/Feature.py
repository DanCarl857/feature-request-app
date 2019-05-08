from flask import request
from flask_restful import Resource
from models.Model import db, Feature, FeatureSchema

features_schema = FeatureSchema(many=True)
feature_schema = FeatureSchema()

class FeatureResources(Resource):
    def get(self):
       features = Feature.query.all()
       features = features_schema.dump(features).data
       return {'status': 'Successfully gotten features', 'data': features}, 200 

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data: 
            return {'message': 'No payload provided'}, 400

        print(json_data)
        # Validate and deserialize input
        data, errors = feature_schema.load(json_data)
        print(errors)
        print(data)
        if errors: 
            return errors, 422
        feature = Feature.query.filter_by(title=data['title']).first()
        if feature:
            return {'message': 'Feature request already exists'}, 400

        title = data['title']
        description = data['description']
        client = data['client']
        target_date = data['target_date']
        product_area = data['product_area']
        priority = data['priority']

        if title and description and client and target_date and product_area and priority and priority > 0:
            new_feature = Feature(
                title=title,
                description=description,
                client=client,
                target_date=target_date,
                product_area=product_area,
                priority=priority
            )

            all_client_features = Feature.query.filter_by(client=client).order_by(Feature.priority).all()
            all_client_features.insert(new_feature.priority - 1, new_feature)
            for index, feature in enumerate(all_client_features, 1):
                feature.priority = index

            db.session.add(new_feature)
            db.session.commit()

            response = feature_schema.dump(new_feature).data
            return {'status': 'Successfully created feature request', 'data': response}, 201
        else:
            return {'message', 'Some fields are either missing or invalid.'}, 400

    def put(self):
        json_data = request.get_json(force=True)
        print(json_data)
        if not json_data:
            return {'message': 'No payload provided'}, 400
        
        data, errors = feature_schema.load(json_data)
        if errors: 
            return errors, 422
        feature = Feature.query.filter_by(id=data['id']).first()
        print(feature)
        if not feature:
            return {'message': 'Feature does not exist'}, 404
        feature.title = data['title']
        feature.description = data['description']
        feature.client = data['client']
        feature.product_area = data['product_area']
        feature.priority = data['priority']
        feature.target_date = data['target_date']
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

class FeatureResource(Resource):
    def get(self, id):
        feature = Feature.query.get(id)
        if not feature:
            return {'message': 'No feature request exists with that ID'}, 404

        response = feature_schema.dump(feature).data
        return {'status': 'Successfully retrieved feature request', 'data': response}, 200

    def delete(self, id):
        feature = Feature.query.get(id)
        if not feature:
            return {'message': 'Feature does not exist'}, 404

        db.session.delete(feature)
        db.session.commit()
        return {'message': 'Deleted'}, 204