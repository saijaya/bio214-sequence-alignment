"""

This file provides skeleton code for align.py. 

Locations with "FILL IN" in comments are where you need to add code.

Note - you MUST follow this structure or else the autograder will not run properly

Usage: python align.py input_file output_file

"""


import sys
import pandas as pd
import numpy as np


#### ------ USEFUL FUNCTIONS ------- ####
def fuzzy_equals(a, b):
    """
    Checks if two floating point numbers are equivalent.
    """
    epsilon = 10**(-6) 
    return (abs(a - b) < epsilon)
    

#### ------- CLASSES ------- ####

class MatchMatrix(object):
    """
    Match matrix class stores the scores of matches in a data structure
    """
    def __init__(self):
        pass

    def set_score(self, a, b, score):
        """
        Updates or adds a score for a specified match

        Inputs:
           a = the character from sequence A
           b = the character from sequence B
           score = the score to set it for
        """
        ### TO-DO! FILL IN ###

    def get_score(self, a, b):
        """
        Returns the score for a particular match, where a is the
        character from sequence a and b is from sequence b.

        Inputs:
           a = the character from sequence A
           b = the character from sequence B
        Returns:
           the score of that match
        """
        ### TO-DO! FILL IN ###



class ScoreMatrix(object):
    """
    Object to store a score matrix, which generated during the alignment process. The score matrix consists of a 2-D array of
    ScoreEntries that are updated during alignment and used to output the maximum alignment.
    """

    def __init__(self, name, nrow, ncol):
        self.name = name # identifier for the score matrix - Ix, Iy, or M
        self.nrow = nrow
        self.ncol = ncol
        self.score_matrix # FILL IN 
        # you need to figure out a way to represent this and how to initialize
        # Hint: it may be helpful to have an object for each entry

    def get_score(self, row, col):
        ### TO-DO! FILL IN ###
        pass
        
    def set_score(self, row, col, score):    
        ### TO-DO! FILL IN ###
        pass

    def get_pointers(self, row, col):
        """
        Returns the indices of the entries that are pointed to
        This should be formatted as a list of tuples:
         ex. [(1,1), (1,0)]
        """
        ### TO-DO! FILL IN ###

    def set_pointers(self, row, col): ### TO-DO! FILL IN - this needs additional arguments ###
        ### TO-DO! FILL IN ###
        pass

    def print_scores(self):
        """
        Returns a nicely formatted string containing the scores in the score matrix. Use this for debugging!

        Example:
        M=
            0.0, 0.0, 0.0, 0.0, 0.0
            0.0, 1.0, 0.0, 0.0, 0.0
            0.0, 1.0, 1.0, 1.0, 1.0
            0.0, 0.0, 1.0, 1.0, 1.0
            0.0, 0.0, 2.0, 2.0, 1.0
            0.0, 0.0, 1.0, 2.0, 3.0

        """
        ### TO-DO! FILL IN ###
        pass


    def print_pointers(self):
        """
        Returns a nicely formatted string containing the pointers for each entry in the score matrix. Use this for debugging!
        """

        ### TO-DO! FILL IN ###

class AlignmentParameters(object):
    """
    Object to hold a set of alignment parameters from an input file.
    """

    def __init__(self):
        # default values for variables that are filled in by reading
        # the input alignment file
        self.seq_a = ""
        self.seq_b = ""
        self.global_alignment = False 
        self.dx = 0
        self.ex = 0
        self.dy = 0
        self.ey = 0
        self.alphabet_a = "" 
        self.alphabet_b = ""
        self.len_alphabet_a = 0
        self.len_alphabet_b = 0
        self.match_matrix = MatchMatrix()

    def load_params_from_file(self, input_file): 
        """
        Reads the parameters from an input file and stores in the object

        Input:
           input_file = specially formatted alignment input file
        """

        input_params_dict = read_input_file(input_file)
        print_input_params(input_params_dict)
        self.seq_a = str(input_params_dict["seq_a"])
        self.seq_b = str(input_params_dict["seq_b"])
        self.global_alignment = bool(input_params_dict["global_alignment"])
        self.dx = float(input_params_dict["dx"])
        self.ex = float(input_params_dict["ex"])
        self.dy = float(input_params_dict["dy"])
        self.ey = float(input_params_dict["ey"])
        self.alphabet_a = str(input_params_dict["alphabet_a"])
        self.alphabet_b = str(input_params_dict["alphabet_b"])
        self.len_alphabet_a = int(input_params_dict["len_alphabet_a"])
        self.len_alphabet_b = int(input_params_dict["len_alphabet_b"])
        self.match_matrix = input_params_dict["match_matrix"]
        print("hahahaha")
        print(type(self.match_matrix))


