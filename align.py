
"""

This file provides skeleton code for align.py. 

Locations with "FILL IN" in comments are where you need to add code.

Note - you MUST follow this structure or else the autograder will not run properly

Usage: python align.py input_file output_file

"""


import sys


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
        ### TO-DO! FILL IN ###



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
        pass

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
    data = {}

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

    # grab the data
    data['seq_a'] = clean[0]
    data['seq_b'] = clean[1]
    data['global_alignment'] = (int(clean[2]) == 0)

    # gap penalties
    gaps = clean[3].split()
    data['dx'] = float(gaps[0])
    data['ex'] = float(gaps[1])
    data['dy'] = float(gaps[2])
    data['ey'] = float(gaps[3])

    # alphabets
    data['len_alphabet_a'] = int(clean[4])
    data['alphabet_a'] = clean[5]
    data['len_alphabet_b'] = int(clean[6])
    data['alphabet_b'] = clean[7]

    # match matrix
    data['match_matrix_entries'] = []
    for i in range(8, len(clean)):
        parts = clean[i].split()
        if len(parts) == 5:
            data['match_matrix_entries'].append({
                'row': int(parts[0]),
                'col': int(parts[1]),
                'char_a': parts[2],
                'char_b': parts[3],
                'score': float(parts[4])
            })

    return data


def print_data(data):
    print("seq_a:", data['seq_a'])
    print("seq_b:", data['seq_b'])
    print("global:", data['global_alignment'])
    print("gaps:", data['dx'], data['ex'], data['dy'], data['ey'])
    print("alphabets:", data['alphabet_a'], data['alphabet_b'])
    print("matrix entries:", len(data['match_matrix_entries']))
    for entry in data['match_matrix_entries']:
        print(f"  {entry['char_a']} {entry['char_b']}: {entry['score']}")


def main():

    # check that the file is being properly used
    if (len(sys.argv) !=3):
        print("Please specify an input file and an output file as args.")
        return
        
    # input variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # create an align object and run
    # align = Align(input_file, output_file)
    # align.align()

    print(input_file)
    print(output_file)

    data = read_input_file(input_file)
    print(data)




if __name__=="__main__":
    main()
