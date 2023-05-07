import subprocess
import time

num_map_tasks = 3
num_red_tasks = 2
num_workers = 2

# Define the terminal commands to run
server_command = f'python server.py -M {num_map_tasks} -N {num_red_tasks}'
directory = "Desktop/CS262/cs262-finalproject"

# Open new terminals for each worker
for worker_id in range(num_workers):
    worker_command = f'python worker.py {worker_id+1}'
    subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "cd ' + directory + '; ' + worker_command + '"'])
time.sleep(5)

# Open a new terminal for the server
subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to do script "cd ' + directory + '; ' + server_command + '"'])
