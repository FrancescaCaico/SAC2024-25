from google.cloud import firestore
import json, datetime

class Horses(object):
    def __init__(self):
        self.db=firestore.Client()

    def populate_db(self, datafile): 
        horses_ref= self.db.collection('horses')
        with open(datafile) as f: # prendo il file json
            horses=json.load(f)
        for h in horses: 
            horses_ref.document(h['name']).set(h)   # per ogni cavallo l'ID è il suo nome e viene inserito nel firestore con set.

    def get_horse(self, name):
        name=name.upper()   # così diventa non case sensitive 
        # qui vanno inseriti anche i controlli 
        if name=='' or name is None:
            return None
        h=self.db.collection('horses').document(name).get() # recuperiamo il cavallo il cui documento è indicato dal suo nome.
        rv=h.to_dict() if h.exists else None
        return rv
    
    #RECUPERO GENITORI DEI CAVALLI
    def get_parents(self, horses_list):
        rv=[]
        for name in horses_list: 
         h = self.get_horse(name)
         if h is not None: 
            rv.append(h['sire'] if 'sire' in h.keys() else '')    # creo la lista dei padri aggiungendo del dictionary il nome
            rv.append(h['dam'] if 'dam' in h.keys() else '')    # creo la lista delle madri per ogni cavallo
         else:
            rv.extend(['', '']) # extend concatena le liste
        return rv

    #recupero le generazioni a partire da un cavallo
    def get_pedigree(self, name, ngen=2):
        name= name.upper()
        horses_list=[name]
        pedigree={}
        #si vuole avere un dictionary in cui c'è il numero della generazione e la lista degli elementi dei cavalli
        for i in range(ngen): 
            pedigree[i]=horses_list     # si prende il nome del cavallo
            horses_list=self.get_parents(horses_list)   # si chiama get parents
        return pedigree
    
    def insert_visual(self, timestamp, name): 
        name=name.upper()   # così diventa non case sensitive 
        h_ref=self.db.collection('horses').document(name) # recuperiamo il cavallo il cui documento è indicato dal suo nome.
        visual =h_ref.collection('visualizations').add({'timestamp': timestamp}) 
        return self.db.collection('horses').document(name).get() # recuperiamo il cavallo il cui documento è indicato dal suo nome.

    def get_visualizations(self, name):
        name=name.upper()   # così diventa non case sensitive 
        h=self.db.collection('horses').document(name) # recuperiamo il cavallo il cui documento è indicato dal suo nome.
        v_ref=h.collection('visualizations').stream()
        timestamps = set()

        for v in v_ref:
            visual = v.to_dict()
            timestamp = visual.get('timestamp')
        
            if timestamp:
                if isinstance(timestamp, datetime.datetime):
                    timestamps.add(timestamp)
                else:
                    print(f"Formato timestamp non riconosciuto nel documento {v.id}")
        return len(timestamps)

    def get_fourfamous(self): 
        horses_ref=self.db.collection('horses').stream()
        horses_vis=[]
        for h in horses_ref:
            horse_data= h.to_dict()
            visual=self.get_visualizations(h.id)
            horses_vis.append({'horse': horse_data, 'visualizations':visual})

        horses_vis.sort(key=lambda x: x['visualizations'], reverse=True)
        return horses_vis[:4]



if __name__ == '__main__': 
    h= Horses()
 #  h.populate_db('horses.json')
    # print(h.get_horse('varenne')) --> provare sempre in locale
   #print(h.get_parents(['varenne']))
    #print(h.get_pedigree('varenne', ngen=2))    # {0: ['VARENNE'], 1: ['WAIKIKI BEACH', 'IALMAZ']}
    #print(h.get_pedigree('varenne', ngen=3))    # {0: ['VARENNE'], 1: ['WAIKIKI BEACH', 'IALMAZ'], 2: ['SPEEDY SOMOLLI', 'HULA LOBELL', 'ZEBU', 'BAREE']}
    #h.insert_visual(datetime.datetime.now(), 'varenne')
    #print(h.get_visualizations('varenne'))
    print(h.get_fourfamous())