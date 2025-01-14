# DAO OBJECT TO MANAGE COLORS IN FIRESTORE
from google.cloud import firestore
from datetime import datetime


class DAO(object): 

    def __init__(self):
         self.db=firestore.Client()

    def getTravel(self, user, date):      
        tot = self.db.collection('travels').document(f'{user}_{date}').get()
        return tot.to_dict()
    

    def getCommonUsersTravelInfo(self, user): 
        # dato l'utente i viaggi in comune con altri utenti
        ref = self.db.collection("travels").where("user", "==", f"{user}").get()
        # cosi prendiamo quelli dell'utente selezionato ora cerchiamo per partenza 
        users = []
        for r in ref: 
            r.to_dict()
            place = self.db.collection("travels").where("from", '==', f"{r.get('from')}").where("to", '==', f"{r.get('to')}").get()
            for p in place: 
                p = p.to_dict()
                date_p = datetime.strptime(p.get('date'), "%Y-%m-%d")
                date_r = datetime.strptime(r.get('date'), "%Y-%m-%d")
                delta = date_p - date_r
                if  delta.days <= 1 and r.get('user')!=p.get('user'): 
                    users.append(p.get('user'))
        return users
    
    def getCommonUsersTravel(self, user, info): 
        # dato l'utente i viaggi in comune con altri utenti
        ref = self.db.collection("travels").where("user", "==", f"{user}").get()
        # cosi prendiamo quelli dell'utente selezionato ora cerchiamo per partenza 
        if info is False: 
            users = []
            for r in ref: 
                r.to_dict()
                place = self.db.collection("travels").where("from", '==', f"{r.get('from')}").where("to", '==', f"{r.get('to')}").get()
                for p in place: 
                    p = p.to_dict()
                    date_p = datetime.strptime(p.get('date'), "%Y-%m-%d")
                    date_r = datetime.strptime(r.get('date'), "%Y-%m-%d")
                    delta = date_p - date_r
                    if  delta.days <= 1 and r.get('user')!=p.get('user'): 
                        if info is False: 
                            users.append(p.get('user'))
        else:
            users = []
            for r in ref: 
                r = r.to_dict()
                place = self.db.collection("travels").where("from", '==', f"{r.get('from')}").where("to", '==', f"{r.get('to')}").get()
                u = []
                for p in place: 
                    p = p.to_dict()
                    date_p = datetime.strptime(p.get('date'), "%Y-%m-%d")
                    date_r = datetime.strptime(r.get('date'), "%Y-%m-%d")
                    delta = date_p - date_r
                    if  delta.days <= 1 and r.get('user')!=p.get('user'): 
                        u.append(p.get('user'))
                users.append({"route": r , "users" : u})
                                        
        return users

    def getCommonUsersTravelUpdated(self, user): 
        # dato l'utente i viaggi in comune con altri utenti
        ref_old = self.db.collection("travels").where("user", "==", f"{user}").get()
        # cosi prendiamo quelli dell'utente selezionato ora cerchiamo per partenza 
        users = []
        for r in ref_old: 
            r = r.to_dict()
            place = self.db.collection("travels").where("from", '==', f"{r.get('from')}").where("to", '==', f"{r.get('to')}").get()
            u_old = []
            for p in place: 
                p = p.to_dict()
                date_p = datetime.strptime(p.get('date'), "%Y-%m-%d")
                date_r = datetime.strptime(r.get('date'), "%Y-%m-%d")
                delta = date_p - date_r
                if  delta.days <= 1 and r.get('user')!=p.get('user'): 
                    print("trovato un old user")
                    u_old.append(p.get('user'))
                print(u_old)
            up = self.db.collection("updated").document(f"{r.get('user')}_{r.get('date')}").get()
            if up:
                up = up.to_dict()
                place = self.db.collection("travels").where("from", '==', f"{up.get('new_from')}").where("to", '==', f"{up.get('new_to')}").get()
                u_new = []
                for p in place: 
                    p = p.to_dict()
                    date_p = datetime.strptime(p.get('date'), "%Y-%m-%d")
                    date_r = datetime.strptime(up.get('new_date'), "%Y-%m-%d")
                    delta = date_p - date_r
                    if  delta.days <= 1 and up.get('user')!=p.get('user'): 
                        u_new.append(p.get('user'))
                print("Trovato un modified")
                users.append({"original": r , "original_users" : u_old, "modified": up, "new_users": u_new})
        print(users)
        return users

    def postTravel(self, user, date, data):
        ref = self.db.collection('travels')
        ref.document(f'{user}_{date}').set(data)
        return self.getTravel(user, date)

    # def delete(self, name): 
    #     self.db.collection('<nome>').document(name).delete()