#
# Created by OFShare on 2020-03-27
#

import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='form')

class HelloWorld(Resource):
    def get(self):
        print("receive get...")
        return {'hello': 'world'}

    def post(self):
        print("receive post...")
        args = reqparse.parse_args()
        name = args['name']
        return "hello " + name + " " + str(datetime.date.today())
        
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, port=8123)