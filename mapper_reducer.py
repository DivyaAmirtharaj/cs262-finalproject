import grpc
import protos.mapreduce_pb2_grpc as pb2_grpc
import protos.mapreduce_pb2 as pb2
import os
from protos.mapreduce_pb2_grpc import MapReduceStub
import glob

SERVER_ADDRESS = 'localhost:50050'

class Mapper():
	# The Mapper class handles the map phase of MapReduce

	def __init__(self):
		self.files = {}  # Dictionary to keep track of opened files

	def map(self, map_id, filenames, M): 
		"""
		Performs the map operation for a given map_id and set of filenames.

		Args:
			map_id (int): The ID of the map task.
			filenames (list): List of filenames to process.
			M (int): Total number of reduce tasks (buckets).

		"""
		try:
			os.makedirs('map_dirs')  # Create a directory to store map output files
		except Exception as e:
			pass
		
		for filename in filenames:
			with open(filename, 'r') as file:
				text = file.read()
				print(text)
				for word in text.split():
					bucket_id = ord(word[0]) % M  # Calculate the bucket ID for the word

					new_file = f'map_dirs/mr-{map_id}-{bucket_id}'  # Create a new file for the word

					if new_file not in self.files:
						self.files[new_file] = open(new_file, 'a')  # Open the file if it doesn't exist in the dictionary

					words = self.files[new_file]
					words.write(f'{word}\n')  # Write the word to the file

		for file in self.files.values():
			file.close()  # Close all the opened files
		self.files = {}  # Reset the dictionary

		print("exited loop")

		with grpc.insecure_channel(SERVER_ADDRESS) as channel:
			stub = MapReduceStub(channel)
			stub.finish_map_task(pb2.Empty())  # Notify the server that the map task is finished

class Reducer():
	# The Reducer class handles the reduce phase of MapReduce

	def __init__(self) -> None:
		pass

	def count_bucket(self, bucket_id):
		"""
		Counts the occurrences of words in a specific bucket.

		Args:
			bucket_id (int): ID of the bucket to count.

		Returns:
			dict: Dictionary with word counts.

		"""
		counter = {}
		for file in glob.glob(f'map_dirs/mr-*-{bucket_id}'):  # Iterate over files in the specified bucket
			with open(file) as f:
				print(file)
				for word in f.readlines():
					w = word.strip()
					if w not in counter:
						counter[w] = 0
					counter[w] += 1
		return counter

	def reduce(self, bucket_id):
		"""
		Performs the reduce operation for a given bucket ID.

		Args:
			bucket_id (int): ID of the bucket to reduce.

		"""
		try:
			os.makedirs('out')  # Create a directory to store the output files
		except:
			pass
		counts = self.count_bucket(bucket_id)  # Count the occurrences of words in the bucket
		with open(f'out/out-{bucket_id}', 'a') as out:
			print(counts)
			for key, val in counts.items():
				print("writing")
				out.write(f'{key} {val}\n')  # Write the word count to the output file

