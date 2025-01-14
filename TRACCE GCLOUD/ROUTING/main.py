from flask import Flask, render_template, request 
from flask_restful import Api
from wtforms import Form, IntegerField, SubmitField, validators, BooleanField, StringField
from dao import DAO
import os, json
from google.cloud import pubsub_v1
from api import * 

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
api = Api(app)

basePath="/api/v1"

api.add_resource(Rule, f'{basePath}/routing/<int:id>')
api.add_resource(RuleList, f'{basePath}/routing')
api.add_resource(Clean, f'{basePath}/clean') # o azione importante


# Realizzare una pagina Web che mostra:
#  • il contenuto della tabella di routing
#  • un form per inserire un indirizzo IP
# Se viene inviato il form, viene mostrata di nuovo la pagina, ma si evidenzia con 
# il colore rosso la regola di routing che viene usata per il routing dell’indirizzo
# specificato. In caso di errori nei campi del form, viene invece mostrato un
# messaggio di errore

@app.route("/", methods=['GET', 'POST'])
def home(): 
    # SI DEVONO STAMPARE TUTTE LE REGOLE DI ROUTING
    rules = dao.getRulesDESC(list=1)
    return render_template("home.html", rules=rules)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)