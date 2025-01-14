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

api.add_resource(Chirp, f'{basePath}/chirps')
api.add_resource(Chirps, f'{basePath}/chirps/<string:id>')
api.add_resource(Clean, f'{basePath}/clean') # o azione importante

class HashtagForm(Form):
    hashtag = StringField("Hashtag", validators=[validators.Length(1, 100)])
    sub = SubmitField("Cerca")
     
class MessageForm(Form):
    message = StringField("Message", validators=[validators.Length(1, 100)])
    sub = SubmitField("Invia")
     

@app.route("/insert", methods=['GET', 'POST'])
def search():
    form_msg=MessageForm(request.form) # per le post 
    form_hash=HashtagForm(request.args) # per le get
    # si vuole postare un messaggio
    if request.method == 'POST':
       mes = form_msg.data.get("message")
       d = dao.postMessage(mes)
       return render_template("search.html", ok = True, form_msg = form_msg, form_hash=form_hash)
    
    if request.method == 'GET': 
        if form_hash.data.get("hashtag") is not None:
        # HO PRESO GLI HASHTAG DEVO FARE LA GET SUL DAO E POI UNA NUOVA PAGINA HTML DA RENDEIRIZZARE
            m = dao.getMessageByHashtag(form_hash.data.get("hashtag"))
            print(m)
            return render_template("hashtags.html", messages = m)
        else:     
            return render_template("search.html", form_msg = form_msg, form_hash = form_hash)

if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)