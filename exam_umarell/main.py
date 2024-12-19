from flask import Flask, render_template, request
from wtforms import Form, IntegerField, SubmitField, validators, BooleanField
from dao import DAO
import os, json
from google.cloud import pubsub_v1
#from colors_gcp import Colors

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
dao=DAO()

# Create object to encapsulate model (for form)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class SearchForm(Form):
    cap = IntegerField('Cap', [validators.NumberRange( min=00000, max=50000)])
    umarell = BooleanField('Umarell')
    cantieri = BooleanField('Cantieri')
    submit= SubmitField('Submit')


@app.route('/', methods=['GET'])
def homepage():

    cantieridata = []
    umarelldata = []

    if request.method == 'GET':
        f = SearchForm(request.args)
        if f.cantieri.data: 
           cantieridata= dao.getCantieriCAP(f.cap.data)
           print(cantieridata)

        if f.umarell.data: 
           umarelldata = dao.getUmarellCAP(f.cap.data)
           print(umarelldata)

    return render_template('index.html', form = f, cantieri= cantieridata, umarell = umarelldata)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

