# DEFINISCO QUI LE RISORSE PER DIVIDERE LE INTERFACCE 
from flask import Flask, request
from flask_restful import Resource
from dao import DAO
import json, re
dao = DAO()

# L’applicazione deve esporre le seguenti funzionalità tramite opportune Web API
# RESTful:
# 1. inviando richieste POST allo URI /api/v1/chirps/ è possibile inserire un
# nuovo messaggio
# 2. inviando richieste GET allo URI /api/v1/chirps/{id} è possibile leggere
# un messaggio
# 3. inviando richieste POST allo URI /api/v1/clean è possibile cancellare i
# dati memorizzati nel database


# definitions:
#   Chirp:
#     type: object
#     required:
#       - id
#       - message
#       - timestamp
#     properties:
#       id:
#         type: string
#         example: "msgid1"
#       message:
#         type: string
#         example: "A New chirp with #hashtag1,#hastag2"
#       timestamp:
#         type: string
#         format: timestamp # YYYY-MM-DD HH:mm:S
#         example: "2023-02-01 13:00:01"

# /chirps/{id}:
#     parameters:
#       - name: id
#         in: path
#         required: true
#         description: "Document id of the chirp"
#         type: string
#     get:
#       description: "Get info of the selected chirp"
#       operationId: "GetChirp"
#       responses:
#         200:
#           description: "Return the details of the selected Chirp"
#           schema:
#             $ref: "#/definitions/Chirp"
#         404:
#           description: "Not found"

def validate_input(data):

    if data is None:
        return False
    
    if not isinstance(data.get("id"), (str)) or data["id"] is None: 
        return False
    
    if  data["message"] is None or (isinstance(data["message"], (str)) and (len(data['message'])<=100 and len(data['message'])>0 )) is False:
        return False
    
    if data["timestamp"] is None or not isinstance(data["timestamp"], (str)) : 
        return False

    return True

class Chirp(Resource): 

    def validate_input(self, data):

        if data is None:
            return False
                
        if  not 1<=len(data)<=100:
            return False
        
        return True

    def post(self): 
        # POSTO UN MESSAGGIO TRAMITE UNA RICHIESTA JSON 
        data = request.json
        print(f"Valore di Data --> {data}")
        if self.validate_input(data) is False:
            return None, 400
        data = dao.postMessage(data)
        return data, 200

class Chirps(Resource): 
    def get(self, id): 
        data = dao.getChirpByID(id)
        if data is None: 
            return None, 404
        return data

class Clean(Resource): 
    def post(self): 
        dao.deleteAll()
        return None, 200


#   ChirpList:
#     type: array
#     items:
#       type: string
#     example: ["msgid1", "msgid2"]