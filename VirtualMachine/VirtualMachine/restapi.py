from distutils.command.build_scripts import first_line_re
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Aircrafts(Resource):
    
    def get(self):
        data = pd.read_csv('aircrafts.csv')  
        data = data.sort_values(by= 'category')
        data = data.to_dict()  
        return {'data': data}, 200
    

    def post(self):

        category = request.args['category']
        serialNo = request.args['serialNo']
        country = request.args['country']
        
        new_data = pd.DataFrame({
            'category': [category],
            'serialNo': [serialNo],
            'country': [country],
            'firstFlight': [[]]
        })
        
        data = pd.read_csv('aircrafts.csv')
        
        data = data.append(new_data, ignore_index=True)
        data = data.sort_values(by= 'category')
        
        data.to_csv('aircrafts.csv', index=False)
        
        return {'data': data.to_dict()}, 200  


    def put(self):
        
        category = request.args['category']
        firstFlight = request.args['firstFlight']
        
        data = pd.read_csv('aircrafts.csv')
        
        if category in list(data['category']):
            
            data['firstFlight'] = data['firstFlight'].apply(
                lambda x: ast.literal_eval(x)
            )
            
            aircraft_data = data[data['category'] == category]

            
            aircraft_data['firstFlight'] = aircraft_data['firstFlight'].values[0] \
                .append(firstFlight)
            
            data.to_csv('aircrafts.csv', index=False)
            
            return {'data': data.to_dict()}, 200

        else:
            
            return {
                'message': f"'{category}' user not found."
            }, 404


    def delete(self):
        category = request.args['category']
        data = pd.read_csv('aircrafts.csv')
        data = data[data['category'] != category]

        data.to_csv('aircrafts.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200




api.add_resource(Aircrafts, '/aircrafts')  

if __name__ == '__main__':
    app.run()  

