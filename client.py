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

    def _ask_task(self):
        task = self.stub.get_worker_task(pb2.Empty())
        return task

    def run(self):
        while True:
            try:
                task = self._ask_task()
                if task.task_type == pb2.TaskType.map:
                    self.mapper.map(task.id, task.data, task.M)
                elif task.task_type == pb2.TaskType.reduce:
                    self.reducer.reduce(task.id)
                elif task.task_type == pb2.TaskType.shut_down:
                    pass
                else:
                    return
            except Exception as e:
                print(e)

if __name__ == '__main__':
    port = str(sys.argv[1])
    client = Client(port)
    client.run()