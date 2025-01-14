# DAO OBJECT TO MANAGE COLORS IN FIRESTORE
from google.cloud import firestore
import re
import datetime
from google.cloud import pubsub_v1
# QUANDO VIENE AGGIUNTO UN NUOVO CANTIERE --> SI PUBBLICA SUL TOPIC DI RIFERIMENTO: si possono inserire sotto topic? O si filtra per CAP nel subber?

publisher=pubsub_v1.PublisherClient()



class DAO(object): 


    def __init__(self):
        self.c=0
        self.db=firestore.Client()

    def getChirpByID(self, id):   
        tot=self.db.collection('messages').document(f"{id}").get() 
        return tot.to_dict()
    
    def getMessageByHashtag(self, hash):   
        tot = self.db.collection('messages').where("hashtags", "array_contains", hash).get()
        res = [t.to_dict().get("message") for t in tot]
        return res

    def postMessage(self,data):
        # LE INFO DI ID, TIMESTAMP ECC VANNO INSERITE QUI 
        timestamp = datetime.datetime.now()
        self.c +=1
        id = "msgid" + f"{self.c}"
        hashtags = re.findall('(#\w+)', data, re.DOTALL)

        d = {
            "message" : str(data),
            "hashtags": hashtags, 
            "timestamp" : str(timestamp)
        }
        ref = self.db.collection('messages').document(f'{id}').set(d)

        h_data = { id: f'{timestamp}'}
        #verifica di creazione del topic per gli hashtag

        
        for h in hashtags:
            print(h[1:]) # no #
            topic_path = publisher.topic_path('chirpsfc', h[1:])
            print(topic_path)
            try: 
                publisher.create_topic(request={"name": topic_path})
            except: 
                print(f"Hashtag ({h}) topic già presente")
            
            self.db.collection('hashtags').document(h).set(h_data, merge=True)
            result = publisher.publish(topic_path, data.encode('utf-8'))
            print(result)

        # quando viene postato un messaggio si genera anche la collezione topic aggiungendo l'id del messaggio all'hashtag di riferimento      
        return d
        
    def deleteAll(self): 
        for d in self.db.collection("messages").list_documents(): 
           d.delete()


    
    