class Align(object):
    """
    Object to hold and run an alignment; running is accomplished by using "align()"
    """

    def __init__(self, input_file, output_file):
        """
        Input:
            input_file = file with the input for running an alignment
            output_file = file to write the output alignments to
        """
        self.input_file = input_file
        self.output_file = output_file
        self.align_params = AlignmentParameters()

        # Note the below three lines is ensure the autograder runs properly.
        # You should leave the below three lines as is but then
        # Initialize m_matrix, ix_matrix, and iy_matrix in populate_score_matrices
        self.m_matrix = None
        self.ix_matrix = None
        self.iy_matrix = None

    def align(self):
        """
        Main method for running alignment.
        """

        # load the alignment parameters into the align_params object
        self.align_params.load_params_from_file(self.input_file)

        # populate the score matrices based on the input parameters
        self.populate_score_matrices()

        # perform a traceback and write the output to an output file

        ### TO-DO! FILL IN ###

    def populate_score_matrices(self):
        """
        Method to populate the score matrices based on the data in align_params.
        Should call update(i,j) for each entry in the score matrices
        Note: You MUST initialize M, Ix, Iy in this function rather than elsewhere
        """

        ### TO-DO! FILL IN ###
        num_rows_in_score_matrices = self.align_params.len_alphabet_a+1
        num_columns_in_score_matrices = self.align_params.len_alphabet_b + 1

        self.M_score_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))
        self.M_score_matrix[0, :] = 0.0
        self.M_score_matrix[:, 0] = 0.0
        self.M_score_direction_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)

        self.Ix_score_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))
        self.Ix_score_matrix[0, :] = 0.0
        self.Ix_score_matrix[:, 0] = 0.0
        self.Ix_score_direction_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))

        self.Iy_score_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)
        self.Iy_score_matrix[0, :] = 0.0
        self.Iy_score_matrix[:, 0] = 0.0
        self.Iy_score_direction_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)

        print(self.M_score_matrix)

        # Start with (1,1)
        self.update(row=1, col=1)
        print(self.M_score_matrix)
        print(self.M_score_direction_matrix)


    def update(self, row, col):
        """
        Method to update the matrices at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """
        self.update_m(row, col)
        self.update_ix(row, col)
        self.update_iy(row, col)

    def update_m(self, row, col):
        ### TO-DO! FILL IN ###

        match_matrix = pd.DataFrame(self.align_params.match_matrix)
        seq_A = self.align_params.seq_a
        seq_B = self.align_params.seq_b
        score_record = match_matrix[match_matrix["seq_A_residue"] == seq_A[row]]
        score_record = score_record[match_matrix["seq_B_residue"] == seq_B[col]]
        print("\n")
        s_ij_match = float(list(score_record["score"])[0])
        print(s_ij_match)

        M_score_matrix = self.M_score_matrix
        M_score_direction_matrix = self.M_score_direction_matrix

        score_from_M = self.M_score_matrix[row-1, col-1] + s_ij_match
        score_from_Ix = self.Ix_score_matrix[row-1, col-1] + s_ij_match
        score_from_Iy = self.Iy_score_matrix[row-1, col-1] + s_ij_match

        max_score = max(score_from_M, score_from_Ix, score_from_Iy)
        M_score_matrix[row, col] = max_score
        self.M_score_matrix = M_score_matrix

        if type(M_score_direction_matrix[row, col]) != list:
            M_score_direction_matrix[row, col] = list()

        if fuzzy_equals(score_from_M, max_score):
            pointers = M_score_direction_matrix[row, col]
            pointers.append("M")
            M_score_direction_matrix[row, col] = pointers

        if fuzzy_equals(score_from_Ix, max_score):
            pointers = M_score_direction_matrix[row, col]
            pointers.append("Ix")
            M_score_direction_matrix[row, col] = pointers

        if fuzzy_equals(score_from_Iy, max_score):
            pointers = M_score_direction_matrix[row, col]
            pointers.append("Iy")
            M_score_direction_matrix[row, col] = pointers

        self.M_score_direction_matrix = M_score_direction_matrix


    def update_ix(self, row, col):
        ### TO-DO! FILL IN ###
        pass

    def update_iy(self, row, col):
        ### TO-DO! FILL IN ###
        pass

    def find_traceback_start(self):
        """
        Finds the location to start the traceback..
        Think carefully about how to set this up for local 

        Returns:
            (max_val, max_loc) where max_val is the best score
            max_loc is a set() containing tuples with the (i,j) location(s) to start the traceback
             (ex. [(1,2), (3,4)])
        """
        ### TO-DO! FILL IN ###

    def traceback(self): ### TO-DO! FILL IN additional arguments ###
        """
        Performs a traceback.
        Hint: include a way to printing the traceback path. This will be helpful for debugging!
           ex. M(5,4)->Iy(4,3)->M(4,2)->Ix(3,1)->Ix(2,1)->M(1,1)->M(0,0)


        """
        ### TO-DO! FILL IN ###
        pass


