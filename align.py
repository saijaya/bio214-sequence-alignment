"""

This file provides skeleton code for align.py. 

Locations with "FILL IN" in comments are where you need to add code.

Note - you MUST follow this structure or else the autograder will not run properly

Usage: python align.py input_file output_file

"""


import sys
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
        self.matrix = {}

    def set_score(self, a, b, score):
        """
        Updates or adds a score for a specified match

        Inputs:
           a = the character from sequence A
           b = the character from sequence B
           score = the score to set it for
        """
        if a not in self.matrix:
            self.matrix[a] = {}

        self.matrix[a][b] = score

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
        return self.matrix[a][b]


class ScoreCell(object):
    def __init__(self):
        self.score = 0
        self.pointers = list()

    def set_cell_score(self, score):
        self.score = score

    def get_cell_score(self):
        return self.score

    def add_cell_pointer(self, pointer_tuple):
        self.pointers.append(pointer_tuple)

    def get_cell_pointers(self):
        return self.pointers


class ScoreMatrix(object):
    """
    Object to store a score matrix, which generated during the alignment process. The score matrix consists of a 2-D array of
    ScoreEntries that are updated during alignment and used to output the maximum alignment.
    """

    def __init__(self, name, nrow, ncol):
        assert name in ["M", "Ix", "Iy"], "Invalid score matrix name"
        self.name = name  # identifier for the score matrix - Ix, Iy, or M
        self.nrow = nrow
        self.ncol = ncol
        self.score_matrix = np.empty((nrow, ncol), dtype=ScoreCell)
        for i in range(nrow):
            for j in range(ncol):
                self.score_matrix[i, j] = ScoreCell()
        # you need to figure out a way to represent this and how to initialize
        # Hint: it may be helpful to have an object for each entry

    def get_score(self, row, col):
        ### TO-DO! FILL IN ###
        return self.score_matrix[row, col].get_cell_score()

    def set_score(self, row, col, score):    
        ### TO-DO! FILL IN ###
        self.score_matrix[row, col].set_cell_score(score=score)

    def get_pointers(self, row, col):
        """
        Returns the indices of the entries that are pointed to
        This should be formatted as a list of tuples:
         ex. [(1,1), (1,0)]
        """
        ### TO-DO! FILL IN ###
        return self.score_matrix[row, col].get_cell_pointers()

    def set_pointers(self, row, col, pointer: list): ### TO-DO! FILL IN - this needs additional arguments ###
        ### TO-DO! FILL IN ###
        assert len(pointer) == 3, "invalid pointer"
        curr_pointers = self.score_matrix[row, col].get_cell_pointers()
        curr_pointers.append(pointer)

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

        # I took some inspiration for this print code so it looks pretty and well spaced
        # ~print(f"\n{self.name} Scores:")
        rows, cols = self.nrow, self.ncol

        # Column header
        header = "     " + "".join([f"{j:>8}" for j in range(cols)])
        # ~print(header)
        
        # Print row
        for i in range(rows):
            row_str = f"{i:>3}: "
            for j in range(cols):
                score_value = self.get_score(i, j)
                row_str += f"{score_value:>8.1f}"
            # ~print(row_str)
        # ~print()

    def print_pointers(self):
        """
        Returns a nicely formatted string containing the pointers for each entry in the score matrix. Use this for debugging!
        """
        # I took some inspiration for this print code so it looks pretty and well spaced
        # ~print(f"\n{self.name} Pointers:")
        rows, cols = self.nrow, self.ncol

        # Create column headers
        header = "     " + "".join([f"{j:>8}" for j in range(cols)])
        # ~print(header)
        
        # Print each row
        for i in range(rows):
            row_str = f"{i:>3}: "
            for j in range(cols):
                cell = self.get_pointers(i, j)
                if cell is None or (isinstance(cell, list) and len(cell) == 0):
                    cell_str = "{}"
                elif isinstance(cell, list):
                    # Format list of pointers - extract just matrix names
                    ptr_str = ",".join([p[0] if isinstance(p, list) else str(p) for p in cell])
                    cell_str = f"{{{ptr_str}}}"
                else:
                    cell_str = f"{{{str(cell)}}}"
                row_str += f"{cell_str:>8}"
            # ~print(row_str)
        # ~print()


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
        # ~print("<<<<<<<<<<<<<<<<<<<<<<ALIGN PARAMS LOAD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

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

        self.match_matrix_df = input_params_dict["match_matrix"]
        for entry in input_params_dict["match_matrix"]:
            self.match_matrix.set_score(entry["seq_A_residue"], entry["seq_B_residue"], entry["score"])


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
        self.universal_alignments_bucket = list()

    def align(self):
        """
        Main method for running alignment.
        """
        # ~print("<<<<<<<<<<<<<<<<<<<<<<ALIGN START>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # load the alignment parameters into the align_params object
        self.align_params.load_params_from_file(self.input_file)
        # ~print(f"Seq A: {self.align_params.seq_a}, Seq B: {self.align_params.seq_b}")
        # ~print(f"Global/ Local: {'Global' if self.align_params.global_alignment else 'Local'}")

        # populate the score matrices based on the input parameters
        self.populate_score_matrices()

        # perform a traceback and write the output to an output file
        # ~print("Calling traceback")
        self.traceback()

    def populate_score_matrices(self):
        """
        Method to populate the score matrices based on the data in align_params.
        Should call update(i,j) for each entry in the score matrices
        Note: You MUST initialize M, Ix, Iy in this function rather than elsewhere
        """
        # ~print("<<<<<<<<<<<<<<<<<<<<<<~~~POPULATE SCORE MATRIX>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        num_rows_in_score_matrices = self.align_params.len_seq_a+1
        num_columns_in_score_matrices = self.align_params.len_seq_b + 1
        # ~print(f"Matrix size: {num_rows_in_score_matrices}x{num_columns_in_score_matrices}")

        # ~print("!!Initializing ScoreMatrix")
        self.m_matrix = ScoreMatrix("M", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.m_matrix.set_score(i, 0, 0.0)

        for j in range(num_columns_in_score_matrices):
            self.m_matrix.set_score(0, j, 0.0)

        # ~print("\nself.m_matrix:")
        # self.m_matrix.print_scores()
        # self.m_matrix.print_pointers()

        self.ix_matrix = ScoreMatrix("Ix", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.ix_matrix.set_score(i, 0, 0.0)

        for j in range(num_columns_in_score_matrices):
            self.ix_matrix.set_score(0, j, 0.0)

        # ~print("\nself.ix_matrix:")
        # self.ix_matrix.print_scores()
        # self.ix_matrix.print_pointers()

        self.iy_matrix = ScoreMatrix("Iy", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.iy_matrix.set_score(i, 0, 0.0)

        for j in range(num_columns_in_score_matrices):
            self.iy_matrix.set_score(0, j, 0.0)

        # ~print("\nself.iy_matrix:")
        # self.iy_matrix.print_scores()
        # self.iy_matrix.print_pointers()
        
        for i in range(1, self.align_params.len_seq_a+1):
            for j in range(1, self.align_params.len_seq_b+1):
                self.update(row=i, col=j)

        # ~print("\nfinal version of m_matrix:")
        # # ~print(self.m_matrix)
        # self.m_matrix.print_scores()

        # ~print("\nfinal version of m_matrix_pointers:")
        # self.m_matrix.print_pointers()

        # ~print("\nfinal version of ix_matrix:")
        # # ~print(self.ix_matrix)
        # self.ix_matrix.print_scores()

        # ~print("\nfinal version of ix_matrix_pointers:")
        # self.ix_matrix.print_pointers()

        # ~print("\nfinal version of iy_matrix:")
        # # ~print(self.iy_matrix)
        # self.iy_matrix.print_scores()

        # ~print("\nfinal version of iy_matrix_pointers:")
        # self.iy_matrix.print_pointers()

    def update(self, row, col):
        """
        Method to update the matrices at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """
        # ~print(f"\n\n<<<<<<<<<<<<<inside update({row},{col})>>>>>>>>>>>>>>>>>")
        # ~print(f"seq A: {self.align_params.seq_a}")
        # ~print(f"seq B: {self.align_params.seq_b}")
        # ~print(f"considering subsequences: \nseq A [0:{row}] = '{self.align_params.seq_a[0:row]}', \nseq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        # ~print(f"considering residues: \nXi (seq_a[{row-1}]) = '{self.align_params.seq_a[row-1]}', \nYj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")

        self.update_m(row, col)
        self.update_ix(row, col)
        self.update_iy(row, col)
        # ~print(f"<<<<<<<<<<update complete ({row},{col})>>>>>>>>>>>>>>")

    def update_m(self, row, col):
        # ~print(f"\n<<<<<<<<<<<<<inside update_m({row},{col})>>>>>>>>>>>>>>>>>")
        # ~print(f"seq A: {self.align_params.seq_a}")
        # ~print(f"seq B: {self.align_params.seq_b}")
        # ~print(f"considering subsequences: \nseq A [0:{row}] = '{self.align_params.seq_a[0:row]}', \nseq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        # ~print(f"considering residues: \nXi (seq_a[{row-1}]) = '{self.align_params.seq_a[row-1]}', \nYj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")

        seq_a = self.align_params.seq_a
        curr_residue_a = seq_a[row-1]
        # ~print(f"current last residue seq_a: {curr_residue_a}")
        seq_b = self.align_params.seq_b
        curr_residue_b = seq_b[col-1]
        # ~print(f"current last residue seq_b: {curr_residue_b}")

        s_ij_match = self.align_params.match_matrix.get_score(curr_residue_a, curr_residue_b)
        # ~print(f"residue match score (from lookup match_matrix: {s_ij_match}")

        # in order to update score in current cell, we need max of 3 scores
        # ~print("in order to update score in current cell, we need max of 3 scores")
        score_from_m_matrix = self.m_matrix.get_score(row - 1, col - 1) + s_ij_match
        # ~print(f"score from m_matrix: M[{row-1},{col-1}]: {self.m_matrix.get_score(row - 1, col - 1):.2f} + {s_ij_match} = {score_from_m_matrix:.2f}")
        # ~print("m_matrix:")
        # self.m_matrix.print_scores()
        score_from_ix_matrix = self.ix_matrix.get_score(row - 1, col - 1) + s_ij_match
        # ~print(f"score from ix_matrix: Ix[{row-1},{col-1}]: {self.ix_matrix.get_score(row - 1, col - 1):.2f} + {s_ij_match} = {score_from_ix_matrix:.2f}")
        # ~print("ix_matrix:")
        # self.ix_matrix.print_scores()
        score_from_iy_matrix = self.iy_matrix.get_score(row - 1, col - 1) + s_ij_match
        # ~print(f"score from iy_matrix: Iy[{row-1},{col-1}]: {self.iy_matrix.get_score(row - 1, col - 1):.2f} + {s_ij_match} = {score_from_iy_matrix:.2f}")
        # ~print("iy_matrix:")
        # self.iy_matrix.print_scores()

        max_score = max(score_from_m_matrix, score_from_ix_matrix, score_from_iy_matrix)
        # ~print(f"max_score of 3 scores: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        # ~print(f"global_alignment: ", global_alignment)
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        # ~print(f"final_max_score: ", final_max_score)

        self.m_matrix.set_score(row, col, final_max_score)
        # ~print("udpated m_matrix:")
        # self.m_matrix.print_scores()

        # ~print(f"<<<<<<<<<<m_matrix cell value updated ({row},{col})>>>>>>>>>>>>>>")

        # If local alignment and final_score is 0.0, no pointers
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            # ~print("local alginment. cell score 0.0. no pointers from cell")
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                # ~print(f"adding [M, {row-1}, {col-1}]")
                self.m_matrix.set_pointers(row, col, ["M", row-1, col-1])

            if fuzzy_equals(score_from_ix_matrix, max_score):
                # ~print(f"adding [Ix, {row-1}, {col-1}]")
                self.m_matrix.set_pointers(row, col, ["Ix", row - 1, col - 1])

            if fuzzy_equals(score_from_iy_matrix, max_score):
                # ~print(f"adding [Iy, {row-1}, {col-1}]")
                self.m_matrix.set_pointers(row, col, ["Iy", row - 1, col - 1])

        # ~print(f"final score in m_matrix cell: M[{row},{col}] = {self.m_matrix.get_score(row, col):.2f}")
        # ~print(f"final pointers in m_matrix_pointers cell: M[{row},{col}] = pointers: {self.m_matrix.get_pointers(row, col)}")
        # ~print(f"<<<<<<<<<<m_matrix cell pointers updated ({row},{col})>>>>>>>>>>>>>>")

    def update_ix(self, row, col):

        # ~print(f"\n<<<<<<<<<<<<<inside update_ix({row},{col})>>>>>>>>>>>>>>>>>")
        # ~print("GAP IN B")
        # ~print(f"seq A: {self.align_params.seq_a}")
        # ~print(f"seq B: {self.align_params.seq_b}")
        # ~print(f"considering subsequences: \nseq A [0:{row-1}] = '{self.align_params.seq_a[0:row-1]}', \nseq B [0:{col}] = '{self.align_params.seq_b[0:col]}'")
        # ~print(f"considering residues: \nXi (seq_a[{row-2}]) = '{self.align_params.seq_a[row-2]}', \nYj (seq_b[{col-1}]) = '{self.align_params.seq_b[col-1]}'")

        # seq_a = self.align_params.seq_a
        # curr_residue_a = seq_a[row-2]
        # ~print("current last residue seq_a: " + curr_residue_a)
        # seq_b = self.align_params.seq_b
        # curr_residue_b = seq_b[col-1]
        # ~print("current last residue seq_b: " + curr_residue_b)

        dy = self.align_params.dy
        # ~print(f"dy = {dy}")
        ey = self.align_params.ey
        # ~print(f"ey = {ey}")

        # ~print("self.m_matrix:")
        # self.m_matrix.print_scores()

        # ~print("before update ix_matrix:")
        # self.ix_matrix.print_pointers()

        # ~print("in order to update score in current cell, we need max of 2 scores")
        score_from_m_matrix = self.m_matrix.get_score(row-1, col) - dy
        # ~print(f"score from m_matrix: M[{row-1},{col}]: {self.m_matrix.get_score(row - 1, col):.2f} - {dy} = {score_from_m_matrix:.2f}")

        score_from_ix_matrix = self.ix_matrix.get_score(row-1, col) - ey
        # ~print(f"score from ix_matrix: Ix[{row-1},{col}]: {self.ix_matrix.get_score(row - 1, col):.2f} - {ey} = {score_from_ix_matrix:.2f}")

        max_score = max(score_from_m_matrix, score_from_ix_matrix)
        # ~print(f"max_score chosen: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        # ~print(f"global_alignment: ", global_alignment)
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        # ~print(f"final_max_score: ", final_max_score)

        self.ix_matrix.set_score(row, col, final_max_score)
        # ~print("updated ix_matrix:")
        # self.ix_matrix.print_scores()

        # ~print(f"<<<<<<<<<<ix_matrix cell value updated ({row},{col})>>>>>>>>>>>>>>")
        # If local alignment and final_score is 0.0, no pointers
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            # ~print("local alginment. cell score 0.0. no pointers from cell")
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                # ~print(f"adding [M, {row-1}, {col}]")
                self.ix_matrix.set_pointers(row, col, ["M", row-1, col])

            if fuzzy_equals(score_from_ix_matrix, max_score):
                # ~print(f"adding [Ix, {row-1}, {col}]")
                self.ix_matrix.set_pointers(row, col, ["Ix", row - 1, col])

        # ~print(f"final score in ix_matrix cell: Ix[{row},{col}] = {self.ix_matrix.get_score(row, col):.2f}")
        # ~print(f"final pointers in ix_matrix_pointers cell: Ix[{row},{col}] = pointers: {self.ix_matrix.get_pointers(row, col)}")
        # ~print(f"<<<<<<<<<<ix_matrix cell pointers updated ({row},{col})>>>>>>>>>>>>>>")

    def update_iy(self, row, col):
        # ~print(f"\n<<<<<<<<<<<<<inside update_iy({row},{col})>>>>>>>>>>>>>>>>>")
        # ~print("GAP IN A")
        # ~print(f"seq A: {self.align_params.seq_a}")
        # ~print(f"seq B: {self.align_params.seq_b}")
        # ~print(f"considering subsequences: \nseq A[0:{row}] = '{self.align_params.seq_a[0:row]}', \nseq B [0:{col-1}] = '{self.align_params.seq_b[0:col-1]}'")
        # ~print(f"considering residues: \nXi (seq_a[{row - 1}]) = '{self.align_params.seq_a[row - 1]}', \nYj (seq_b[{col - 2}]) = '{self.align_params.seq_b[col - 2]}'")

        # seq_a = self.align_params.seq_a
        # curr_residue_a = seq_a[row - 1]
        # ~print("current last residue seq_a: " + curr_residue_a)
        # seq_b = self.align_params.seq_b
        # curr_residue_b = seq_b[col - 2]
        # ~print("current last residue seq_b: " + curr_residue_b)

        dx = self.align_params.dx
        # ~print(f"dx = {dx}")
        ex = self.align_params.ex
        # ~print(f"ex = {ex}")

        # ~print("self.m_matrix:")
        # self.m_matrix.print_scores()

        # ~print("before update iy_matrix:")
        # self.iy_matrix.print_scores()

        # ~print("in order to update score in current cell, we need max of 2 scores")
        score_from_m_matrix = self.m_matrix.get_score(row, col-1) - dx
        # ~print(f"score from m_matrix: M[{row},{col-1}]: {self.m_matrix.get_score(row, col-1):.2f} - {dx} = {score_from_m_matrix:.2f}")

        score_from_iy_matrix = self.iy_matrix.get_score(row, col-1) - ex
        # ~print(f"score from iy_matrix: Iy[{row},{col-1}]: {self.iy_matrix.get_score(row, col-1):.2f} - {ex} = {score_from_iy_matrix:.2f}")

        max_score = max(score_from_m_matrix, score_from_iy_matrix)
        # ~print(f"max_score chosen: {max_score:.2f}")

        global_alignment: bool = self.align_params.global_alignment
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        # ~print(f"global_alignment: ", global_alignment)
        # ~print(f"final_max_score: ", final_max_score)

        self.iy_matrix.set_score(row, col, final_max_score)
        # ~print("updated iy_matrix:")
        # self.iy_matrix.print_scores()

        # ~print(f"<<<<<<<<<<iy_matrix cell value updated ({row},{col})>>>>>>>>>>>>>>")
        # If local alignment and final_score is 0.0, no pointers
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            # ~print("local alginment. cell score 0.0. no pointers from cell")
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                # ~print(f"adding [M, {row}, {col-1}]")
                self.iy_matrix.set_pointers(row, col, ["M", row, col-1])

            if fuzzy_equals(score_from_iy_matrix, max_score):
                # ~print(f"adding [Iy, {row}, {col-1}]")
                self.iy_matrix.set_pointers(row, col, ["Iy", row, col-1])

        # ~print(f"final score in iy_matrix cell: Iy[{row},{col}] = {self.iy_matrix.get_score(row, col):.2f}")
        # ~print(f"final pointers in iy_matrix_pointers cell: Iy[{row},{col}] = pointers: {self.iy_matrix.get_pointers(row, col)}")
        # ~print(f"<<<<<<<<<<iy_matrix cell pointers updated ({row},{col})>>>>>>>>>>>>>>")

    # Here is my other traceback feature
    def traceback_cell(self, curr_cell_matrix_letter, row, col, input_alignments=None, input_pointer_history=None):

        global_alignment: bool = self.align_params.global_alignment

        seq_a = self.align_params.seq_a
        seq_b = self.align_params.seq_b
        # ~print(f"seq_a: {seq_a}")
        # ~print(f"seq_b: {seq_b}")

        if input_alignments is None:
            input_alignments = []

        if input_pointer_history is None:
            input_pointer_history = []

        # ~print(f"\n<<<<<<<<<<<<<<<<NOW STARTING TRACEBACK IN CELL: {curr_cell_matrix_letter} ({row}, {col})>>>>>>>>>>>>>>>>")
        # ~print(f"Current matrix: {curr_cell_matrix_letter}")
        # ~print(f"Current cell: ({row}, {col})")
        # ~print(f"Num input alignments so far: {len(input_alignments)} path(s)")
        # ~print(f"Input alignments (natural order):")
        if len(input_alignments) == 0:
            # ~print(f"(empty - no input alignments yet)")
            pass
        else:
            for align_idx, alignment in enumerate(input_alignments):
                # ~print(f"\nInput alignment {align_idx+1}:")
                # ~print(f"Input alignment Seq A: {''.join(reversed(alignment[0]))}")
                # ~print(f"Input alignment Seq B: {''.join(reversed(alignment[1]))}")
                pass

        print_pointer_history = "--->".join(
            [str(p[0]) + "(" + str(p[1]) + "," + str(p[2]) + ")" for p in input_pointer_history])
        # ~print(f"Input pointer history: {print_pointer_history}")

        if curr_cell_matrix_letter == "M":
            pointers_from_curr_cell = self.m_matrix.get_pointers(row, col)
            curr_cell_score = self.m_matrix.get_score(row, col)
        elif curr_cell_matrix_letter == "Ix":
            pointers_from_curr_cell = self.ix_matrix.get_pointers(row, col)
            curr_cell_score = self.ix_matrix.get_score(row, col)
        elif curr_cell_matrix_letter == "Iy":
            pointers_from_curr_cell = self.iy_matrix.get_pointers(row, col)
            curr_cell_score = self.iy_matrix.get_score(row, col)
        else:
            # ~print("ERROR - Invalid matrix name!")
            return

        # ~print(f"curr_cell_score: {curr_cell_score}")
        # ~print("pointers_from_curr_cell")
        for pointer in pointers_from_curr_cell:
            # ~print(f"{pointer}")
            pass
        # ~print()
        """
        self.m_matrix.print_scores()
        self.m_matrix.print_pointers()
        self.ix_matrix.print_scores()
        self.ix_matrix.print_pointers()
        self.iy_matrix.print_scores()
        self.iy_matrix.print_pointers()
        """

        # cell traceback logic (given we already have variables: row, col, input_alignments, input_pointer_history,\
        # global_alignment, seq_a, seq_b, curr_cell_matrix_letter, curr_cell_score and pointers_from_curr_cell)
        # 1. STOP CONDITION: If current cell score is 0 AND mode is local: save input alignments AS IS to universal bucket of alignments
        # 2. Else, proceed to next steps:
        # 3. Based on current cell matrix letter, determine what residues to add to incoming alignments
        # 4. Update ALL incoming alignments with appropriate residue pair determined in step 1 above
        # 5. STOP CONDITION: If there are NO pointers from current cell: save updated alignments to universal bucket of alignments
        # 6. Else, proceed to next steps:
        # 7. Get scores of next_cells from all pointers_from_curr_cell
        # 8. If local AND ANY M-->0 pointer exists, keep ONLY the M pointer (ie update pointers_from_curr_cell).
        # 9. Else proceed:
        # 10. Loop through each pointer in pointers_from_curr_cell. For each pointer in pointers_from_curr_cell:
        # 11.       update pointer history with pointer (for debugging, this doesnt affect logic per se)
        # 12.       get next_cell_matrix_letter, next_cell_row, next_cell_col, updated_input_alignments, updated_pointer_history

        #1
        if global_alignment is False and fuzzy_equals(curr_cell_score, 0.0):
            self.universal_alignments_bucket.extend(input_alignments)
            return

        # Here is one of the bug fixes I mentioned in my quiz
        if row == 0 or col == 0:
            finished = input_alignments if input_alignments else []
            self.universal_alignments_bucket.extend(finished)
            return

        #2, #3
        # Here is one of the bug fixes I mentioned in my quiz
        # Append residues based on curr cell first before passing on to pointer cells
        if curr_cell_matrix_letter == "M":
            residue_to_append_to_seq_a = seq_a[row - 1]
            # ~print(f"residue_to_append_to_seq_a = seq_a[{row - 1}]: {residue_to_append_to_seq_a}")
            residue_to_append_to_seq_b = seq_b[col - 1]
            # ~print(f"residue_to_append_to_seq_b = seq_b[{col - 1}]: {residue_to_append_to_seq_b}")
            # ~print(f"curr_cell_score_matrix_letter is {curr_cell_matrix_letter}-> No gap: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")

        elif curr_cell_matrix_letter == "Ix":
            residue_to_append_to_seq_a = seq_a[row - 1]
            # ~print(f"residue_to_append_to_seq_a = seq_a[{row - 1}]: {residue_to_append_to_seq_a}")
            residue_to_append_to_seq_b = "_"
            # ~print(f"residue_to_append_to_seq_b = - : {residue_to_append_to_seq_b}")
            # ~print(f"curr_cell_score_matrix_letter is {curr_cell_matrix_letter}-> gap in B: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")

        elif curr_cell_matrix_letter == "Iy":
            residue_to_append_to_seq_a = "_"
            # ~print(f"residue_to_append_to_seq_a = - : {residue_to_append_to_seq_a}")
            residue_to_append_to_seq_b = seq_b[col - 1]
            # ~print(f"residue_to_append_to_seq_a = seq_b[{col - 1}]: {residue_to_append_to_seq_b}")

            # ~print(f"curr_cell_score_matrix_letter is {curr_cell_matrix_letter}-> gap in A: adding {residue_to_append_to_seq_a} to A and {residue_to_append_to_seq_b} from B")
        else:
            # ~print("Invalid next_cell_letter!")
            return

        # 4
        updated_input_alignments = list()
        if len(input_alignments) == 0:
            updated_input_alignments = [[[residue_to_append_to_seq_a], [residue_to_append_to_seq_b]]]
        else:
            # Update all input alignments with latest residue based on pointer_to_next_cell
            # ~print(f"UPDATING INPUT ALIGNMENTS - adding '{residue_to_append_to_seq_a}' from seq A and '{residue_to_append_to_seq_b}' from seq B:")
            for input_alignment in input_alignments:
                # ~print(f"~~Input alignement before update: {input_alignment}")

                input_alignment_seq_a: list = input_alignment[0]
                # ~print(f"Before update (reversed to show natural order of sequence):")
                # ~print(f"Seq A: {''.join(reversed(input_alignment_seq_a))}")

                input_alignment_seq_b: list = input_alignment[1]
                # ~print(f"Before update (reversed to show natural order of sequence):")
                # ~print(f"Seq B: {''.join(reversed(input_alignment_seq_b))}")

                # ~print(f"pre-updated input alignment seq A: {input_alignment_seq_a}")
                # ~print(f"residue to add to Seq A: {residue_to_append_to_seq_a}")
                input_alignment_seq_a_updated = input_alignment_seq_a + [residue_to_append_to_seq_a]
                # ~print(f"updated input alignment seq A: {input_alignment_seq_a_updated}")

                # ~print(f"pre-updated input alignment seq B: {input_alignment_seq_b}")
                # ~print(f"residue to add to Seq B: {residue_to_append_to_seq_b}")
                input_alignment_seq_b_updated = input_alignment_seq_b + [residue_to_append_to_seq_b]
                # ~print(f"updated input alignment seq B: {input_alignment_seq_b_updated}")

                # ~print(f"After update (reversed to show natural order of sequence):")
                # ~print(f"Seq A: {''.join(reversed(input_alignment_seq_a))}")
                # ~print(f"Seq B: {''.join(reversed(input_alignment_seq_b))}")

                updated_input_alignments.append([input_alignment_seq_a_updated, input_alignment_seq_b_updated])

        # 5
        if pointers_from_curr_cell is None or (len(pointers_from_curr_cell) == 0):
            # ~print("<<<<<<<<<<<<<<<<<RECURSION END CASE. ADDING TO GLOBAL ALIGNMENTS>>>>>>>>>>>>>>>>>>")
            # ~print(f"Input pointer_to_next_cell history: {print_pointer_history}")

            # universal_alignments_bucket = self.universal_alignments_bucket
            # ~print(f"universal_alignments_bucket BEFORE update:")
            for alignment in self.universal_alignments_bucket:
                # ~print(alignment[0])
                # ~print(alignment[1])
                # ~print("\n")
                pass

            # ~print(f"alignments to be added (input_alignments):")
            for alignment in updated_input_alignments:
                # ~print(alignment[0])
                # ~print(alignment[1])
                # ~print("\n")
                pass

            final_alignments_to_add = updated_input_alignments if updated_input_alignments else input_alignments
            self.universal_alignments_bucket.extend(final_alignments_to_add)
            # ~print(f"universal_alignments_bucket AFTER update:")
            for alignment in self.universal_alignments_bucket:
                # ~print(alignment[0])
                # ~print(alignment[1])
                # ~print("\n")
                pass
            return

        #8
        if self.align_params.global_alignment is False and any([pointer[0] == "M" for pointer in pointers_from_curr_cell]):
            m_pointer = [pointer for pointer in pointers_from_curr_cell if pointer[0] == "M"][0]
            m_pointer_score = self.m_matrix.get_score(m_pointer[1], m_pointer[2])
            if fuzzy_equals(m_pointer_score, 0.0):
                pointers_from_curr_cell = [m_pointer]

        num_pointers_from_curr_cell = len(pointers_from_curr_cell)

        # 10, 11, 12
        # for each pointer_to_next_cell:
        # update alignment based on direction of pointer_to_next_cell
        # M --> both curr residues added to all existing alignments in input alignments
        # Ix --> Gap in B. include residue from seq_a
        # Iy --> Gap in A. Include residue from seq_b
        # Once updated, call next cell with updated input alignment and next cell details from pointer_to_next_cell
        # ~print(f"Looping through {num_pointers_from_curr_cell} pointers")
        for idx, pointer_to_next_cell in enumerate(pointers_from_curr_cell):
            # ~print(f"\npointer_to_next_cell {idx+1}/{num_pointers_from_curr_cell}")
            # ~print(f"pointer_to_next_cell: {pointer_to_next_cell}")
            input_pointer_history.append([curr_cell_matrix_letter, row, col])
            print_pointer_history = "--->".join([str(p[0]) + "(" + str(p[1]) + "," + str(p[2]) + ")" for p in input_pointer_history])
            # ~print(f"Updated pointer_to_next_cell history: {print_pointer_history}")

            next_cell_letter = pointer_to_next_cell[0]
            next_cell_row = pointer_to_next_cell[1]
            next_cell_col = pointer_to_next_cell[2]

            self.traceback_cell(next_cell_letter, next_cell_row, next_cell_col, updated_input_alignments, input_pointer_history)

    def find_max_score_and_location_global(self):
        # Find max score along the highest row (last row)
        highest_row = self.align_params.len_seq_a
        max_val_row = float('-inf')
        max_locations_row = []

        for j in range(self.m_matrix.ncol):
            current_score = self.m_matrix.get_score(highest_row, j)
            if current_score > max_val_row:
                max_val_row = current_score
                max_locations_row = [(highest_row, j)]
            elif fuzzy_equals(current_score, max_val_row):
                max_locations_row.append((highest_row, j))
            else:
                continue

        # Find max score along the highest column (last column)
        highest_col = self.align_params.len_seq_b
        max_val_col = float('-inf')
        max_locations_col = []

        for i in range(self.m_matrix.nrow):
            current_score = self.m_matrix.get_score(i, highest_col)
            if current_score > max_val_col:
                max_val_col = current_score
                max_locations_col = [(i, highest_col)]
            elif fuzzy_equals(current_score, max_val_col):
                max_locations_col.append((i, highest_col))
            else:
                continue

        # Determine which has the higher score
        if max_val_row > max_val_col:
            return max_val_row, set(max_locations_row)
        elif max_val_col > max_val_row:
            return max_val_col, set(max_locations_col)
        elif fuzzy_equals(max_val_col, max_val_row):
            # Both have the same max score, combine locations
            all_locations = set(max_locations_row + max_locations_col)
            return max_val_row, all_locations
        else:
            return

    def find_max_score_and_location_local(self):

        max_val = None
        max_loc = list()

        for i in range(self.m_matrix.nrow):
            for j in range(self.m_matrix.ncol):
                curr_cell_score = self.m_matrix.get_score(i, j)

                if max_val is None:
                    max_val = curr_cell_score
                    max_loc.append((i, j))
                    continue

                if fuzzy_equals(max_val, curr_cell_score) is True:
                    max_loc.append((i, j))
                    continue

                if max_val > curr_cell_score:
                    continue

                if max_val < curr_cell_score:
                    max_val = curr_cell_score
                    max_loc = [(i, j)]

        max_loc = set(max_loc)

        return max_val, max_loc

    def find_traceback_start(self):
        """
        Finds the location to start the traceback..
        Think carefully about how to set this up for local

        Returns:
            (max_val, max_loc) where max_val is the best score
            max_loc is a set() containing tuples with the (i,j) location(s) to start the traceback
             (ex. [(1,2), (3,4)])
        """
        # ~print(f"<<<<<<<<<<find_traceback_start>>>>>>>>>>>>>>")
        if self.align_params.global_alignment is True:
            return self.find_max_score_and_location_global()

        if self.align_params.global_alignment is False:
            return self.find_max_score_and_location_local()

        return

    def traceback(self): ### TO-DO! FILL IN additional arguments ###
        """
        Performs a traceback.
        Hint: include a way to printing the traceback path. This will be helpful for debugging!
           ex. M(5,4)->Iy(4,3)->M(4,2)->Ix(3,1)->Ix(2,1)->M(1,1)->M(0,0)

        """
        # ~print("<<<<<<<<<<<<<<<<<<<<<<START TRACEBACK>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        best_alignment_score, traceback_start_locations = self.find_traceback_start()
        # ~print(f"Max score found = {best_alignment_score}")
        # ~print(f"Num traceback_start_locations found = {len(traceback_start_locations)}")
        # ~print(f"traceback_start_locations = {traceback_start_locations}")

        """
        self.m_matrix.print_scores()
        self.m_matrix.print_pointers()
        self.ix_matrix.print_scores()
        self.ix_matrix.print_pointers()
        self.iy_matrix.print_scores()
        self.iy_matrix.print_pointers()
        """

        if self.align_params.global_alignment is True:
            # ~print("GLOBAL ALIGNMENT")
            pass

        if self.align_params.global_alignment is False:
            # ~print("LOCAL ALIGNMENT")
            pass

        for traceback_start_location in traceback_start_locations:
            # ~print(f"traceback_start_location = {traceback_start_location}")
            traceback_start_coord_x = traceback_start_location[0]
            traceback_start_coord_y = traceback_start_location[1]
            # ~print(f"Calling traceback_cell from M[{traceback_start_coord_x},{traceback_start_coord_y}] with score {best_alignment_score}")
            self.traceback_cell("M", traceback_start_coord_x, traceback_start_coord_y)

        # ~print("<<<<<<<<<<<<<<<<<<<<<<TRACEBACK COMPLETE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # ~print(f"Found {len(self.universal_alignments_bucket)} optimal alignment(s) of score {best_alignment_score}")

        final_alignments = list()

        for idx, alignment in enumerate(self.universal_alignments_bucket):
            # ~print(f"\nAlignment without trimming {idx+1}:")
            # ~print(f"Seq A: {''.join(reversed(alignment[0]))}")
            # ~print(f"Seq B: {''.join(reversed(alignment[1]))}")

            # ~print("trimming and reversing sequences")
            final_seq_a, final_seq_b = trim_reverse_join_alignment(alignment[0], alignment[1])

            # ~print(f"final sequences:")
            # ~print(final_seq_a)
            # ~print(final_seq_b)

            final_alignments.append((final_seq_a, final_seq_b))

        final_alignments = list(set(final_alignments))

        # Store results as instance variables for comparison
        self.final_score = best_alignment_score
        self.final_alignments = final_alignments

        # ~print(f"final_score: {best_alignment_score}")
        # ~print(f"final_alignments: {final_alignments}")

        self.write_output()

    def write_output(self):
        ### TO-DO! FILL IN ###
        with open(self.output_file, "w") as f:
            f.write(f"{round(self.final_score, 1)}\n")

            for a, b in self.final_alignments:
                f.write("\n")  # blank line before each alignment
                f.write(a + "\n")  # aligned sequence A
                f.write(b + "\n")  # aligned sequence B


# Here is my other traceback feature
def trim_reverse_join_alignment(seq_a: list, seq_b: list):
    def trim_sequences(seq_a: list, seq_b: list):
        while len(seq_a) > 0 and len(seq_b) > 0:
            if seq_a[0] == "_" or seq_b[0] == "_":
                seq_a.pop(0)
                seq_b.pop(0)
            else:
                break

        return seq_a, seq_b

    seq_a, seq_b = trim_sequences(seq_a, seq_b)
    seq_a = list(reversed(seq_a))
    seq_b = list(reversed(seq_b))
    seq_a, seq_b = trim_sequences(seq_a, seq_b)

    seq_a = "".join(seq_a)
    seq_b = "".join(seq_b)

    return seq_a, seq_b


def read_expected_output(filename):
    """
    Read expected output file and parse the format:
    - First line: expected final score
    - Empty line (gap)
    - Pairs of lines: expected sequence alignments
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Remove empty lines
    lines = [line for line in lines if line]
    
    if not lines:
        raise ValueError("Empty output file")
    
    # First line is the expected score
    expected_score = float(lines[0])
    
    # Remaining lines are sequence pairs
    expected_alignments = []
    for i in range(1, len(lines), 2):
        if i + 1 < len(lines):
            seq_a = lines[i]
            seq_b = lines[i + 1]
            expected_alignments.append((seq_a, seq_b))
    
    return expected_score, expected_alignments


def compare_outputs(align_obj, expected_output_file):
    """
    Compare generated output with expected output file.
    """
    # ~print("\n" + "="*60)
    # ~print("COMPARING OUTPUTS")
    # ~print("="*60)
    
    # Read expected output
    expected_score, expected_alignments = read_expected_output(expected_output_file)
    
    # Get generated results
    generated_score = align_obj.final_score
    generated_alignments = align_obj.final_alignments
    
    # Compare scores (round to 1 decimal place)
    generated_score_rounded = round(generated_score, 1)
    expected_score_rounded = round(expected_score, 1)
    
    score_match = (generated_score_rounded == expected_score_rounded)
    # ~print(f"Score comparison:")
    # ~print(f"  Expected: {expected_score} (rounded: {expected_score_rounded})")
    # ~print(f"  Generated: {generated_score} (rounded: {generated_score_rounded})")
    # ~print(f"  Match: {'YES' if score_match else 'NO'}")
    
    # Compare alignments
    # ~print(f"\nAlignment comparison:")
    # ~print(f"  Expected alignments: {len(expected_alignments)}")
    # ~print(f"  Generated alignments: {len(generated_alignments)}")
    
    # Convert to sets for comparison (order of alignments doesn't matter)
    expected_set = set(expected_alignments)
    generated_set = set(generated_alignments)
    
    # Find matches
    found_alignments = expected_set.intersection(generated_set)
    missing_alignments = expected_set - generated_set
    extra_alignments = generated_set - expected_set
    
    # ~print(f"  Found in generated: {len(found_alignments)}/{len(expected_alignments)}")
    
    if missing_alignments:
        # ~print(f"  Missing from generated: {len(missing_alignments)}")
        for alignment in missing_alignments:
            # ~print(f"    Missing: {alignment[0]} | {alignment[1]}")
            pass
    
    if extra_alignments:
        # ~print(f"  Extra in generated: {len(extra_alignments)}")
        for alignment in extra_alignments:
            # ~print(f"    Extra: {alignment[0]} | {alignment[1]}")
            pass
    
    if not missing_alignments and not extra_alignments:
        # ~print("  All alignments match perfectly!")
        pass
    
    # ~print("="*60)
    
    return score_match, len(found_alignments), len(expected_alignments), len(missing_alignments), len(extra_alignments)


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
        # ~print("\n" + k + ":")
        # ~print(v)
        pass


def main():

    # check that the file is being properly used
    if (len(sys.argv) !=3):
        # ~print("Please specify an input file and an output file as args.")
        return

    # ~print(f"<<<<<<<<<<<<<<<<<<<<<<PROGRAM START ]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # input variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # ~print(f"input_file: {input_file}")
    # ~print(f"output_file: {output_file}")

    # create an align object and run
    align = Align(input_file, output_file)
    align.align()


if __name__=="__main__":
    main()
