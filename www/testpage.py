from flask import Flask, render_template
import os
import sys
sys.path.insert(1,'/home/kali/Orion/Queuing')
import Queue
import subprocess
import re

capitalise_first = lambda word :  word[0].upper() + word[1:len(word)] if word != None else word

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('HomePageTemplate.html')

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
    task_id = Queue.new_task(f'ping -c 10 {ip_address}')
    subprocess.Popen(f"python /home/kali/Orion/Queuing/Queue.py {task_id}",shell=True)
    task_info = Queue.get_task_info(task_id)
    return task_info

@app.route('/QuickStartScan')
def quickstart():
    return get_IP()
    #task_id = Queue.new_task(f'nmap')

def get_IP():
    interfaces = []
    ifconfig = os.popen('ifconfig').read().split("\n\n")
    print("\n\n".join(ifconfig))
 
    for interface in ifconfig:
        
        try:
            interface_name = re.findall(".+: ",interface)[0].removesuffix(": ")
        except:
            break
        
        try:
            ipv4 = re.findall("inet \S+ ",interface)[0].removeprefix("inet ").removesuffix(" ")
        except:
            ipv4 = ""
        
        try:
            mask = re.findall("netmask \S+ ",interface)[0].removeprefix("netmask ").removesuffix(" ")
        except:
            mask = ""
        
        try:    
            ipv6 = re.findall("inet6 \S+ ",interface)[0].removeprefix("inet6 ").removesuffix(" ")
        except:
            ipv6 = ""

        interfaces.append({
            "interface" :interface_name,
            "ipv4"      :ipv4,
            "mask"      :mask,
            "ipv6"      :ipv6
        })

    
    return interfaces
    #for interface in re.findall(" [a-z]+[0-9]*: ", ifconfig):

if __name__ == "__main__":
    app.run(debug=True) 

