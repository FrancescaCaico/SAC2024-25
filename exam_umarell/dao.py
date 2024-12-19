# TEMPLATE DAO 
import json, os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import pubsub_v1
index_u=0
index_c=0


topic_name=os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'newCantiere'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'examuc'

publisher= pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('examuc', 'newCantiere')


class DAO(object):

    def __init__(self):
        self.db = firestore.Client()
        self.populateDBC('cantiere.json')
        self.populateDBU('umarell.json')
    
    

    def getUmarell(self, id):
        
        tot = self.db.collection('umarell').document(f'{id}').get()
        return tot.to_dict()
    
    def getCantiere(self, id):
        tot = self.db.collection('cantieri').document(f'{id}').get()
        return tot.to_dict()
    
    def getCantieriCAP(self, CAP): 
        tot = self.db.collection('cantieri').where(filter=FieldFilter("cap", "==", CAP)).stream()
        rv =[]
        for t in tot: 
           rv.append(t.to_dict())
        return rv

    def getUmarellCAP(self, CAP): 
        tot = self.db.collection('umarell').where(filter=FieldFilter("cap", "==", CAP)).stream()
        rv =[]
        for t in tot: 
           rv.append(t.to_dict())
        return rv

    def addUmarell(self, id, nome, cognome, CAP):
        ref=self.db.collection('umarell')
        data = {
            'nome': nome, 'cognome': cognome, 'cap' : CAP
        }
        ref.document(f'{id}').set(data)

    def addCantiere(self, id, indirizzo, CAP):
        ref=self.db.collection('cantieri')
        data = {
            'indirizzo': indirizzo, 'cap' : CAP
        }
        ref.document(f'{id}').set(data)
        messaggio = f"Nuovo cantiere: {indirizzo}, CAP: {CAP}"
        future = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
        print(f"[Pub/Sub] Notifica inviata con ID: {future.result()}")

    def populateDBU(self, filename):
        with open(filename) as f:
            data = json.load(f)
            for d in data:
                self.addUmarell(d['id'], d['nome'], d['cognome'], d['cap'])
        
    def populateDBC(self, filename):
        with open(filename) as f:
            data = json.load(f)
            for d in data:
                self.addCantiere(d['id'], d['indirizzo'], d['cap'])
    
    def clean(self):
     ref = self.db.collection('umarell').list_documents()
     for doc in ref:
         doc.delete()
     ref = self.db.collection('cantieri').list_documents()
     for doc in ref:
         doc.delete()


