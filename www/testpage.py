from flask import Flask, render_template
import os

capitalise_first = lambda word :  word[0].upper() + word[1:len(word)] if word != None else word

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@app.route('/Page')
def second_page():
    return "<p>This is a second page</p>"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('TestTemplate.html', name=capitalise_first(name))
@app.route('/pwd')
def pwd():
    return os.system('pwd')

if __name__ == "__main__":
    app.run(debug=True) 
