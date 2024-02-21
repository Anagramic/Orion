from flask import Flask, render_template
 
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@app.route('/Page')
def second_page():
    return "<p>This is a second page</p>"

if __name__ == "__main__":
    app.run(debug=True) 