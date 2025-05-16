# IMPORT NECESSARIE PER IMPLEMENTARE L'API 

import re
from flask import Flask, request
from flask_restful import Resource, Api
from dao import DAO

# A seconda del numero di risorse specificate nel .yaml si generano le classi di conseguenza --> solitamente in fondo e identificate dal campo "object"
dao = DAO()
nome_pattern = re.compile(r'^[a-zA-Z]+$')
email_pattern = re.compile(r'^[a-zA-Z0-9._%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$')

# # L’applicazione deve esporre le seguenti funzionalità tramite opportune Web API
# RESTful:
# •inviando richieste POST allo URI /api/v1/santa/{email} è possibile is-
# criversi al secret santa
# •inviando richieste GET allo URI /api/v1/santa/{email} è possibile ot-
# tenere l’indicazione del destinatario del proprio regalo
# La lista degli accoppiamenti fornisce a ciascun partecipante il nome successivo
# nell’elenco dei partecipanti (compilato in ordine cronologico con le iscrizioni), a
# parte l’ultimo che riceve i dati del primo partecipante.
# Nel caso di errori, si chiede ritornare un oggetti JSON con un campo message
# contiene la descrizione dell’errore come indicata nella specifica OpenAPI


""" SantaParticpant:
    type: object
    required:
      - firstName
      - lastName
    properties:
      firstName: 
        type: string
      lastName: 
        type: string
    example:
      firstName: "Riccardo"
      lastName: "Lancellotti"
      """

class Santa(Resource):
    # ti iscrivi al secret santa
    def post(self, email):
        data = request.json
        # bisogna validare i dati 

        for k in ["firstName", "lastName"]: 
            if k not in data.keys(): 
                return {"message": "Generic error"}, 400


        if not isinstance(data["firstName"], (str)) or not nome_pattern.match(f"{data['firstName']}"):
            return {"message": "Generic error"}, 400
        
        if not isinstance(data["lastName"], (str)) or not nome_pattern.match(f"{data['lastName']}"):
            return {"message": "Generic error"}, 400
        
        if not isinstance(email, (str)) or not email_pattern.match(email):
            return {"message": "Generic error"}, 400
        
        if dao.get(email): 
            return {"message": "Conflict"}, 409
        
        dao.post(email, data)
        return data, 201
    
    def get(self, email):

        if not isinstance(email, (str)) or not email_pattern.match(email):
            return {"message": "Generic error"}, 400
        
        if dao.get(email) is None: 
            return {"message": "Not Found"}, 404
        
        data = dao.getDestinatario(email)      
        
        return data, 200

class Clean(Resource):
    def get(self): 
        dao.clean()
        return  None, 200