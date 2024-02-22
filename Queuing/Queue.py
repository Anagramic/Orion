import os
import time

def get_tasks():
    os.chdir('/home/kali/Orion/Queuing/Tasks')
    
    #gets all the task folders in the "Tasks" directory and splits them in to an array
    tasks = os.popen('ls').read().split()
    tasks_array = []

    #Goes throuhg all task folders and extraxcts the data (id,status,command,result) associated
    for task in tasks:
        os.chdir(task)
        files = os.popen('ls').read().split()
        
        with open('STATUS') as file:
            status = file.read()
        
        with open('COMMAND') as file:
            command = file.read()

        with open('TIME_START') as file:
                time_start = file.read()

        if status == 'COMPLETE':
            with open('OUTPUT') as file:
                result = file.read()
            with open('TIME_STOP') as file:
                time_stop = file.read()
        else:
            result = 'in progress'
            time_stop = time.time()

        tasks_array.append({
            'id':task,
            'status': status, 
            'command':command, 
            'result':result, 
            'time_start':time_start, 
            'time_stop':time_stop})
        
        os.chdir('/home/kali/Orion/Queuing/Tasks')
    
    return tasks_array


def new_task(command):
    tasks = get_tasks()
    
    for task in tasks:
        print(task)
    os.system('pwd')
    return os.popen(command).read()

print(new_task('ping -c 1 192.168.137.1'))
