import os

def get_tasks():
    os.popen('cd /Queuing/Tasks')
    os.popen('ls')

def new_task(command):
    get_tasks()
    return os.popen(command).read()

print(new_task('ping -c 2 192.168.137.1'))
