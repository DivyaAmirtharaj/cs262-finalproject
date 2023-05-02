import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from concurrent import futures
from threading import Lock
import grpc
import time
import argparse
import glob
from collections import defaultdict

class Server(pb2_grpc.MapReduceServicer):
    def __init__(self, num_map_tasks, num_red_asks):
        self.num_map_tasks = num_map_tasks
        self.num_red_tasks = num_red_tasks
        self.lock = Lock()
        self.task_count = 0
        self.task_id = 0
        self.cur_task_type = pb2.TaskType.map
        self.start_time = time.time()
        self.directory = "./inputs"
        self.split_data = self.split_data_for_map(num_map_tasks)
    
    def split_data_for_map(self, num_map_tasks):
        data_by_id = defaultdict(list)
        data_filenames = glob.glob(f'{self.directory}/*')
        for i, filename in enumerate(data_filenames):
            id = i % num_map_tasks
            data_by_id[id].append(filename)
        print(data_by_id)
        return data_by_id
    
    def get_map_or_reduce_task(self):
        task_id = self.task_id
        self.task_id += 1

        if self.cur_task_type == pb2.TaskType.map:
            num_tasks = self.num_map_tasks
        else:
            num_tasks = self.num_red_tasks

        if task_id == num_tasks - 1:
            self.cur_task_type = pb2.TaskType.idle

        if self.cur_task_type == pb2.TaskType.map:
            return pb2.Task(task_type=pb2.TaskType.map,
                            id=task_id,
                            data=self.split_data[task_id],
                            M=self.num_map_tasks
                            )
        else:
            return pb2.Task(task_type=pb2.TaskType.reduce,
                            id=task_id,
                            )
    
    def get_worker_task(self, request: pb2.Empty, context):
        with self.lock:
            if self.cur_task_type == pb2.TaskType.map or self.cur_task_type == pb2.TaskType.reduce:
                return self.get_map_or_reduce_task()
            return pb2.Task(task_type=self.cur_task_type)
    
    def finish_map_task(self, request: pb2.Empty, context):
        with self.lock:
            self.task_count += 1
            
            if self.task_count == self.num_map_tasks:
                self.cur_task_type = pb2.TaskType.map
                self.task_id = 0
                self.task_count = 0
            
            return pb2.Empty()

    def finish_reduce_task(self, request: pb2.Empty, context):
        with self.lock:
            self.task_count += 1
            
            if self.task_count == self.num_red_tasks:
                self.cur_task_type = pb2.TaskType.shut_down
            
            return pb2.Empty()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', dest='M', type=int, required=True, help='number of map tasks')
    parser.add_argument('-N', dest='N', type=int, required=True, help='number of reduce tasks')
    args = parser.parse_args()

    num_map_tasks = args.M
    num_red_tasks = args.N

    address = "localhost"
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    pb2_grpc.add_MapReduceServicer_to_server(Server(num_map_tasks, num_red_tasks), server)  # register the server to gRPC
    print(f'Server is listening on {port}!')
    server.add_insecure_port("{}:{}".format(address, port))
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
