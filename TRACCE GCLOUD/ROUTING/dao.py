# DAO OBJECT TO MANAGE COLORS IN FIRESTORE
from google.cloud import firestore
import json 
import ipaddress


class DAO(object): 

    def __init__(self):
         self.db=firestore.Client()
    
    def getRulesDESC(self, list):
        ref = self.db.collection("routing").order_by("netmaskCIDR", direction=firestore.Query.DESCENDING)
        ref = ref.get()
        rv = []
        for r in ref:
            if list:
             rv.append({**r.to_dict(), "rule_id": r.id})
            else: 
                rv.append(r.id)
        return rv
    
    def getRuleByIP(self, IP):      

        tot = self.db.collection('routing').where("ip", "==", f"{IP}").stream()
        rv = []
        for t in tot: 
            rv.append(t.id)
        return rv

    def getRuleByID(self, id):      
        tot = self.db.collection('routing').document(f'{id}').get()
        return tot.to_dict()

    def post(self, data, id):
        ref = self.db.collection('routing')
        ref.document(f"{id}").set(data)
        return self.getRuleByID(id)

    def update(self, data, id):
        ref = self.db.collection('routing')
        ref.document(f"{id}").update(data)
        return self.getRuleByID(id)

    def deleteByID(self, id): 
        self.db.collection("routing").document(f"{id}").delete()

    def deleteAll(self): 
        rules = self.db.collection('routing').list_documents()
        for r in rules:
            r.delete()