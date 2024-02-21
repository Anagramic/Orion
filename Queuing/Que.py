import os

def get_tasks():
    os.chdir('Queuing/Tasks/')
    return os.popen('ls').read().split()


def new_task(command):
    tasks = get_tasks()
    os.system('pwd')
    return os.popen(command).read()

print(new_task('ping -c 2 192.168.137.1'))