def write_output(self):
    ### TO-DO! FILL IN ###
    pass


def read_input_file(filename):
    input_params = {}

    with open(filename, 'r') as f:
        lines = f.readlines()

    # strip comments and empty lines
    clean = []
    for line in lines:
        if ';' in line:
            line = line.split(';')[0]
        line = line.strip()
        if line:
            clean.append(line)

    # grab the input_params
    input_params['seq_a'] = clean[0]
    input_params['seq_b'] = clean[1]

    # parse mode flag with validation
    mode = int(clean[2])
    if mode not in [0, 1]:
        raise ValueError(f"Invalid mode flag: {mode}. Must be 0 (global) or 1 (local)")
    input_params['global_alignment'] = (mode == 0)

    # gap penalties
    gaps = clean[3].split()
    input_params['dx'] = float(gaps[0])
    input_params['ex'] = float(gaps[1])
    input_params['dy'] = float(gaps[2])
    input_params['ey'] = float(gaps[3])

    # alphabets
    input_params['len_alphabet_a'] = int(clean[4])
    input_params['alphabet_a'] = clean[5]
    input_params['len_alphabet_b'] = int(clean[6])
    input_params['alphabet_b'] = clean[7]

    # match matrix as pandas DataFrame
    matrix_data = []
    for i in range(8, len(clean)):
        parts = clean[i].split()
        if len(parts) == 5:
            matrix_data.append({
                'row': int(parts[0]),
                'col': int(parts[1]),
                'seq_A_residue': parts[2],
                'seq_B_residue': parts[3],
                'score': float(parts[4])
            })

    expected_entries = input_params['len_alphabet_a'] * input_params['len_alphabet_b']
    if len(matrix_data) != expected_entries:
        raise ValueError(f"Expected {expected_entries} matrix entries but found {len(matrix_data)}")

    input_params['match_matrix'] = matrix_data
    return input_params


def print_input_params(input_params):
    for k, v in input_params.items():
        print("\n" + k + ":")
        print(v)


def main():

    # check that the file is being properly used
    if (len(sys.argv) !=3):
        print("Please specify an input file and an output file as args.")
        return
        
    # input variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(input_file)
    print(output_file)

    # create an align object and run
    align = Align(input_file, output_file)
    align.align()


if __name__=="__main__":
    main()
