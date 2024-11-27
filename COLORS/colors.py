# DAO OBJECT TO MANAGE COLORS IN FIRESTORE
from google.cloud import firestore
import json 

class Colors(object):

    def __init__(self):
        self.db=firestore.Client()


    def populateDB(self, filejson): 
        colors_ref= self.db.collection("colors")
        with open(filejson) as f: # prendo il file json
            colors=json.load(f)
        for c in colors: 
            colors_ref.document(c['name']).set(c) 

    def get_color(self, name):
        if not name or name is None:  
            colors = self.db.collection('colors').stream()
            colors_data = [c.to_dict() for c in colors] 
            return colors_data

     
        c = self.db.collection('colors').document(name).get()
        rv = c.to_dict() if c.exists else None
        return rv

    def add_color(self, name, r, g, b):
        print(name)
        colors_ref = self.db.collection('colors')
        colors_ref.document(name).set({'name': name,'red': r, 'green': g, 'blue': b})
    

    def delete_color(self, name): 
        self.db.collection('colors').document(name).delete()


if __name__ == '__main__':
    c= Colors()
   # c.populateDB("colors.json")
    print(c.get_color())
