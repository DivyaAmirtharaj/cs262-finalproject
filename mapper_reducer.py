import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
import os
from protos.mapreduce_pb2_grpc import MapReduceStub
import glob
import string


class Mapper():
	#need to add the enter/exit stuff for the file cache
	def __init__(self):
		self.files = {}

	# pass set of filenames 
	def map(self, map_id, chunks, num_red_tasks, server_address): 
		map_results = {}
		for chunk in chunks:
			text = chunk.translate(str.maketrans('', '', string.punctuation)).lower()

			for word in text.split():
				bucket_id = ord(word[0]) % num_red_tasks
				new_key = f'map_dirs/mr-{map_id}-{bucket_id}'
				if new_key not in map_results:
					map_results[new_key] = []
				
				map_results[new_key].append(word)

		res = pb2.MapResults()
		for key, value in map_results.items():
			w = pb2.WordList()
			w.word_list.extend(value)
			res.map_results[key].CopyFrom(w)

		with grpc.insecure_channel(server_address) as channel:
			stub = MapReduceStub(channel)
			print("finishing")
			stub.finish_map_task(res)
		return res

class Reducer():
	def __init__(self) -> None:
		pass

	def count_bucket(self, map_results):
		counter = {}
		for container in map_results.map_results.values():
			for word in container.word_list:
				word = word.strip()
				if word not in counter:
					counter[word] = 0
				counter[word] += 1
		return counter

	def reduce(self, bucket_id, map_results, server_address):
		print(key for key in map_results.map_results.keys())
		counts = self.count_bucket(map_results)
		reduce_res = pb2.ReduceResults()
		for key, val in counts.items():
			reduce_res.reduce_results[key] = val
		reduce_res.bucket_id = bucket_id

		with grpc.insecure_channel(server_address) as channel:
			stub = MapReduceStub(channel)
			stub.finish_reduce_task(reduce_res)
