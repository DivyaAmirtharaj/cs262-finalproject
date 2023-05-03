import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from mapper_reducer import Mapper, Reducer
import sys

SERVER_ADDRESS = 'localhost:50050'

class Client():
    def __init__(self, port) -> None:
        self.port = port
        self.channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = pb2_grpc.MapReduceStub(self.channel)
        self.mapper = Mapper()
        self.reducer = Reducer()
        self.state = "working"

    def _ask_task(self):
        self.channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = pb2_grpc.MapReduceStub(self.channel)
        task = self.stub.get_worker_task(pb2.Empty())
        return task

    def run(self):
        while True:
            try:
                task = self._ask_task()
                if task.task_type == pb2.TaskType.map:
                    self.state = "working"
                    print(task.id)
                    self.mapper.map(task.id, task.data, task.M)
                elif task.task_type == pb2.TaskType.reduce:
                    self.state = "working"
                    self.reducer.reduce(task.id)
                elif task.task_type == pb2.TaskType.idle:
                    self.state = "idle"
                else:
                    print("returned")
                    return
            except Exception as e:
                if self.state != "waiting":
                    print("Server is unavailable")
                    self.state = "waiting"


if __name__ == '__main__':
    port = str(sys.argv[1])
    client = Client(port)
    client.run()