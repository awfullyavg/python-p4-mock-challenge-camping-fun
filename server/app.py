#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Campers(Resource):
    #GET method
    def get(self):
        # # campers_list = []
        # campers_list = [camper.to_dict() for camper in Campers.query.all()]
        # # for campers in Campers.query.all():
        # #     campers_list.append(campers.to_dict())
        # #Maybe return
        # response = make_response(campers_list, 200)
        # return response
        try:
            campers = Camper.query.all()
            # campers = [ c.to_dict( only=("id", "name", "age")) for c in Camper.query.all()  ]
            new_campers = []
            for c in campers:
                new_campers.append(c.to_dict(only=("id", "name", "age")))            
            return new_campers, 200

        except: 
            return {"error": "Bad request"}, 400
api.add_resource(Campers, '/campers')

class Campers_Id(Resource):
    def get(self, id):
        try:
            camper = Camper.query.filter(Camper.id == id).first()
            return camper.to_dict(only=("id", "name", "age")), 200
        
        except:
            return {"error": "Bad request"}, 404
api.add_resource(Campers_Id, '/campers/<int:id>')
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
