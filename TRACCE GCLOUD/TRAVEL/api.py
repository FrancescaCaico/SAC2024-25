# IMPORT NECESSARIE PER IMPLEMENTARE L'API 

import re
from flask import Flask, request
from flask_restful import Resource, Api
from dao import DAO
from datetime import datetime 
import uuid

app = Flask(__name__,static_url_path='/static',static_folder='static')
api=Api(app)
dao = DAO()

# SI INSERISCE IL BASE PATH SPECIFICATO NEL .YAML DELLA CONFIGURAZIONE ( SOLITAMENTE DATA DAL PROF )
basePath = "/api/v1"
nome =  re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

# L’applicazione deve esporre le seguenti funzionalità tramite opportune Web API RESTful:
# 1. inviando richieste POST allo URI /api/v1/travel/{user}/{date} è possibile registrare un itinerario di viaggio
# per l’utente indicato nella data indicata;
# 2. inviando richieste GET allo URI specificato in precendeza è possibile ottenere le informazioni riguardanti
# l’itinerario di viaggio
# # A seconda del numero di risorse specificate nel .yaml si generano le classi di conseguenza --> solitamente in fondo e identificate dal campo "object"

class TravelDetails(Resource):
    def validate_inputs(self, user, date, data): 
        if not isinstance(user, (str)) or not nome.match(str(user)):
            return False
        try:
            print(f"PROVA DELLA DATA {date}")
            date = datetime.strptime(date, "%Y-%m-%d")
        except: 
            print("lA DATA NON VA BENE")
            return False
        
        for k in ["from", "to"]:
            if k not in data.keys(): 
                print("Non ci sono le label")
                return False

        if len(data["from"]) != 3 or len(data["to"]) !=3: 
            return False
        return True

    def post(self, user, date):
       data = request.json 
       print(data)
       print("Entrata nella post")
       if self.validate_inputs(user, date, data) is False:
           return None, 400
       
       if dao.getTravel(user,date) is not None: 
           print("C'È GIA")
           return None, 409
       print('NON CE')
       d = dao.postTravel(user, date, data)
       return d, 201
    
    def get(self, user, date):

        if not isinstance(user, (str)) or nome.match(str(user)):
            return None, 400
        try:
            date = datetime.strptime(date)
        except: 
            return None, 400

        if dao.getTravel(user, date) is None: 
            return 404, None
        
        return dao.getTravel(user, date), 200

class CommonTravels(Resource): 
    def get(self, user):
        print(f"{user}")
        if not isinstance(user, (str)) or not nome.match(str(user)):
            return None, 400
        
        d = dao.getCommonUsersTravel(user, 0)
        if d is None: 
            return None, 404
        
        return d
