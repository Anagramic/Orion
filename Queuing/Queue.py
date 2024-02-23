import os
import time
import sys

def start_running(taskID):
    os.chdir(f'/home/kali/Orion/Queuing/Tasks/{taskID}/')
    with open('STATUS','w') as file:
        file.write('WORKING')

    run_command(taskID)

def run_command(taskID):
    os.chdir(f'/home/kali/Orion/Queuing/Tasks/{taskID}/') #add path?
    
    with open('COMMAND','r') as file:
        command = file.readline()
        print(command)

    os.popen(f"{command} > /home/kali/Orion/Queuing/Tasks/{taskID}/OUTPUT")
    
    with open('STATUS','w') as file:
        file.write('COMPLETE')
    
    with open('TIME_STOP','w') as file:
        file.write(str(time.time()))

def get_task_info(task_id):
    try:
        os.chdir(f'/home/kali/Orion/Queuing/Tasks/{task_id}/')
    except:
        return "not found"
    
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
        result = status.lower().capitalize()
        time_stop = time.time()
    return {
            'id'        :task_id,
            'status'    :status, 
            'command'   :command, 
            'result'    :result, 
            'time_start':time_start, 
            'time_stop' :time_stop}

def get_tasks():
    os.chdir('/home/kali/Orion/Queuing/Tasks')
    
    #gets all the task folders in the "Tasks" directory and splits them in to an array
    tasks = os.popen('ls').read().split()
    tasks_array = []

    #Goes throuhg all task folders and extraxcts the data (id,status,command,result) associated
    for task in tasks:
        os.chdir(task)
        tasks_array.append(get_task_info(task))
        
        os.chdir('/home/kali/Orion/Queuing/Tasks')
    
    return tasks_array

def format_data(data): #data is a list of dictionaries with the same key
    headings = list(data[0].keys())

    data_array = []
    for dictionary in data:
        data_array.append(list(dictionary.values()))

    #makes all cells strings
    for row in data_array:
        for position in range(len(row)):
            row[position] = str(row[position])

    for position in range(len(headings)):
        headings[position] = str(headings[position])

    #makes a list of the max length of each row   
    row_lengths = []
    for heading in headings: #sets all the max lengths to be at lest the length of the heading
        row_lengths.append(len(heading))

    for position in range(len(row_lengths)): #changes the length if the new found entry is longer
        for row in data_array:
            if len(row[position]) > row_lengths[position]:
                row_lengths[position] = len(row[position])
    
    final_output = '|'
    for position in range(len(headings)):
        final_output = final_output + headings[position] #adds the heading
        for _ in range(row_lengths[position]):  #adds the trailing spaces
            final_output+=' '
        final_output += '|'
    final_output+='\n'
    table_width = len(final_output)
    line = ''
    
    for _ in range (table_width):
        line+='-'
    
    final_output = line+'\n'+final_output+line+'\n'

    for row in data_array:
        final_output +='|'
        for position in range(len(row)):
            final_output+=row[position]
            for _ in range(row_lengths[position]-len(row[position])):
                final_output+=' '
            final_output += '|'
        final_output += line + '\n'
    
    print(final_output)

def new_task(command):
    tasks = get_tasks()

    ids = [] # will break if no files exist
    if tasks != []:
        for task in tasks:
            ids.append(task['id'])
        ids.sort()
        new_id = int(ids[-1]) +1
    else:
        new_id = 1

    os.mkdir(f'/home/kali/Orion/Queuing/Tasks/{new_id}/')
    os.chdir(f'/home/kali/Orion/Queuing/Tasks/{new_id}/')
    
    with open('COMMAND','w') as file:
        file.write(command)
    with open('OUTPUT','w'): pass
    with open('STATUS','w') as file:
        file.write('NOT STARTED')
    with open('TIME_START','w') as file:
        file.write(str(time.time()))
    with open('TIME_STOP','w') as file:
        file.write(str(time.time()))

    return(new_id)

if __name__ == "__main__":
    print(sys.argv[1])
    start_running(sys.argv[1])

#How to use this
#Run new_task as a library in flask
#Then pass the task id returned back into this as a sys arg which runs as subproccess