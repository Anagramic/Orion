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
            'id'        :task,
            'status'    :status, 
            'command'   :command, 
            'result'    :result, 
            'time_start':time_start, 
            'time_stop' :time_stop})
        
        os.chdir('/home/kali/Orion/Queuing/Tasks')
    
    return tasks_array

def format_data(data): #data is a list of dictionaries with the same key
    headings = data[0].keys()

    data_array = []
    for dictionary in data:
        data_array.append(dictionary.values())

    print(data_array) 
    #makes all cells strings
    for row in data_array:
        for position in range(len(row)):
            row[position] = str(row[position])

    for position in range(len(headings)):
        headings[position] = str(headings[position])

    #makes a list of the max length of each row   
    row_lengths = []
    for heading in headings: #sets all the max lengths to be at lest the length of the heading
        row_lengths.appen(len(heading))

    for position in range(len(row_lengths)): #changes the length if the new found entry is longer
        for row in data_array:
            if len(row[position]) > row_lengths[position]:
                row_lengths[position] = len(row[position])
    
    final_output = '|'
    for position in range(len(headings)):
        final_output = final_output + headings[position] #adds the heading
        for _ in range(row_lengths[position]):  #adds the trailing spaces
            final_output+=' '
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
    


def format_data_wrong(data):
    #get headings
    headings = data[0].keys()
    print(headings)
    max_length = 0
    data_array = []

    for dictionary in data:
        data_array.append(dictionary.values())

    for heading in headings:
    
        if len(heading) > max_length:
            max_length = len(heading)
    
    for row in data_array:
    
        for cell in row:
            cell = str(cell)
            if len(cell) > max_length:
                max_length = len(cell)
    
    final_output = '|'
    for heading in headings:
        final_output+=heading
        for _ in range(max_length-len(heading)):
            final_output+=' '
        final_output+='|'

    row_length=len(final_output)
    cross = ''

    for _ in range(row_length//2):
        cross+='_'
    cross+='\n'

    final_output = cross + final_output + "\n"
    for row in data_array:
        new_row = '|'
        for cell in row:
            cell = str(cell)
            new_row+=cell
            for _ in range(max_length-len(cell)):
                new_row+=' '
        final_output+= new_row + '|\n' + cross
    
    print(final_output)

    
            
        
    
    



def new_task(command):
    tasks = get_tasks()
    format_data(tasks)
    os.system('pwd')
    return os.popen(command).read()

print(new_task('ping -c 1 192.168.137.1'))
