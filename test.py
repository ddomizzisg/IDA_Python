from IDA.split import split_bytes
import random
from IDA.assemble import assemble_bytes
import time


test_data = random.randbytes(1 * 1000000 * 10)

#Store data in file
#with open('test_data', 'wb') as f:
#   f.write(test_data)

#fragments = split_bytes(test_data, 2, 1)
for n in range(2,50):
    for k in range(1,n):
        start_time = time.time()
        fragments = split_bytes(test_data, n, k)
        end_time = time.time()
        print(n,k, end_time-start_time, flush=True)


#result = assemble_bytes(fragments)
#print( result)
#fragments = IDA.split("README.md", 10, 5) 