import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from concurrent import futures
import grpc
import time

class Server(pb2_grpc.MapReduceServicer):
    def __init__(self):
        pass

if __name__ == '__main__':
    address = "localhost"
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    pb2_grpc.add_MapReduceServicer_to_server(Server(), server)  # register the server to gRPC
    print(f'Server is listening on {port}!')
    server.add_insecure_port("{}:{}".format(address, port))
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
