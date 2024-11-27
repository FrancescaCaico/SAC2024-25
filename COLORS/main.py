from flask import Flask, render_template, request
from colors import Colors

app = Flask(__name__, static_url_path='/static', static_folder='static')
colors_dao=Colors()


@app.route('/', methods=['GET'])
def home():
    col=colors_dao.get_color(None)
    return render_template('home.html', colors=col)

@app.route('/colors/<name>', methods=['GET'])
def get_onecolor(name):
    col=colors_dao.get_color(name)
    return render_template('singlecolor.html', color=col)


@app.route('/colors/manage/', methods=['GET', 'POST'])
def manage(): 
    if request.method == 'POST':
        action=request.form.get('action')
        name = request.form.get('name')
        
        if action == 'add':  # Operazione di eliminazione          
            r = request.form.get('red', type=int)
            g = request.form.get('green', type=int)
            b = request.form.get('blue', type=int)
            colors_dao.add_color(name, r, g, b)
        
        if action == 'delete':
            colors_dao.delete_color(name)
    
    col=colors_dao.get_color(None)
    return render_template('manage.html', colors=col)    
 


@app.errorhandler(404)
def color_not_found(e): 
    path=request.path
    return render_template('404.html', link=path) , 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
