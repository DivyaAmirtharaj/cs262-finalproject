import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2

SERVER_ADDRESS = 'localhost:50050'

class Client():
    def __init__(self, port) -> None:
        self.port = port
        self.channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = pb2_grpc.MapReduceStub(self.channel)
        self.mapper = Mapper()

    def ask_task(self) -> TaskInfo:

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
			stub = DriverServiceStub(channel)
			task = stub.get_worker_task(pb2.Empty())
		return task

    def run(self) -> None:
        while True:
            try:
            	task = self.ask_task()
            	if task.type == pb2.TaskType.map:
            		self.mapper.map(task.id, task.data, task.M)



