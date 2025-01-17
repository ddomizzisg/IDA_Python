from IDA.tools import build_building_blocks, inner_product, nextPrime
from IDA.fragment_handler import fragment_writer
import argparse
import pickle
import numpy as np
import sys

class Fragment:
    def __init__(self, idx, content, p, n, m): 
        self.idx = idx
        self.content = content
        self.p = p
        self.n = n
        self.m = m

def split_bytes(data, n, m):
    """
    Inputs: 
    data: bytes to split
    n   : number of fragments after splitting the file
    m   : minimum number of fragments required to restore the file
    Output:
    a list of n fragments (as Fragment objects)
    """
    
    data = pickle.dumps(data)
    
    if n<0 or m<0: 
        raise ValueError("numFragments ad numToAssemble must be positive.")
    
    if m>n: 
        raise ValueError("numToAssemble must be less than numFragments")
    
    # find the prime number greater than n
    # all computations are done modulo p
    p = 257 if n<257 else nextPrime(n)
    

    original_segments=[list(data[i:i+m]) for i in range(0,len(data),m)]
    
    # for the last subfile, if the length is less than m, pad the subfile with zeros 
    # to achieve final length of m
    residue = len(data)%m
    if residue:
        
        last_subfile=original_segments[-1]
        last_subfile.extend([0]*(m-residue))
    
    original_segments_array = np.array(original_segments)
    
    
    building_blocks=build_building_blocks(m,n,p)
    fragments=[]
    for i in range(n): 
        fragment_arr = np.array([inner_product(building_blocks[i], original_segments[k],p) for k in range(len(original_segments))] )
        #print(fragment_arr)
        #print(sys.getsizeof(fragment_arr))
        #fragment = []       
        #for k in range(len(original_segments)): 
        #    fragment.append(inner_product(building_blocks[i], original_segments[k],p))
        #print(fragment)
        #print(sys.getsizeof(fragment))
        frag = Fragment(i, fragment_arr, p, n, m)
        fragments.append(frag)
    
    return fragments

def split(filename, n, m): 
    """
    Inputs: 
    file: name of the file to split
    n   : number of fragments after splitting the file
    m   : minimum number of fragments required to restore the file
    Output:
    a list of n fragments (as Fragment objects)
    """
    if n<0 or m<0: 
        raise ValueError("numFragments ad numToAssemble must be positive.")
    
    if m>n: 
        raise ValueError("numToAssemble must be less than numFragments")
    
    # find the prime number greater than n
    # all computations are done modulo p
    p = 257 if n<257 else nextPrime(n)
    
    # convert file to byte strings
    original_file=open(filename, "rb").read()  
    
    # split original_file into chunks (subfiles) of length m 
    original_segments=[list(original_file[i:i+m]) for i in range(0,len(original_file),m)]
    
    # for the last subfile, if the length is less than m, pad the subfile with zeros 
    # to achieve final length of m
    residue = len(original_file)%m
    if residue:
        
        last_subfile=original_segments[-1]
        last_subfile.extend([0]*(m-residue))
    
    
    building_blocks=build_building_blocks(m,n,p)
    
    fragments=[]
    for i in range(n): 
        fragment = []
        for k in range(len(original_segments)): 
            fragment.append(inner_product(building_blocks[i], original_segments[k],p))
        fragments.append(fragment)
    
    return fragment_writer(filename, n, m, p, original_file, fragments)
    
def main(): 
    parser = argparse.ArgumentParser(description="Split the file.")
    parser.add_argument("filename", metavar = "filename", type = str, help="The file name.")
    parser.add_argument("n", metavar = "numFragments", type = int, help = "Number of fragments after splitting the original file.")
    parser.add_argument("m", metavar = "numToAssemble", type = int, help = "Minimum number of fragments required to assemble/restore the original file. ")
    args = parser.parse_args()
    fragments=split(args.filename, args.n, args.m)
    print(fragments)

if __name__ == "__main__":
    main()
