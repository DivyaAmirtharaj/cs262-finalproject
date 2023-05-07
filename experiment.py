import subprocess
import time
import os

num_map_tasks = 3
num_red_tasks = 2
chunk_size = 100000
num_workers = 2

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
time.sleep(2)
terminal_process.terminate()
subprocess.run(['osascript', '-e', 'tell application "Terminal" to close (every window whose name contains "' + directory + '")'])

