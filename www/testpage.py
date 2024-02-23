from flask import Flask, render_template
import os
import sys
sys.path.insert(1,'/home/kali/Orion/Queuing')
import Queue
import subprocess

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
@app.route('/ping')
def ping():
    return os.popen('ping -c 4 192.168.56.1').read()

@app.route('/ping/<ip_address>')
def ping2(ip_address):
    task_id = Queue.new_task(f'ping -c 1 {ip_address}') #breaks at 10 tasks???
    print("!!!!!!"+str(task_id))
    subprocess.call(["python","/home/kali/Orion/Queuing/Queue.py", f"{task_id}"])
    return "ended"

if __name__ == "__main__":
    app.run(debug=True) 

