import pytest
import unittest
import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from worker import Worker
from unittest.mock import MagicMock, patch

class WorkerTest(unittest.TestCase):
    #@patch('grpc.insecure_channel')
    def setUp(self):
        self.mock_stub = MagicMock()
        self.mock_stub.get_worker_task.return_value = pb2.Task(id=0, data=["file"], task_type=pb2.TaskType.map, num_red_tasks=2)
        self.mock_channel = MagicMock()
        self.worker = Worker(1)
        self.worker.stub = self.mock_stub
        self.worker.channel = self.mock_channel
    
    def test_worker_setup(self):
        assert(self.worker.id == 1)
        assert(self.worker.channel == self.mock_channel)

    def test_ask_task(self):
        task = self.worker._ask_task()

        assert(isinstance(task, pb2.Task))
        assert(task.id == 0)
        assert(task.task_type == pb2.TaskType.map)

if __name__ == "__main__":
    t = WorkerTest()
    t.setUp()
    t.test_worker_setup()
    t.test_ask_task()
