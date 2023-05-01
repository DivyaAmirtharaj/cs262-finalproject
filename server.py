import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from concurrent import futures
import grpc
import time
import argparse

class Server(pb2_grpc.MapReduceServicer):
    def __init__(self, num_map_tasks, num_red_asks):
        self.num_map_tasks = num_map_tasks
        self.num_red_tasks = num_red_tasks
    
    def next_map_task(self):
    
    def give_task_to_worker(self, request, )

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
