import subprocess
import time
import os

def run_process(num_map_tasks, num_red_tasks, chunk_size, num_workers):
    # Define the terminal commands to run
    server_command = f'python server.py -M {num_map_tasks} -N {num_red_tasks} -chunk {chunk_size}'
    directory = os.getcwd()

    # Open new terminals for each worker
    worker_terminals = []
    for worker_id in range(num_workers):
        worker_command = f'python worker.py {worker_id+1}'
        worker_process = subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "cd ' + directory + '; ' + worker_command + '"'])
        worker_terminals.append(worker_process)
    time.sleep(5)
    # Open a new terminal for the server
    terminal_process = subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "cd ' + directory + '; ' + server_command + '"'])
    time.sleep(5)

    # Get the process ID (PID) of the terminal process
    terminal_pid = terminal_process.pid
    # Use sudo and kill to terminate the terminal process
    subprocess.run(['sudo', 'kill', '-9', str(terminal_pid)])


def run(chunk_size):
    for i in range(5):
        num_map_tasks = i
        for j in range(5):
            num_red_tasks = j
            for k in range(5):
                num_workers = k
                run_process(num_map_tasks, num_red_tasks, chunk_size, num_workers)

'''
run(1000)
run(10000)
run(100000)
'''

'''
# Exmaple running of experiment, will open 3 worker terminals, and 1 server terminal and output the result to experiment_results
num_map_tasks = 3
num_red_tasks = 2
chunk_size = 100000
num_workers = 2
run_process(num_map_tasks, num_red_tasks, chunk_size, num_workers)
'''
