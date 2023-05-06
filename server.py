import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from concurrent import futures
from threading import Lock
import grpc
import time
import argparse
import glob
import os
from collections import defaultdict

INPUT_DIR = "./books"
INTERMEDIATE_DIR = "./map_dirs"
OUT_DIR = "./out"

class Server(pb2_grpc.MapReduceServicer):
    def __init__(self, num_map_tasks, num_red_tasks, workers):
        self.num_map_tasks = num_map_tasks
        self.num_red_tasks = num_red_tasks
        self.lock = Lock()
        self.task_count = 0
        self.task_id = 0
        self.cur_task_type = pb2.TaskType.map
        self.start_time = time.time()
        self.split_data = self.split_data_for_map(num_map_tasks)
        self.worker_ids = workers
        self.map_task_split = {id : [] for id in workers}
        self.red_task_split = {id : [] for id in workers}
        self.map_task_backlog = []
        self.red_task_backlog = []
    
    def clear_prev_output_data(self, dir):
        filenames = glob.glob(f'{dir}/*')
        for f in filenames:
            os.remove(f)
    
    def update_task_backlogs(self, id):
        num_map_backlog = len(self.map_task_split[id])
        num_red_backlog = len(self.red_task_split[id])
        self.map_task_backlog.extend(self.map_task_split[id])
        self.red_task_backlog.extend(self.red_task_split[id])
        self.task_count -= (num_map_backlog + num_red_backlog)
        if num_map_backlog > 0:
            self.cur_task_type = pb2.TaskType.map 
        elif num_red_backlog > 0:
            self.cur_task_type = pb2.TaskType.reduce

    def split_data_for_map(self, num_map_tasks):
        self.clear_prev_output_data(INTERMEDIATE_DIR)
        self.clear_prev_output_data(OUT_DIR)
        data_by_id = defaultdict(list)
        data_filenames = glob.glob(f'{INPUT_DIR}/*')
        for i, filename in enumerate(data_filenames):
            id = i % num_map_tasks
            data_by_id[id].append(filename)
        return data_by_id

    def get_map_task(self, worker_id):
        if len(self.map_task_backlog) != 0:
            print("from backlog")
            task_id = self.map_task_backlog.pop(0)
        else:
            task_id = self.task_id
            self.task_id += 1
        if task_id == self.num_map_tasks - 1:
            self.cur_task_type = pb2.TaskType.idle
        print(worker_id)
        print(task_id)
        self.map_task_split[worker_id].append(task_id)
        print(self.map_task_split)
        
        return pb2.Task(task_type=pb2.TaskType.map,
                            id=task_id,
                            data=self.split_data[task_id],
                            num_red_tasks=self.num_red_tasks
                            )

    def get_reduce_task(self, worker_id):
        if len(self.red_task_backlog) != 0:
            task_id = self.red_task_backlog.pop(0)
        else:
            task_id = self.task_id
            self.task_id += 1
        print(task_id)
        if task_id == self.num_red_tasks - 1:
            self.cur_task_type = pb2.TaskType.idle

        self.red_task_split[worker_id].append(task_id)

        return pb2.Task(task_type=pb2.TaskType.reduce,
                            id=task_id,
                            )
    
    def worker_down(self, request: pb2.Worker, context):
        down_id = request.id
        self.update_task_backlogs(down_id)
        return pb2.Empty()

    def get_worker_task(self, request: pb2.Worker, context):
        with self.lock:
            worker_id = request.id
            if self.cur_task_type == pb2.TaskType.map:
                return self.get_map_task(worker_id)
            elif self.cur_task_type == pb2.TaskType.reduce:
                return self.get_reduce_task(worker_id)
            return pb2.Task(task_type=self.cur_task_type)
    
    def finish_map_task(self, request: pb2.Empty, context):
        with self.lock:
            self.task_count += 1
            
            if self.task_count == self.num_map_tasks:
                self.cur_task_type = pb2.TaskType.reduce
                self.task_id = 0
                self.task_count = 0
            
            return pb2.Empty()

    def finish_reduce_task(self, request: pb2.Empty, context):
        with self.lock:
            self.task_count += 1
            
            if self.task_count == self.num_red_tasks:
                self.cur_task_type = pb2.TaskType.shut_down
                elapsed_time = time.time() - self.start_time
                print(f"Finished after {elapsed_time} seconds")
            
            return pb2.Empty()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', dest='M', type=int, required=True, help='number of map tasks')
    parser.add_argument('-N', dest='N', type=int,required=True, help='number of reduce tasks')
    parser.add_argument('-workers', dest='worker_list', nargs="*", type=int, default=[1,2])
    args = parser.parse_args()

    num_map_tasks = args.M
    num_red_tasks = args.N
    workers = args.worker_list

    address = "localhost"
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    mapreduce = Server(num_map_tasks, num_red_tasks, workers)
    pb2_grpc.add_MapReduceServicer_to_server(mapreduce, server)  # register the server to gRPC
    print(f'Server is listening on {port}!')
    server.add_insecure_port("{}:{}".format(address, port))
    server.start()

    while True:
        time.sleep(64 * 64 * 100)
