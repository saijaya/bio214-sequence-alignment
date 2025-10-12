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

def print_pointer_matrix(pointer_matrix, name="Pointer Matrix"):
    """
    Print a pointer matrix as a pandas DataFrame.

    Args:
        pointer_matrix: numpy array containing pointer lists
        name: name of the matrix to display
    """
    print(f"\n{name}:")
    rows, cols = pointer_matrix.shape

    # Create a formatted version for display
    display_matrix = []
    for i in range(rows):
        row_data = []
        for j in range(cols):
            cell = pointer_matrix[i, j]
            if cell is None or (isinstance(cell, list) and len(cell) == 0):
                row_data.append("{--}")
            elif isinstance(cell, list):
                # Format list of pointers - extract just matrix names
                ptr_str = ",".join([p[0] if isinstance(p, list) else str(p) for p in cell])
                row_data.append(f"{{{ptr_str}}}")
            else:
                row_data.append(f"{{{str(cell)}}}")
        display_matrix.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(display_matrix,
                      columns=[str(j) for j in range(cols)],
                      index=[str(i) for i in range(rows)])

    print(df)
    print()


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
        self.seq_a = str(input_params_dict["seq_a"]).strip()
        self.seq_b = str(input_params_dict["seq_b"]).strip()
        self.global_alignment = bool(input_params_dict["global_alignment"])
        self.dx = float(input_params_dict["dx"])
        self.ex = float(input_params_dict["ex"])
        self.dy = float(input_params_dict["dy"])
        self.ey = float(input_params_dict["ey"])
        self.alphabet_a = str(input_params_dict["alphabet_a"])
        self.alphabet_b = str(input_params_dict["alphabet_b"])
        self.len_alphabet_a = int(input_params_dict["len_alphabet_a"])
        self.len_alphabet_b = int(input_params_dict["len_alphabet_b"])

        # Adding length of sequence inferred:
        self.len_seq_a = len(self.seq_a)
        self.len_seq_b = len(self.seq_b)

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
        self.s_matrix = None
        self.m_matrix = None
        self.ix_matrix = None
        self.iy_matrix = None
        self.global_alignments = list()

    def align(self):
        """
        Main method for running alignment.
        """
        print("DEBUG: === Starting alignment ===")

        # load the alignment parameters into the align_params object
        self.align_params.load_params_from_file(self.input_file)
        print(f"DEBUG: Seq A: {self.align_params.seq_a}, Seq B: {self.align_params.seq_b}")
        print(f"DEBUG: Mode: {'Global' if self.align_params.global_alignment else 'Local'}")

        # populate the score matrices based on the input parameters
        print("DEBUG: === Populating score matrices ===")
        self.populate_score_matrices()

        # perform a traceback and write the output to an output file
        print("Calling traceback")
        ### TO-DO! FILL IN ###
        self.traceback()

    def populate_score_matrices(self):
        """
        Method to populate the score matrices based on the data in align_params.
        Should call update(i,j) for each entry in the score matrices
        Note: You MUST initialize M, Ix, Iy in this function rather than elsewhere
        """

        ### TO-DO! FILL IN ###
        num_rows_in_score_matrices = self.align_params.len_seq_a+1
        num_columns_in_score_matrices = self.align_params.len_seq_b + 1
        print(f"DEBUG: Matrix size: {num_rows_in_score_matrices}x{num_columns_in_score_matrices}")

        self.m_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))
        self.m_matrix[0, :] = 0.0
        self.m_matrix[:, 0] = 0.0
        self.m_matrix_pointers = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)

        self.ix_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))
        self.ix_matrix[0, :] = 0.0
        self.ix_matrix[:, 0] = 0.0
        self.ix_matrix_pointers = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)

        self.iy_matrix = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices))
        self.iy_matrix[0, :] = 0.0
        self.iy_matrix[:, 0] = 0.0
        self.iy_matrix_pointers = np.empty((num_rows_in_score_matrices, num_columns_in_score_matrices), dtype=object)

        print(self.m_matrix)

        # Start with (1,1)
        self.update(row=1, col=1)

        for i in range(1, self.align_params.len_seq_a+1):
            for j in range(1, self.align_params.len_seq_b+1):
                self.update(row=i, col=j)

        print("\nfinal version of m_matrix:")
        print(self.m_matrix)

        print("\nfinal version of m_matrix_pointers:")
        print_pointer_matrix(self.m_matrix_pointers)

        print("\nfinal version of ix_matrix:")
        print(self.ix_matrix)

        print("\nfinal version of ix_matrix_pointers:")
        print_pointer_matrix(self.ix_matrix_pointers)

        print("\nfinal version of iy_matrix:")
        print(self.iy_matrix)

        print("\nfinal version of iy_matrix_pointers:")
        print_pointer_matrix(self.iy_matrix_pointers)

    def update(self, row, col):
        """
        Method to update the matrices at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """

        self.s_matrix = pd.DataFrame(self.align_params.match_matrix)

        print(f"DEBUG: -> update() ({row},{col})")
        print(f"DEBUG: -> subsequences: seq A [0:{row}] = '{self.align_params.seq_a[0:row]}', seq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        print(f"DEBUG: -> residues: Xi (seq_a[{row-1}]) = '{self.align_params.seq_a[row-1]}', Yj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")
        self.update_m(row, col)
        self.update_ix(row, col)
        self.update_iy(row, col)

    def update_m(self, row, col):
        ### TO-DO! FILL IN ###
        print(f"DEBUG:   update_m() M[{row},{col}]")
        print(f"DEBUG:   subsequences: -> seq A [0:{row}] = '{self.align_params.seq_a[0:row]}', seq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        print(f"DEBUG: -> residues: Xi (seq_a[{row-1}]) = '{self.align_params.seq_a[row-1]}', Yj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")

        s_matrix = self.s_matrix
        print("DEBUG: s_matrix:")
        print("DEBUG:", type(s_matrix))
        print("DEBUG:", s_matrix)
        seq_a = self.align_params.seq_a
        curr_residue_a = seq_a[row-1]
        print("Curr residue seq_a: "+ curr_residue_a)
        seq_b = self.align_params.seq_b
        curr_residue_b = seq_b[col-1]
        print("Curr residue seq_b: "+ curr_residue_b)

        s_matrix_slice = s_matrix[s_matrix["seq_A_residue"] == curr_residue_a]
        s_matrix_slice = s_matrix_slice[s_matrix["seq_B_residue"] == curr_residue_b]
        s_ij_match = float(list(s_matrix_slice["score"])[0])
        print(f"residue match score (from lookup match_matrix: {s_ij_match}")

        m_matrix = self.m_matrix

        score_from_m_matrix = self.m_matrix[row - 1, col - 1] + s_ij_match
        print(f"DEBUG:   Score from M[{row-1},{col-1}]: {self.m_matrix[row - 1, col - 1]:.2f} + {s_ij_match} = {score_from_m_matrix:.2f}")
        score_from_ix_matrix = self.ix_matrix[row - 1, col - 1] + s_ij_match
        print(f"DEBUG:   Score from Ix[{row-1},{col-1}]: {self.ix_matrix[row - 1, col - 1]:.2f} + {s_ij_match} = {score_from_ix_matrix:.2f}")
        score_from_iy_matrix = self.iy_matrix[row - 1, col - 1] + s_ij_match
        print(f"DEBUG:   Score from Iy[{row-1},{col-1}]: {self.iy_matrix[row - 1, col - 1]:.2f} + {s_ij_match} = {score_from_iy_matrix:.2f}")

        max_score = max(score_from_m_matrix, score_from_ix_matrix, score_from_iy_matrix)
        print(f"DEBUG:   max_score chosen: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        print(f"global_alignment: ", global_alignment)
        print(f"final_max_score: ", final_max_score)

        m_matrix[row, col] = final_max_score
        self.m_matrix = m_matrix
        print("udpated m_matrix:")
        print(m_matrix)

        m_matrix_pointers = self.m_matrix_pointers

        if type(m_matrix_pointers[row, col]) != list:
            m_matrix_pointers[row, col] = list()

        if global_alignment is False:
            print("global alignment is False")
            if fuzzy_equals(0.0, final_max_score) is True:
                print("final_max_score is also 0. return update_m()")
                return

        if fuzzy_equals(score_from_m_matrix, max_score):
            pointers = m_matrix_pointers[row, col]
            pointers.append(["M", row-1, col-1])
            m_matrix_pointers[row, col] = pointers

        if fuzzy_equals(score_from_ix_matrix, max_score):
            pointers = m_matrix_pointers[row, col]
            pointers.append(["Ix", row-1, col-1])
            m_matrix_pointers[row, col] = pointers

        if fuzzy_equals(score_from_iy_matrix, max_score):
            pointers = m_matrix_pointers[row, col]
            pointers.append(["Iy", row-1, col-1])
            m_matrix_pointers[row, col] = pointers

        self.m_matrix_pointers = m_matrix_pointers
        print(f"DEBUG:   M[{row},{col}] = {final_max_score:.2f}, pointers: {m_matrix_pointers[row, col]}")

    def update_ix(self, row, col):
        ### TO-DO! FILL IN ###
        print(f"DEBUG:   update_ix() Ix[{row},{col}]")
        print("GAP IN B")
        print(f"DEBUG:   subsequences: -> seq A [0:{row-1}] = '{self.align_params.seq_a[0:row-1]}', seq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        print(f"DEBUG: -> residues: Xi (seq_a[{row-2}]) = '{self.align_params.seq_a[row-2]}', Yj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")

        seq_a = self.align_params.seq_a
        curr_residue_a = seq_a[row-2]
        print("Curr residue seq_a: "+ curr_residue_a)
        seq_b = self.align_params.seq_b
        curr_residue_b = seq_b[col-1]
        print("Curr residue seq_b: "+ curr_residue_b)

        s_matrix = self.s_matrix
        print("DEBUG: s_matrix:")
        print("DEBUG:", type(s_matrix))
        print("DEBUG:", s_matrix)

        m_matrix = self.m_matrix
        print("DEBUG: m_matrix:")
        print("DEBUG:", type(m_matrix))
        print("DEBUG:", m_matrix)

        ix_matrix = self.ix_matrix
        print("DEBUG: ix_matrix:")
        print("DEBUG:", type(ix_matrix))
        print("DEBUG:", ix_matrix)

        dy = self.align_params.dy
        print(f"dy = {dy}")
        ey = self.align_params.ey
        print(f"ey = {ey}")

        score_from_m_matrix = m_matrix[row-1, col] - dy
        print(f"score_from_m_matrix: {score_from_m_matrix}")
        score_from_ix_matrix = ix_matrix[row-1, col] -ey
        print(f"score_from_ix_matrix: {score_from_ix_matrix}")

        max_score = max(score_from_m_matrix, score_from_ix_matrix)
        print(f"DEBUG:   max_score chosen: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        print(f"global_alignment: ", global_alignment)
        print(f"final_max_score: ", final_max_score)

        ix_matrix[row, col] = final_max_score
        self.ix_matrix = ix_matrix
        print("updated ix_matrix:")
        print(ix_matrix)

        ix_matrix_pointers = self.ix_matrix_pointers

        if type(ix_matrix_pointers[row, col]) != list:
            ix_matrix_pointers[row, col] = list()

        if global_alignment is False:
            print("global alignment is False")
            if fuzzy_equals(0.0, final_max_score) is True:
                print("final_max_score is also 0. return update_ix()")
                return

        if fuzzy_equals(score_from_m_matrix, max_score):
            pointers = ix_matrix_pointers[row, col]
            pointers.append(["M", row-1, col])
            ix_matrix_pointers[row, col] = pointers

        if fuzzy_equals(score_from_ix_matrix, max_score):
            pointers = ix_matrix_pointers[row, col]
            pointers.append(["Ix", row-1, col])
            ix_matrix_pointers[row, col] = pointers

        self.ix_matrix_pointers = ix_matrix_pointers
        print(f"DEBUG:   Ix[{row},{col}] = {final_max_score:.2f}, pointers: {ix_matrix_pointers[row, col]}")

    def update_iy(self, row, col):
        ### TO-DO! FILL IN ###
        print(f"DEBUG:   update_iy() Iy[{row},{col}]")
        print("GAP IN A")
        print(
            f"DEBUG:   subsequences: -> seq A [0:{row}] = '{self.align_params.seq_a[0:row]}', seq B [0:{col-1}] = '{self.align_params.seq_b[0:col-1]}'")
        print(
            f"DEBUG: -> residues: Xi (seq_a[{row - 1}]) = '{self.align_params.seq_a[row - 1]}', Yj (seq_b[{col - 2}]) = '{self.align_params.seq_b[col - 2]}'")

        seq_a = self.align_params.seq_a
        curr_residue_a = seq_a[row - 1]
        print("Curr residue seq_a: " + curr_residue_a)
        seq_b = self.align_params.seq_b
        curr_residue_b = seq_b[col - 2]
        print("Curr residue seq_b: " + curr_residue_b)

        s_matrix = self.s_matrix
        print("DEBUG: s_matrix:")
        print("DEBUG:", type(s_matrix))
        print("DEBUG:", s_matrix)

        m_matrix = self.m_matrix
        print("DEBUG: m_matrix:")
        print("DEBUG:", type(m_matrix))
        print("DEBUG:", m_matrix)

        iy_matrix = self.iy_matrix
        print("DEBUG: iy_matrix:")
        print("DEBUG:", type(iy_matrix))
        print("DEBUG:", iy_matrix)

        dx = self.align_params.dx
        print(f"dx = {dx}")
        ex = self.align_params.ex
        print(f"ex = {ex}")

        score_from_m_matrix = m_matrix[row, col-1] - dx
        print(f"score_from_m_matrix: {score_from_m_matrix}")
        score_from_iy_matrix = iy_matrix[row, col-1] -ex
        print(f"score_from_iy_matrix: {score_from_iy_matrix}")

        max_score = max(score_from_m_matrix, score_from_iy_matrix)
        print(f"DEBUG:   max_score chosen: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        print(f"global_alignment: ", global_alignment)
        print(f"final_max_score: ", final_max_score)

        iy_matrix[row, col] = final_max_score
        self.iy_matrix = iy_matrix
        print("updated iy_matrix:")
        print(iy_matrix)

        iy_matrix_pointers = self.iy_matrix_pointers

        if type(iy_matrix_pointers[row, col]) != list:
            iy_matrix_pointers[row, col] = list()

        if global_alignment is False:
            print("global alignment is False")
            if fuzzy_equals(0.0, final_max_score) is True:
                print("final_max_score is also 0. return update_ix()")
                return

        if fuzzy_equals(score_from_m_matrix, max_score):
            pointers = iy_matrix_pointers[row, col]
            pointers.append(["M", row, col-1])
            iy_matrix_pointers[row, col] = pointers

        if fuzzy_equals(score_from_iy_matrix, max_score):
            pointers = iy_matrix_pointers[row, col]
            pointers.append(["Iy", row, col-1])
            iy_matrix_pointers[row, col] = pointers

        self.iy_matrix_pointers = iy_matrix_pointers
        print(f"DEBUG:   Iy[{row},{col}] = {final_max_score:.2f}, pointers: {iy_matrix_pointers[row, col]}")

    def find_traceback_start(self):
        """
        Finds the location to start the traceback..
        Think carefully about how to set this up for local 

        Returns:
            (max_val, max_loc) where max_val is the best score
            max_loc is a set() containing tuples with the (i,j) location(s) to start the traceback
             (ex. [(1,2), (3,4)])
        """
        print("DEBUG: Finding traceback start...")
        ### TO-DO! FILL IN ###
        if self.align_params.global_alignment is True:
            print("DEBUG: Global alignment - looking for max in last row/column")
            max_m_matrix = max(self.m_matrix[self.align_params.len_seq_a:].max(), self.m_matrix[:self.align_params.len_seq_b].max())
            print(f"DEBUG:   Max from M matrix edges: {max_m_matrix}")
            max_ix_matrix = max(self.ix_matrix[self.align_params.len_seq_a:].max(), self.ix_matrix[:self.align_params.len_seq_b].max())
            print(f"DEBUG:   Max from Ix matrix edges: {max_ix_matrix}")
            max_iy_matrix = max(self.iy_matrix[self.align_params.len_seq_a:].max(), self.iy_matrix[:self.align_params.len_seq_b].max())
            print(f"DEBUG:   Max from Iy matrix edges: {max_iy_matrix}")

            max_of_maxes = max(max_m_matrix, max_ix_matrix, max_iy_matrix)
            print(f"DEBUG:   Overall max score: {max_of_maxes}")
            print(f"DEBUG:   Starting traceback from position: ({self.align_params.len_seq_a}, {self.align_params.len_seq_b})")

            return max_of_maxes, (self.align_params.len_seq_a, self.align_params.len_seq_b)

    def traceback_cell(self, curr_cell_score_matrix_letter, row, col, input_alignments=None, pointer_history=None):

        seq_a = self.align_params.seq_a
        seq_b = self.align_params.seq_b

        if input_alignments is None:
            input_alignments = []

        if pointer_history is None:
            pointer_history = []

        print(f"\n<<<<<<<<<<<<<<<<NOW STARTING TRACEBACK IN CELL: {curr_cell_score_matrix_letter} ({row}, {col})>>>>>>>>>>>>>>>>")

        print(f"\nDEBUG: === Traceback cell {curr_cell_score_matrix_letter}[{row},{col}] ===")
        print(f"DEBUG:   Current matrix: {curr_cell_score_matrix_letter}")
        print(f"DEBUG:   Position: ({row}, {col})")
        print(f"DEBUG:   Input alignments so far: {len(input_alignments)} path(s)")
        print_pointer_history = "--->".join(
            [str(p[0]) + "(" + str(p[1]) + "," + str(p[2]) + ")" for p in pointer_history])
        print(f"Input pointer history: {print_pointer_history}")
        
        print(f"DEBUG: INCOMING ALIGNMENTS (reversed for readability):")
        if len(input_alignments) == 0:
            print(f"DEBUG:   (empty - no alignments yet)")
        else:
            for align_idx, alignment in enumerate(input_alignments):
                print(f"DEBUG:   Alignment {align_idx+1}:")
                print(f"DEBUG:     Seq A: {''.join(reversed(alignment[0]))}")
                print(f"DEBUG:     Seq B: {''.join(reversed(alignment[1]))}")
                print()

        if curr_cell_score_matrix_letter == "M":
            pointers_from_curr_cell_matrix = self.m_matrix_pointers
        elif curr_cell_score_matrix_letter == "Ix":
            pointers_from_curr_cell_matrix = self.ix_matrix_pointers
        elif curr_cell_score_matrix_letter == "Iy":
            pointers_from_curr_cell_matrix = self.iy_matrix_pointers
        else:
            print("DEBUG: ERROR - Invalid matrix name!")
            return

        print("pointers_from_curr_cell_matrix:")
        print_pointer_matrix(pointers_from_curr_cell_matrix)
        pointers_from_curr_cell = pointers_from_curr_cell_matrix[row, col]
        print(f"pointers_from_curr_cell: {pointers_from_curr_cell}")

        if pointers_from_curr_cell is None or len(pointers_from_curr_cell) == 0:
            print("<<<<<<<<<<<<<<<<<RECURSION END CASE. ADDING TO GLOBAL ALIGNMENTS>>>>>>>>>>>>>>>>>>")
            print(f"Input pointer history: {print_pointer_history}")
            print(f"input_alignments:")
            for alignment in input_alignments:
                print("\n")
                print(alignment[0])
                print(alignment[1])

            global_alignments = self.global_alignments
            print(f"global_alignments BEFORE update:")
            for alignment in self.global_alignments:
                print("\n")
                print(alignment[0])
                print(alignment[1])
            global_alignments.append(input_alignments)
            self.global_alignments = global_alignments
            print(f"global_alignments AFTER update:")
            for alignment in self.global_alignments:
                print("\n")
                print(alignment[0])
                print(alignment[1])

        else:
            num_pointers_from_curr_cell = len(pointers_from_curr_cell)

            # for each pointer:
            # update alignment based on direction of pointer
            # M --> both curr residues added to all existing alignments in input alignments
            # Ix --> Gap in B. include residue from seq_a
            # Iy --> Gap in A. Include residue from seq_b
            # Once updated, call next cell with updated input alignment and next cell details from pointer
            print(f"Looping through {num_pointers_from_curr_cell} pointers")
            for idx, pointer in enumerate(pointers_from_curr_cell):
                print(f"\npointer {idx+1}/{num_pointers_from_curr_cell}")
                print(f"pointer: {pointer}")
                pointer_history.append([curr_cell_score_matrix_letter, row, col])
                print_pointer_history = "--->".join([str(p[0]) + "(" + str(p[1]) + "," + str(p[2]) + ")" for p in pointer_history])
                print(f"Updated pointer history: {print_pointer_history}")

                pointer_letter = pointer[0]
                pointer_row = pointer[1]
                pointer_col = pointer[2]

                updated_input_alignments = list()
                print(f"seq_a: {seq_a}")
                print(f"seq_b: {seq_b}")

                if pointer_letter == "M":
                    residue_to_append_to_seq_a = seq_a[row-1]
                    print(f"residue_to_append_to_seq_a = seq_a[{row - 1}]: {residue_to_append_to_seq_a}")
                    residue_to_append_to_seq_b = seq_b[col-1]
                    print(f"residue_to_append_to_seq_b = seq_b[{col - 1}]: {residue_to_append_to_seq_b}")

                    print(f"pointer_letter is {pointer_letter}-> No gap: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")

                elif pointer_letter == "Ix":
                    residue_to_append_to_seq_a = seq_a[row - 1]
                    print(f"residue_to_append_to_seq_a = seq_a[{row - 1}]: {residue_to_append_to_seq_a}")

                    residue_to_append_to_seq_b = "_"
                    print(f"residue_to_append_to_seq_b = - : {residue_to_append_to_seq_b}")

                    print(f"pointer_letter is {pointer_letter}-> gap in B: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")

                elif pointer_letter == "Iy":
                    residue_to_append_to_seq_a = "-"
                    print(f"residue_to_append_to_seq_a = - : {residue_to_append_to_seq_a}")

                    residue_to_append_to_seq_b = seq_b[col - 1]
                    print(f"residue_to_append_to_seq_a = seq_b[{col - 1}]: {residue_to_append_to_seq_b}")

                    print(f"pointer_letter is {pointer_letter}-> gap in A: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")

                else:
                    print("DEBUG: ERROR - Invalid pointer_letter!")
                    return

                if len(input_alignments) == 0:
                    updated_input_alignments = [[[residue_to_append_to_seq_a], [residue_to_append_to_seq_b]]]
                    self.traceback_cell(pointer_letter, pointer_row, pointer_col, updated_input_alignments, pointer_history)

                else:
                    # Update all input alignments with latest residue based on pointer
                    print(f"DEBUG: UPDATING ALIGNMENTS - adding '{residue_to_append_to_seq_a}' and '{residue_to_append_to_seq_b}':")
                    for input_alignment in input_alignments:
                        print(f"~~Input alignement before update: {input_alignment}")
                        print(f"DEBUG:   Before update (reversed):")
                        print(f"DEBUG:     Seq A: {''.join(reversed(input_alignment[0]))}")
                        print(f"DEBUG:     Seq B: {''.join(reversed(input_alignment[1]))}")

                        input_alignment_seq_a: list = input_alignment[0]
                        input_alignment_seq_a.append(residue_to_append_to_seq_a)

                        input_alignment_seq_b = input_alignment[1]
                        input_alignment_seq_b.append(residue_to_append_to_seq_b)

                        print(f"DEBUG:   After update (reversed):")
                        print(f"DEBUG:     Seq A: {''.join(reversed(input_alignment_seq_a))}")
                        print(f"DEBUG:     Seq B: {''.join(reversed(input_alignment_seq_b))}")
                        print()

                        updated_input_alignments.append([input_alignment_seq_b, input_alignment_seq_b])

                        self.traceback_cell(pointer_letter, pointer_row, pointer_col, updated_input_alignments, pointer_history)

    def traceback(self): ### TO-DO! FILL IN additional arguments ###
        """
        Performs a traceback.
        Hint: include a way to printing the traceback path. This will be helpful for debugging!
           ex. M(5,4)->Iy(4,3)->M(4,2)->Ix(3,1)->Ix(2,1)->M(1,1)->M(0,0)


        """
        print("\nDEBUG: ========== STARTING TRACEBACK ==========")
        ### TO-DO! FILL IN ###
        max_val, max_location = self.find_traceback_start()
        print(f"DEBUG: Starting from M[{max_location[0]},{max_location[1]}] with score {max_val}")
        
        self.traceback_cell("M", max_location[0], max_location[1])
        
        print(f"\nDEBUG: ========== TRACEBACK COMPLETE ==========")
        print(f"DEBUG: Found {len(self.global_alignments)} optimal alignment(s)")
        
        for idx, alignment in enumerate(self.global_alignments):
            print(f"\nDEBUG: Alignment {idx+1}:")
            print(f"DEBUG:   Seq A: {''.join(alignment[0])}")
            print(f"DEBUG:   Seq B: {''.join(alignment[1])}")


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

    print(f"input_file: {input_file}")
    print(f"output_file: {output_file}")

    # create an align object and run
    align = Align(input_file, output_file)
    align.align()

if __name__=="__main__":
    main()
