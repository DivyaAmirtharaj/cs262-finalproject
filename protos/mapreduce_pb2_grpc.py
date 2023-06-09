# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import mapreduce_pb2 as protos_dot_mapreduce__pb2


class MapReduceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_worker_task = channel.unary_unary(
                '/grpc.MapReduce/get_worker_task',
                request_serializer=protos_dot_mapreduce__pb2.Worker.SerializeToString,
                response_deserializer=protos_dot_mapreduce__pb2.Task.FromString,
                )
        self.finish_map_task = channel.unary_unary(
                '/grpc.MapReduce/finish_map_task',
                request_serializer=protos_dot_mapreduce__pb2.MapResults.SerializeToString,
                response_deserializer=protos_dot_mapreduce__pb2.MapResults.FromString,
                )
        self.finish_reduce_task = channel.unary_unary(
                '/grpc.MapReduce/finish_reduce_task',
                request_serializer=protos_dot_mapreduce__pb2.ReduceResults.SerializeToString,
                response_deserializer=protos_dot_mapreduce__pb2.Task.FromString,
                )
        self.worker_down = channel.unary_unary(
                '/grpc.MapReduce/worker_down',
                request_serializer=protos_dot_mapreduce__pb2.Worker.SerializeToString,
                response_deserializer=protos_dot_mapreduce__pb2.Empty.FromString,
                )


class MapReduceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_worker_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def finish_map_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def finish_reduce_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def worker_down(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MapReduceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_worker_task': grpc.unary_unary_rpc_method_handler(
                    servicer.get_worker_task,
                    request_deserializer=protos_dot_mapreduce__pb2.Worker.FromString,
                    response_serializer=protos_dot_mapreduce__pb2.Task.SerializeToString,
            ),
            'finish_map_task': grpc.unary_unary_rpc_method_handler(
                    servicer.finish_map_task,
                    request_deserializer=protos_dot_mapreduce__pb2.MapResults.FromString,
                    response_serializer=protos_dot_mapreduce__pb2.MapResults.SerializeToString,
            ),
            'finish_reduce_task': grpc.unary_unary_rpc_method_handler(
                    servicer.finish_reduce_task,
                    request_deserializer=protos_dot_mapreduce__pb2.ReduceResults.FromString,
                    response_serializer=protos_dot_mapreduce__pb2.Task.SerializeToString,
            ),
            'worker_down': grpc.unary_unary_rpc_method_handler(
                    servicer.worker_down,
                    request_deserializer=protos_dot_mapreduce__pb2.Worker.FromString,
                    response_serializer=protos_dot_mapreduce__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.MapReduce', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MapReduce(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_worker_task(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.MapReduce/get_worker_task',
            protos_dot_mapreduce__pb2.Worker.SerializeToString,
            protos_dot_mapreduce__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def finish_map_task(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.MapReduce/finish_map_task',
            protos_dot_mapreduce__pb2.MapResults.SerializeToString,
            protos_dot_mapreduce__pb2.MapResults.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def finish_reduce_task(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.MapReduce/finish_reduce_task',
            protos_dot_mapreduce__pb2.ReduceResults.SerializeToString,
            protos_dot_mapreduce__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def worker_down(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.MapReduce/worker_down',
            protos_dot_mapreduce__pb2.Worker.SerializeToString,
            protos_dot_mapreduce__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
