from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class EplHome(Resource):
    def get(self):
        with open('table.json','r') as f:
            return json.load(f)

class EplTable(Resource):
    def get(self):
        with open('table.json','r') as f:
            return json.load(f)

class EplPasses(Resource):
    def get(self):
        with open('mostpasses.json') as f:
            return json.load(f)

class EplAssists(Resource):
    def get(self):
        with open('topassists.json') as f:
            return json.load(f)

class EplScorers(Resource):
    def get(self):
        with open('topscorer.json') as f:
            return json.load(f)
            

api.add_resource(EplHome, '/')
api.add_resource(EplTable, '/epl_table')
api.add_resource(EplPasses, '/epl_passes')
api.add_resource(EplAssists, '/epl_assists')
api.add_resource(EplScorers, '/epl_scorers')

if __name__ == '__main__':
    app.run(debug=True)
