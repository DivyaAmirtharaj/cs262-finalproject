update protos:
python -m grpc_tools.protoc --proto_path=. protos/mapreduce.proto --python_out=. --grpc_python_out=.