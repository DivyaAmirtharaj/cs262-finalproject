import glob
import time
import string
from collections import defaultdict

if __name__ == "__main__":
    filenames = glob.glob("./books/*")
    start_time = time.time()
    for filename in filenames:
        counts = defaultdict(lambda: 0)
        with open(filename, 'r') as f:
            text = f.read()
            text = text.translate(str.maketrans('', '', string.punctuation)).lower()
            for word in text.split():
                counts[word] += 1
        f.close()

    with open("std_out.txt", "w") as f:
        for key in counts:
            val = counts[key]
            f.write(f'{key} {val}\n')
    f.close()
            
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f'Time elapsed: {end_time - start_time}')