import glob
import time
from collections import defaultdict

if __name__ == "__main__":
    filenames = glob.glob("./inputs")
    start_time = time.time()
    for filename in filenames:
        counts = defaultdict(0)
        with open(filename, 'r') as file:
            for word in file.read().split():
                counts[word] += 1
    
        for key in counts:
            val = counts[key]
            print(f'{key} {val}')
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f'Time elapsed: {end_time - start_time}')