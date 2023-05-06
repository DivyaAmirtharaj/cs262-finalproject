import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
import os
from protos.mapreduce_pb2_grpc import MapReduceStub
import glob
import string

SERVER_ADDRESS = 'localhost:50050'

class Mapper():
	#need to add the enter/exit stuff for the file cache
	def __init__(self):
		self.files = {}

	# pass set of filenames 
	def map(self, map_id, chunks, num_red_tasks): 
		try:
			os.makedirs('map_dirs')
		except Exception as e:
			pass
		
		for chunk in chunks:
			text = chunk.translate(str.maketrans('', '', string.punctuation)).lower()

			for word in text.split():
				bucket_id = ord(word[0]) % num_red_tasks
				new_file = f'map_dirs/mr-{map_id}-{bucket_id}'

				if new_file not in self.files:
					self.files[new_file] = open(new_file, 'a')

				words = self.files[new_file]
				words.write(f'{word}\n')

		for file in self.files.values():
			file.close()
		self.files = {}

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
			stub = MapReduceStub(channel)
			print("finishing")
			stub.finish_map_task(pb2.Empty())

class Reducer():
	def __init__(self) -> None:
		pass

	def count_bucket(self, bucket_id):
		counter = {}
		for file in glob.glob(f'map_dirs/mr-*-{bucket_id}'):
			with open(file) as f:
				for word in f.readlines():
					w = word.strip()
					if w not in counter:
						counter[w] = 0
					counter[w] += 1
		return counter

	def reduce(self, bucket_id):
		try:
			os.makedirs('out')
		except:
			pass
		counts = self.count_bucket(bucket_id)
		with open(f'out/out-{bucket_id}', 'a') as out:
			for key, val in counts.items():
				out.write(f'{key} {val}\n')
			out.close()

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
			stub = MapReduceStub(channel)
			stub.finish_reduce_task(pb2.Empty())
