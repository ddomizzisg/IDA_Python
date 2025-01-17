from IDA.tools import vandermonde_inverse
from IDA.fragment_reader import fragment_reader
import numpy as np
import argparse

def assemble(fragments_filenames, output_filename=None): 
    '''
    Input: 
    fragments_filenames : a list of fragments filenames
    output_filename: a String for the name of the file to write
    Output: 
    String represents the content of the original file
    If filename is given, the content is written to the file
    '''
    
    (m, n, p, fragments) = fragment_reader(fragments_filenames)
    building_basis=[]
    fragments_matrix=[]
    for (idx,fragment) in fragments:
        building_basis.append(idx)
        fragments_matrix.append(fragment)
    
    inverse_building_matrix =  vandermonde_inverse(building_basis,p)
    
    # convert inverse_building_matrix and fragments_matrix to numpy array
    inverse_building_matrix = np.array(inverse_building_matrix)
    fragments_matrix=np.array(fragments_matrix)
    
    output_matrix = np.matmul(inverse_building_matrix, fragments_matrix)%p
    
    # each column of output matrix is a chunk of the original matrix
    original_segments=[]
    ncol = len(output_matrix[0])
    nrow = len(output_matrix)
    for c in range(ncol): 
        col = [output_matrix[r][c] for r in range(nrow)]
        original_segments.append(col)
    
    # combine the original_segment into original_file
    original_file=[]
    for segment in original_segments: 
        original_file.extend(segment)
    
    # convert original_file to its content
    original_file_content = "".join(list(map(chr, original_file)))
    
    if output_filename:# write the output to file
        with open(output_filename,'wb') as fh:
            fh.write(bytes(original_file))
    
        print("Generated file {}".format(output_filename))
        return 
    else: 
        return original_file_content
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble the files")
    parser.add_argument("fragments_filenames", help="A list of fragments filenames.")
    parser.add_argument("output_filename", help="Name of the output file.", default=None)
    args = parser.parse_args()
    main(args.fragments_filenames, args.output_filename)
