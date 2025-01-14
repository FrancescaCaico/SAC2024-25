from flask import Flask, render_template, request
from wtforms import Form, IntegerField, SubmitField, validators, BooleanField
from dao import DAO
import os, json
from google.cloud import pubsub_v1
from api import * 

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
api=Api(app)
dao=DAO()

basePath = "/api/v1"

api.add_resource(Umarell, f'{basePath}/umarell/<int:idumarell>')
api.add_resource(Cantiere, f'{basePath}/cantiere/<int:idcantiere>')
api.add_resource(Clean, f'{basePath}/clean') # o azione importante



#Realizzare una pagina Web che consenta di interrogare il database dei cantieri e degli umarell. La pagina deve prevedere un form con due controlli:
# • Un entryfield per inserire un CAP da ricercare
# • Una serie di checkbox che consentono di selezionare se la ricerca deve essere
# svolta sulla lista degli umarell, dei cantieri o entrambi

# curl -d '{  "id": 5, "indirizzo": "Via Platani 10", "cap": 41122 },' -H "Content-Type: application/json" -v -X POST https://127.0.0.1:8080/api/v1/cantieri/5

# CREAZIONE DEL FORM 
class SearchForm(Form): 
     cap=IntegerField("Cap", [validators.NumberRange(00000, 99999)])
     umarell=BooleanField("Umarell")
     cantieri = BooleanField("Cantieri")
     submit = SubmitField("Search")

@app.route("/search", methods=["GET"])
def search():
    form = SearchForm(request.args)
    u = []
    c=[]
    if request.method == 'GET': 
        cap = form.data.get("cap")
        if form.data.get("cantieri") is True: 
             # la ricerca per cantieri
            c = dao.getCantiereByCAP(cap)
          
        if form.data.get("umarell") is True: 
             # la ricerca per cantieri
            u = dao.getUmarellByCAP(cap)
        
        return render_template("search.html", umarell=u, cantieri=c, form=form)
    
    return render_template("search.html", form=form)


# Realizzare un sistema che implementa un meccanismo di notifica che consente agli umarell di essere aggiornati su nuovi cantieri. 
# Un umarell si può registrare a un topic e ricevere notifiche sui nuovi cantieri che vengono inseriti. 
# Da linea di comando è possibile specificare uno o più CAP che saranno usati per filtrare i messaggi utili.
# Si chiede di realizzare:
# • Una modifica alle funzioni di inserimento dei cantieri che generi anche la notifica sull’apposito topic indicando indirizzo e CAP
# • Un nuovo software client che riceve le notifiche e le mostra su standard output (eventualmente filtrandole)



if __name__ == '__main__':
     app.run(host='127.0.0.1', port=8080, debug=True)