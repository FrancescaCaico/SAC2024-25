from flask import Flask, render_template, request
from horses import Horses
import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')

# si istanzia anche l'oggetto dao --> per questo non serve importare firestore come modulo 
horses_dao=Horses()
@app.route('/', methods=['GET'])
def home():
    famous4horses=horses_dao.get_fourfamous()
    return render_template('home.html', famous_horses=famous4horses)


@app.route('/horses/<name>', methods=['GET'])
def get_name(name):
    ngen=4
    pedigree=horses_dao.get_pedigree(name, ngen=ngen)
    h=horses_dao.get_horse(name)
    v=horses_dao.get_visualizations(name)
    horses_dao.insert_visual(datetime.datetime.now(), name)
    return render_template('pedigree.html', horse=h, pedigree=pedigree, ncols=len(pedigree[ngen-1]), visual=v)    # ncols=len(pedigree[ngen-1]) --> la lunghezza degli elementi che ho  a livello di caratteristiche


@app.errorhandler(404)
def horse_not_found(e): 
    path=request.path
    return render_template('404.html', link=path) , 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
