import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from mapper_reducer import Mapper, Reducer
from concurrent import futures
import sys

SERVER_ADDRESS = 'localhost:50050'

class Worker():
    def __init__(self, id) -> None:
        self.id = id
        self.channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = pb2_grpc.MapReduceStub(self.channel)
        self.mapper = Mapper()
        self.reducer = Reducer()
        self.state = "working"
        self.map_results = None
        self.reduce_results = None

    def _ask_task(self):
        task = self.stub.get_worker_task(pb2.Worker(id=self.id))
        return task

    def run(self):
        while True:
            try:
                self.channel = grpc.insecure_channel(SERVER_ADDRESS)
                self.stub = pb2_grpc.MapReduceStub(self.channel)
                task = self._ask_task()
                if task.task_type == pb2.TaskType.map:
                    print("mapping")
                    self.state = "working"
                    res = self.mapper.map(task.id, task.data, task.num_red_tasks)
                    self.map_results = self.stub.finish_map_task(res)
                elif task.task_type == pb2.TaskType.reduce:
                    self.state = "working"
                    self.reducer.reduce(task.id, self.map_results)
                elif task.task_type == pb2.TaskType.idle:
                    self.state = "idle"
                else:
                    print("returned")
                    return
            except grpc.RpcError as e:
                if self.state != "waiting":
                    print(e)
                    print("Server is offline")
                    self.state = "waiting"
            except KeyboardInterrupt:
                response = self.stub.worker_down(pb2.Worker(id=self.id))
                exit()


if __name__ == '__main__':
    address = "localhost"
    id = int(sys.argv[1])
    worker = Worker(id)
    worker.run()