
import base64
import os
from flask import Flask, json, request, render_template
from flask_restful import Resource, Api
from wtforms import Form, DateField, StringField, validators, SubmitField
from dao import DAO
from api import *
from google.cloud import pubsub_v1, firestore

topic_name=os.environ['TOPIC'] if 'TOPIC_NAME' in os.environ.keys() else 'updates'
project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'uviaggiu'

publisher= pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('uviaggiu', 'updates')

app = Flask(__name__,static_url_path='/static',static_folder='static')
api=Api(app)
dao = DAO()

# SI INSERISCE IL BASE PATH SPECIFICATO NEL .YAML DELLA CONFIGURAZIONE ( SOLITAMENTE DATA DAL PROF )
basePath = "/api/v1"

api.add_resource(TravelDetails, f'{basePath}/travel/<string:user>/<string:date>')
api.add_resource(CommonTravels, f'{basePath}/travel/<string:user>')

# Interfaccia Web
# Realizzare un’applicazione web che permetta di visualizzare gli itinerari di un utente selezionato e gli utenti che condividono l’itinerario
@app.route("/<user>", methods=['GET'])
def home(user):
    travels = dao.getCommonUsersTravel(user, 1)
    return render_template("home.html", travels = travels)

@app.route("/<user>/2", methods=['GET'])
def home2(user):
    print(user)
    travels = dao.getCommonUsersTravelUpdated(user)
    return render_template("home2.html", travels = travels)

# Interconnessione di servizi
# Realizzare un sistema di notifica basato su Google Cloud PubSub per permettere agli utenti di comunicare eventuali
# cambiamenti di itinerari. Permettere agli utenti di inviare tali notifiche attraverso l’interfaccia web, accedendo
# alla pagina di modifica tramite click sullo step dell’itinerario desiderato, permettendo quindi la modifica dei campi
# dell’itinerario. Tali modifiche dovranno essere memorizzate dall’applicazione (tramite l’utilizzo di una Cloud
# Function) in una sezione differente rispetto a quella utilizzata per l’inserimento dell’itinerario. NON dovranno
# essere perse informazioni riguardanti l’itinerario originale.

class TravelForm(Form):
    date = DateField("Date")
    dep =  StringField("From", [validators.Length(3), validators.DataRequired()])
    to=  StringField("To", [validators.Length(3), validators.DataRequired()])
    sub = SubmitField("Modifica")

@app.route("/travel/<user>/<date>/modify", methods = ["POST", "GET"])
def modifyRoute( user, date): 
    f = TravelForm(request.form)
    if request.method == "POST": 
        new_from = f.dep.data
        new_to = f.to.data
        new_date = f.date.data
        # si pubblica sul topic la modifica 
        original = dao.getTravel(user, date)
        messaggio = {
            "original" : original, 
            "modified" : {"from" : new_from, "to" : new_to, "date": new_date}
        }
        # questo si pubblica sul topic --> serve il publisher 
        data = json.dumps(messaggio).encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        print(f"[Pub/Sub] Notifica inviata con ID: {future.result()}")
        return home(user)
    return render_template("modify.html", form=f)

def update_travels(event, context):
    print('funzione chiamata')
    db = firestore.Client() 
    # arriva il messaggio 
    messaggio =  event["data"]
    decoded_data = base64.b64decode(messaggio).decode('utf-8')
    travel_data = json.loads(decoded_data)
    print(f"Dati ricevuti {travel_data}")
    user = travel_data["original"]["user"]
    data_o = travel_data["original"]["date"]
    data = {
      "user": user,  "new_from" : travel_data["modified"]["from"], "new_to" : travel_data["modified"]["to"], "new_date": travel_data["modified"]["date"]
    }
    print(data)
    db.collection("updated").document(f"{user}_{data_o}").set(data)



if __name__ == '__main__':
     app.run(host='127.0.0.1', port=8080, debug=True)