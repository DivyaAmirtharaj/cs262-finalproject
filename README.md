# cs262-finalproject

Starting a server:

Before running the server code, make sure you have the following dependencies installed:

Python 3
gRPC (Python version)
protobuf (Python version)


Make sure you have the following directory available in the project directory:

./books (for input data files)

If any of these directories are missing, create them manually.

Update the server code (server.py) with the desired configurations:

INPUT_DIR: Directory path for input data files.
INTERMEDIATE_DIR: Directory path for intermediate map task outputs.
OUT_DIR: Directory path for final reduce task outputs.
EXPERIMENT_FILE: File path for recording experiment results.

Start the MapReduce server by running the following command:

python server.py -M <num_map_tasks> -N <num_red_tasks> -chunk <chunk_size> -workers <worker_list>

Replace the following command-line arguments:

<num_map_tasks>: Number of map tasks to be performed.
<num_red_tasks>: Number of reduce tasks to be performed.
<chunk_size>: Size of data chunks to be processed.
<worker_list>: List of worker IDs (space-separated) that will connect to the server.

Ensure that the input data files are present in the ./books directory before starting the server.
To clean up the generated intermediate and output files, simply delete the ./map_dirs and ./out directories.

Starting a worker:

Run the worker using the following command:
python worker.py <worker_id> <server_address>

The workers can be started before starting a server for timing purposes (they will wait until a server is started). 

Experiments are found in experiment.py and unit tests are found in test_server.py and test_worker.py.