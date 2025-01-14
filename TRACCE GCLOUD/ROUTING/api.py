import re
from flask import  request
from flask_restful import Resource, Api
from dao import DAO
import ipaddress

"""L’applicazione deve esporre le seguenti funzionalità tramite opportune Web API  RESTful:
 1. inviando richieste POST allo URI /api/v1/routing/{id} è possibile inserire una nuova regola di routing
 2. inviando richieste GET allo URI /api/v1/routing/{id} è possibile leggere una regola 
 3. inviando richieste PUT allo URI /api/v1/routing/{id} è possibile modificare una regola
 4. inviando richieste DELETE allo URI /api/v1/routing/{id} è possible cancellare una regola
 5. inviando richieste GET allo URI /api/v1/routing/ è possibile ottenere la lista delle regole nella tabella di routing (in ordine decrescente di lunghezza del prefisso))
 6. inviando richieste POST allo URI /api/v1/routing/ è possibile verificare il routing verso un indirizzo IP
 7. inviando richieste POST allo URI /api/v1/clean è possibile azzerare la tabella di routing

L’interfaccia di utilizzo delle API deve soddisfare rigorosamente il file di specifica OpenAPI disponibile insieme alla presente specifica"""
dao = DAO()


ip_pattern=re.compile(r'^(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}')

class Rule(Resource):

    def validate_data(self, data): 
        for k in ["ip", "netmaskCIDR", "gw", "device"]: 
            if k not in data.keys():
                return False
        # VALIDAZIONE IP
        if not isinstance(data["ip"], (str)) or not ip_pattern.match(str(data['ip'])) :
            print(f"{data['ip']} NON È UN IP VALIDO")
            return False
        
        # VALIDAZIONE gw
        if not isinstance(data["gw"], (str)) or not ip_pattern.match(str(data["gw"])):
            print(f"{data['gw']} NON È UN GW VALIDO")
            return False
        
        # VALIDAZIONE NETMASK
        if not isinstance(data["netmaskCIDR"], (int)) or  not 0<=data["netmaskCIDR"]<=30:
            print(f"{data} NON È UNA NETMASK VALIDA")
            return False

        # VALIDAZIONE DEVICE
        if not isinstance(data["device"], (str)):
            print(f"{data['device']} NON È UN device VALIDO")
            return False
        
        try: 
            ipaddress.IPv4Network(f'{data["ip"]}/{data["netmaskCIDR"]}', strict=True) # controlla semplicemente se l'ip è di rete
        except: 
            return False

        return True

    def post(self, id):
        # si può inserire una regola di routing --> request.json ci sono i dati formattati
        data = request.json
        # bisogna validare l'id 
        print(id)
        if not isinstance(id, (int)): 
            return None, 400
        
        if dao.getRuleByID(id): 
            return None, 409
        
        # vanno validati gli altri campi
        if self.validate_data(data) is False:
            return None, 400
        d = dao.post(data, id)

        return d, 201
    
    def get(self, id):
        try:
            int_id = int(id)
            print(f"ID CHE DOVREBBE FALLIRE {id}")
            if int_id < 0:
                return None, 400
                
            d = dao.getRuleByID(id)
            if d is None: 
                print(f"non c'è con l'id {id}")
                return None, 404
            return d, 200
        except :
            return None, 400

    def put(self,id):
        data = request.json
        d = dao.getRuleByID(id)
        if d is None: 
            return None, 404
        return dao.update(data, id), 200
    
    def delete(self, id):
        d = dao.getRuleByID(id)
        if d is None: 
            return None, 404
        dao.deleteByID(id)
        return None, 204

class RuleList(Resource):
     
    def post(self):
        ip = request.json
        ip = ip[1:-1]
        routing_table = dao.getRulesDESC(1) # prendiamo le regole di routing
        res = []
        real_ip = ipaddress.ip_address(ip)
        gateway = filter(lambda route: route["netmaskCIDR"] == 0, routing_table)
        for route in routing_table:
            print(route)
            network = ipaddress.ip_network(f'{route["ip"]}/{route["netmaskCIDR"]}', strict=True)
            if real_ip in network:
                print("found", route)
                return f'"{route["rule_id"]}"', 200
        return None, 404
    
  # 5. inviando richieste GET allo URI /api/v1/routing/ è possibile ottenere la lista delle regole nella tabella di routing (in ordine decrescente di lunghezza del prefisso))
    def get(self):
        r = dao.getRulesDESC(0)
        return r, 200

class Clean(Resource): 
    def post(self): 
        dao.deleteAll()
        return None, 200
