# DEFINISCO QUI LE RISORSE PER DIVIDERE LE INTERFACCE 
from flask import Flask, request
from flask_restful import Resource, Api
from dao import DAO
import json, re
dao = DAO()

address_pattern = re.compile(r'^(Via|Viale|Piazza|Corso|Largo)\s+[A-Za-z\s]+\d{1,4}(?:[a-zA-Z]?)$')
cap_pattern= re.compile(r'^\d{5}$')
nome_pattern = re.compile(r'^[a-zA-Z]+$')


# PRIMA RISORSA --> la definizione del nome della risorsa sta nel file .yaml dato dal prof. in questo caso abbiamo due classi: 
""" definitions:  
_____________________________________________________________________
  Cantiere:                           |  Umarell: 
    type: object                      |     type: object
    required:                         |     required: 
      - indirizzo                     |       - nome
      - cap                           |       - cognome       
    properties:                       |       - cap   
      indirizzo:                      |    properties: 
        type: string                  |      nome: 
      cap:                            |        type: string      
        type: integer                 |      cognome:     
        minimum: 0                    |        type: string  
        maximum: 99999                |      cap:
    example:                          |        type: integer  
      indirizzo: 'Via Vivarelli 10'   |        minimum: 0
      cap: 41125                      |        maximum: 99999
                                      |    example:
                                      |      nome: 'Walter' 
                                      |      cognome: 'Ometti' 
                                      |      cap: 41125"
______________________________________|_______________________________
"""

class Cantiere(Resource):
    # VANNO IMPLEMENTATI I METODI SPECIFICATI NELLA DIRETTIVA DEL .YAML 
    def validateFormat(self, data): 
      for k in ["indirizzo", "cap"]: 
        if k not in data.keys(): 
           return False
      
      if not isinstance(data["indirizzo"], (str)) or not address_pattern.match(f"{data['indirizzo']}"):      # validazione CAP
        return False

      if not isinstance(data["cap"], (int)) or not cap_pattern.match(f"{data['cap']}"): 
         return False
      
      return True


    def get(self, idcantiere):
      cantiere = dao.getCantiereByID(idcantiere)
      if cantiere is None: 
          return None, 404
      return cantiere, 200

    def post(self, idcantiere): 
        # validazione richiesta post
        data = request.json
        print(f"POST CANTIERE --> {data}")
        if self.validateFormat(data) is False:
            return None, 400
        
        # Se è gia presente c'è un conflitto
        if dao.getCantiereByID(idcantiere):
            return None, 409 
        
        # altrimenti è tutto ok e si può postare
        dao.postCantiere(idcantiere, data)
        return data, 201
        

# Inviando richieste POST e GET allo URI /api/v1/umarell/{idumarell} è possibile aggiungere o recuperare dati relativi a un umarell
class Umarell(Resource): 
    
     # VANNO IMPLEMENTATI I METODI SPECIFICATI NELLA DIRETTIVA DEL .YAML 
    def validateFormat(self, data): 
      for k in ["nome", "cognome", "cap"]: 
        if k not in data.keys(): 
           return False
      
      # validazione inome --> usiamo le regex
      if not isinstance(data["nome"], (str)) or not nome_pattern.match(f"{data['nome']}"):     
        return False

      if not isinstance(data["cognome"], (str)) or not nome_pattern.match(f"{data['cognome']}"):     
         return False
      
      if not isinstance(data["cap"], (int)) or not cap_pattern.match(f"{data['cap']}"): 
         return False

      return True

    def get(self, idumarell):  
      umarell = dao.getUmarellByID(idumarell)
      print(f"GET UMARELL {umarell}")
      if umarell is None: 
          return None, 404
      return umarell, 200


    def post(self, idumarell):
      # validazione richiesta post
        data = request.json
        print(f"POST UMARELL --> {data}")
        if self.validateFormat(data) is False:
            return None, 400
        
        # Se è gia presente c'è un conflitto
        if dao.getUmarellByID(idumarell):
            return None, 409 
        
        # altrimenti è tutto ok e si può postare
        dao.postUmarell(idumarell, data)
        return data, 201
    
class Clean(Resource): 
   def get(self):
      dao.deleteAll()