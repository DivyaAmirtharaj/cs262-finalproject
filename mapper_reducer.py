import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2

SERVER_ADDRESS = 'localhost:50050'

class Mapper():
	#need to add the enter/exit stuff for the file cache
	def __init__(self):
		self.files = {}

	# pass set of filenames 
	def map(self, map_id, filenames, M): 
		os.makedirs('map_dirs')
		
		for filename in filenames:
			with open(filename, 'r') as file:
				for word in file.read().split():
					bucket_id = ord(word[0]) % M

					if filename not in self._files:
						self.files[filename] = open(filename, 'a')

					words = self.files(f'{map_dirs}/mr-{map_id}-{bucket_id}')
					words.write(f'{word}\n')

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
			stub = DriverServiceStub(channel)
			stub.FinishMap(Empty())

class Reducer():


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
		os.makedirs('out')
		counts = self.count_bucket(bucket_id)
		with open(f'out/out-{bucket_id}', 'a') as out:
			for key, val in counts.items():
				out.write(f'{key} {val}\n')

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            stub.FinishReduce(Empty())
