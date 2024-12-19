from flask import Flask, request
from flask_restful import Resource, Api
from dao import DAO
import  re
app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')

api=Api(app)
dao = DAO()
address_pattern = re.compile(r'^(Via|Viale|Piazza|Corso|Largo)\s+[A-Za-z\s]+\d{1,4}(?:[a-zA-Z]?)$')
cap_regex = re.compile(r'^\d{5}$')
basePath = '/api/v1'

class UmarellResource(Resource):
    def get(self, idumarell):
        c=dao.getUmarell(idumarell)
        if c is None:
            return None, 404
        else:
            return c, 200

    def validate_umarell(self, data):
        for k in ['nome', 'cognome', 'cap']:
            if k not in data.keys():
                return False
            
        if not isinstance(data['nome'], (str)) or not isinstance(data['cognome'], (str)):
            return False
        if not cap_regex.match(f"{data['cap']}"):
            return False
        return True

        
    def post(self, idumarell):
        data=request.json
        print('got POST request' + str(data))
        if not self.validate_umarell(data):
            return None, 400
        if dao.getUmarell(idumarell) is not None:
            return None, 409
        dao.addUmarell(idumarell, data['nome'], data['cognome'], data['cap'])
        return data, 201
        
    def put(self, idumarell):
        # validate data
        data=request.json
        if not self.validate_umarell(data):
            return None, 400
        if dao.getUmarell(idumarell) is None:
            return None, 404
        dao.addUmarell(idumarell, data['nome'], data['cognome'], data['cap'])
        return None, 201

class CantiereResource(Resource):
    def get(self, idcantiere):
        c=dao.getCantiere(idcantiere)
        if c is None:
            return None, 404
        else:
            return c, 200

    def validate_cantiere(self, data):
        for k in ['indirizzo' , 'cap']:
            print(data.keys())
            if k not in data.keys():
                return False
        if not isinstance(data['indirizzo'], str) or not address_pattern.match(data['indirizzo']):
            return False
        if not cap_regex.match(f"{data['cap']}"):
            return False
        
        return True
        
    def post(self, idcantiere):
        data=request.json
        print('got POST request' + str(data))
        if not self.validate_cantiere(data):
            return None, 400
        if dao.getCantiere(idcantiere) is not None:
            return None, 409
        dao.addCantiere(idcantiere, data['indirizzo'], data['cap'])
        return data, 201
        
    def put(self, idcantiere):
        # validate data
        data=request.json
        if not self.validate_cantiere(data):
            return None, 400
        if dao.getCantiere(idcantiere) is None:
            return None, 404
        dao.addCantiere(idcantiere, data['indirizzo'], data['cap'])
        return None, 201
    
class CleanResource(Resource):
    def post(self):
        dao.clean()
        return None, 200
    
    def get(self):
        dao.clean()
        return None, 200

    
api.add_resource(UmarellResource, f'{basePath}/umarell/<int:idumarell>')
api.add_resource(CantiereResource, f'{basePath}/cantiere/<int:idcantiere>')
api.add_resource(CleanResource, f'{basePath}/clean')


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=8080, debug=True)