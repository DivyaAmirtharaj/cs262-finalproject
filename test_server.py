import pytest
import unittest
import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
from server import Server
from unittest.mock import MagicMock, patch

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.server = Server(5, 3, [1, 2, 3])
    
    def test_server_setup(self):
        assert(self.server.task_count == 0)
        assert(self.server.task_id == 0)
        assert(self.server.cur_task_type == pb2.TaskType.map)
    
    def test_map_task(self):
        worker_request = pb2.Worker(id=1)
        task = self.server.get_worker_task(worker_request, None)
        assert(task.task_type == pb2.TaskType.map)
        assert(task.id == 0)

        self.server.finish_map_task(pb2.Empty(), None)
        assert(self.server.task_count == 1)
    
    def test_worker_dead_after_map(self):
        worker_request = pb2.Worker(id=1)
        empty = self.server.worker_down(worker_request, None)

        assert(self.server.task_count == 0)
        assert(self.server.map_task_backlog == [0])
    
    def test_reduce_task(self):
        self.server.task_count = 0
        self.server.task_id = 0
        self.server.cur_task_type = pb2.TaskType.reduce

        worker_request = pb2.Worker(id=2)
        task = self.server.get_worker_task(worker_request, None)

        assert(task.task_type == pb2.TaskType.reduce)
        assert(task.id == 0)

        self.server.finish_reduce_task(pb2.Empty(), None)

        assert(self.server.task_count == 1)
    
    def test_worker_dead_after_reduce(self):
        worker_request = pb2.Worker(id=2)
        empty = self.server.worker_down(worker_request, None)

        assert(self.server.task_count == 0)
        assert(self.server.red_task_backlog == [0])
    

if __name__ == "__main__":
    t = ServerTest()
    t.setUp()
    t.test_map_task()
    t.test_worker_dead_after_map()
    t.test_reduce_task()
    t.test_worker_dead_after_reduce()
