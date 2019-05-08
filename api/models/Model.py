from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()

class Feature(db.Model):
    __tablename__ = "features"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    # Making this not nullable as we won't want a feature with no description
    description = db.Column(db.String(1000), nullable=False)
    client = db.Column(db.String, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    product_area = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Feature {}>'.format(self.title)

class FeatureSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True, validate=validate.Length(1))
    client = fields.String(required=True)
    target_date = fields.Date(required=True)
    product_area = fields.String(required=True)
    priority = fields.Integer(required=True)