import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from concurrent import futures
from threading import Lock, Event
import grpc
import time
import argparse

class Server(pb2_grpc.MapReduceServicer):
    def __init__(self, num_map_tasks, num_red_asks):
        self.num_map_tasks = num_map_tasks
        self.num_red_tasks = num_red_tasks
        self.lock = Lock()
        self.task_count = 0
        self.task_id = 0
        self.cur_task_type = pb2.TaskType.map
        self.start_time = time.time()
    
    def chunk_data():
        
    
    def get_map_or_reduce_task(self):
        id = self.task_id
        self.task_id += 1

        if self.cur_task_type == pb2.TaskType.map:
            num_tasks = self.num_map_tasks
        else:
            num_tasks = self.num_red_tasks

        if id == num_tasks - 1:
            self.cur_task_type = pb2.TaskType.idle

        if self.cur_task_type == pb2.TaskType.map:
            return pb2.Task(type=pb2.TaskType.map,
                            id=id,
                            )
        else:
            return pb2.Task(type=pb2.TaskType.map,
                            id=id,
                            )
    
    def get_worker_task(self, request: pb2.Empty, context):
        with self.lock:
            return self.get_map_or_reduce_task()
    
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
                # stop
            
            return pb2.Empty()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', dest='N', type=int, required=True, help='number of map tasks')
    parser.add_argument('-M', dest='M', type=int, required=True, help='number of reduce tasks')
    args = parser.parse_args()

    num_map_tasks = args.N 
    num_red_tasks = args.M 

    address = "localhost"
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    pb2_grpc.add_MapReduceServicer_to_server(Server(), server)  # register the server to gRPC
    print(f'Server is listening on {port}!')
    server.add_insecure_port("{}:{}".format(address, port))
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
