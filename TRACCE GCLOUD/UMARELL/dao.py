# DAO OBJECT TO MANAGE COLORS IN FIRESTORE
import json
from google.cloud import firestore
from google.cloud import firestore
from google.cloud import pubsub_v1
# QUANDO VIENE AGGIUNTO UN NUOVO CANTIERE --> SI PUBBLICA SUL TOPIC DI RIFERIMENTO: si possono inserire sotto topic? O si filtra per CAP nel subber?
publisher=pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("umcant", "newCant")



class DAO(object): 


    def __init__(self):
         self.db=firestore.Client()

    def getUmarellByID(self, id):      
        tot = self.db.collection('umarell').document(f'{id}').get()
        return tot.to_dict()
    

    def getUmarellByCAP(self, CAP):   
        tot= []   
        for t in self.db.collection('umarell').where("cap", "==", CAP).get(): 
            tot.append(t.to_dict())
        return tot
    
    def getCantiereByID(self, id):      
        tot = self.db.collection('cantieri').document(f'{id}').get()
        return tot.to_dict()
    
    def getCantiereByCAP(self, CAP):   
        tot= []   
        for t in self.db.collection('cantieri').where("cap", "==", CAP).get(): 
            tot.append(t.to_dict())

        return tot

    def postCantiere(self, id, data):
        # i dati arrivano formattati in json
        ref = self.db.collection('cantieri')
        ref.document(f'{id}').set(data)
        # ho postato un nuovo cantiere --> funziona anche se si aggiorna. ==> devo pubblicare sul topic generale
        # si deve effettuare l'encode? SI
        data = json.dumps(data).encode("utf-8")
        print(data)
        future = publisher.publish(topic_path, data)
        print(f"[Pub/Sub] Notifica inviata con ID: {future.result()}")

    
    def postUmarell(self, id, data):
        ref = self.db.collection('umarell')
        ref.document(f'{id}').set(data)
        

    def deleteAll(self): 
        for d in self.db.collection("cantieri").list_documents(): 
           d.delete()
        for d in self.db.collection("umarell").list_documents(): 
           d.delete()

    
    