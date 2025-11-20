"""
Sequence Alignment Implementation

This module implements sequence alignment algorithms for biological sequences.
It supports both global and local alignment with configurable scoring matrices
and gap penalties. The implementation uses dynamic programming with three
score matrices (M, Ix, Iy) to handle matches/mismatches and insertions/deletions.

Classes:
    MatchMatrix: Stores scoring information for character matches
    ScoreCell: Represents a single cell in the score matrix with score and pointers
    ScoreMatrix: Manages the 2D score matrix for alignment calculations
    AlignmentParameters: Holds alignment configuration and parameters
    Align: Main alignment class that performs the alignment process

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
    """
    Score cell class stores the score and pointers for a given cell in the score matrix
    """
    def __init__(self):
        self.score = 0
        self.pointers = list()

    def set_cell_score(self, score):
        """
        Sets the score for this cell.
        
        Input:
            score = the score value to set
        """
        self.score = score

    def get_cell_score(self):
        """
        Returns the score for this cell.
        
        Returns:
            the score value of this cell
        """
        return self.score

    def add_cell_pointer(self, pointer_tuple):
        """
        Adds a pointer to this cell.
        
        Input:
            pointer_tuple = the pointer tuple to add
        """
        self.pointers.append(pointer_tuple)

    def get_cell_pointers(self):
        """
        Returns the list of pointers for this cell.
        
        Returns:
            list of pointer tuples
        """
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
        """
        Returns the score at the specified row and column.
        
        Input:
            row = the row index
            col = the column index
        Returns:
            the score value at the specified position
        """
        ### TO-DO! FILL IN ###
        return self.score_matrix[row, col].get_cell_score()

    def set_score(self, row, col, score):
        """
        Sets the score at the specified row and column.
        
        Input:
            row = the row index
            col = the column index
            score = the score value to set
        """
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

    def set_pointers(self, row, col, pointer: list):
        """
        Sets a pointer at the specified row and column.
        
        Input:
            row = the row index
            col = the column index
            pointer = the pointer list to add (should be length 3)
        """
        ### TO-DO! FILL IN - this needs additional arguments ###
        ### TO-DO! FILL IN ###
        assert len(pointer) == 3, "invalid pointer"
        curr_pointers = self.score_matrix[row, col].get_cell_pointers()
        curr_pointers.append(pointer)


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

        # object variable to store final list of alignments
        self.universal_alignments_bucket = list()

    def align(self):
        """
        Main method for running alignment.
        """
        # load the alignment parameters into the align_params object
        self.align_params.load_params_from_file(self.input_file)
        # populate the score matrices based on the input parameters
        self.populate_score_matrices()
        # perform a traceback and write the output to an output file
        self.traceback()

    def populate_score_matrices(self):
        """
        Method to populate the score matrices based on the data in align_params.
        Should call update(i,j) for each entry in the score matrices
        Note: You MUST initialize M, Ix, Iy in this function rather than elsewhere
        """
        num_rows_in_score_matrices = self.align_params.len_seq_a+1
        num_columns_in_score_matrices = self.align_params.len_seq_b + 1

        # Initializing ScoreMatrix M
        self.m_matrix = ScoreMatrix("M", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Setting 0th row and column to all zeroes
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.m_matrix.set_score(i, 0, 0.0)
        for j in range(num_columns_in_score_matrices):
            self.m_matrix.set_score(0, j, 0.0)

        # Initializing ScoreMatrix Ix
        self.ix_matrix = ScoreMatrix("Ix", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Setting 0th row and column to all zeroes
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.ix_matrix.set_score(i, 0, 0.0)
        for j in range(num_columns_in_score_matrices):
            self.ix_matrix.set_score(0, j, 0.0)

        # Initializing ScoreMatrix Iy
        self.iy_matrix = ScoreMatrix("Iy", num_rows_in_score_matrices, num_columns_in_score_matrices)
        # Setting 0th row and column to all zeroes
        # Here is where I could add end-gap penalties
        for i in range(num_rows_in_score_matrices):
            self.iy_matrix.set_score(i, 0, 0.0)
        for j in range(num_columns_in_score_matrices):
            self.iy_matrix.set_score(0, j, 0.0)

        # Now we iterate over cells in matrices and update them all
        for i in range(1, self.align_params.len_seq_a+1):
            for j in range(1, self.align_params.len_seq_b+1):
                self.update(row=i, col=j)

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
        """
        Method to update the M matrix at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """
        # First we update curr cell score
        seq_a = self.align_params.seq_a
        curr_residue_a = seq_a[row-1]
        seq_b = self.align_params.seq_b
        curr_residue_b = seq_b[col-1]

        s_ij_match = self.align_params.match_matrix.get_score(curr_residue_a, curr_residue_b)

        # in order to update score in current cell, we need max of 3 scores
        score_from_m_matrix = self.m_matrix.get_score(row - 1, col - 1) + s_ij_match
        score_from_ix_matrix = self.ix_matrix.get_score(row - 1, col - 1) + s_ij_match
        score_from_iy_matrix = self.iy_matrix.get_score(row - 1, col - 1) + s_ij_match

        # Find max score among 3
        max_score = max(score_from_m_matrix, score_from_ix_matrix, score_from_iy_matrix)

        global_alignment: bool = self.align_params.global_alignment
        # If local alignment, no negative score allowed in matrices
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)

        self.m_matrix.set_score(row, col, final_max_score)

        # Next, we move on to pointers from curr cell
        # If local alignment and final_score is 0.0, no pointers from cell
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                self.m_matrix.set_pointers(row, col, ["M", row-1, col-1])

            if fuzzy_equals(score_from_ix_matrix, max_score):
                self.m_matrix.set_pointers(row, col, ["Ix", row - 1, col - 1])

            if fuzzy_equals(score_from_iy_matrix, max_score):
                self.m_matrix.set_pointers(row, col, ["Iy", row - 1, col - 1])

    def update_ix(self, row, col):
        """
        Method to update the Ix matrix at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """
        # First we update curr cell score
        dy = self.align_params.dy
        ey = self.align_params.ey

        # in order to update score in current cell, we need max of 2 scores
        score_from_m_matrix = self.m_matrix.get_score(row-1, col) - dy
        score_from_ix_matrix = self.ix_matrix.get_score(row-1, col) - ey
        max_score = max(score_from_m_matrix, score_from_ix_matrix)

        global_alignment: bool = self.align_params.global_alignment
        # If local alignment, no negative score allowed in matrices
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        self.ix_matrix.set_score(row, col, final_max_score)

        # Next we move to pointers from curr cell
        # If local alignment and final_score is 0.0, no pointers
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                self.ix_matrix.set_pointers(row, col, ["M", row-1, col])

            if fuzzy_equals(score_from_ix_matrix, max_score):
                self.ix_matrix.set_pointers(row, col, ["Ix", row - 1, col])

    def update_iy(self, row, col):
        """
        Method to update the Iy matrix at a given row and column index.

        Input:
           row = the row index to update
           col = the column index to update
        """
        # First we update curr cell score
        dx = self.align_params.dx
        ex = self.align_params.ex

        # in order to update score in current cell, we need max of 2 scores
        score_from_m_matrix = self.m_matrix.get_score(row, col-1) - dx
        score_from_iy_matrix = self.iy_matrix.get_score(row, col-1) - ex
        max_score = max(score_from_m_matrix, score_from_iy_matrix)

        global_alignment: bool = self.align_params.global_alignment
        final_max_score = max_score if global_alignment is True else max(0.0, max_score)
        self.iy_matrix.set_score(row, col, final_max_score)

        # Next we move to pointers from curr cell
        # If local alignment and final_score is 0.0, no pointers
        if global_alignment is False and fuzzy_equals(0.0, final_max_score) is True:
            pass
        else:
            # Here is my traceback pointer approach
            # Here I set pointer from current cell (to the cell(s) that led to best score)
            if fuzzy_equals(score_from_m_matrix, max_score):
                self.iy_matrix.set_pointers(row, col, ["M", row, col-1])

            if fuzzy_equals(score_from_iy_matrix, max_score):
                self.iy_matrix.set_pointers(row, col, ["Iy", row, col-1])

    # Here is my other traceback feature
    def traceback_cell(self, curr_cell_matrix_letter, row, col, input_alignments=None, input_pointer_history=None):
        """
        Method to perform a traceback from a given cell in the score matrices.

        Input:
           curr_cell_matrix_letter = the letter of the matrix to traceback from
           row = the row index to traceback from
           col = the column index to traceback from
           input_alignments = the list of alignments to update
           input_pointer_history = the list of pointers to update
        """
        global_alignment: bool = self.align_params.global_alignment

        seq_a = self.align_params.seq_a
        seq_b = self.align_params.seq_b

        # Set to empty list if none passed in
        if input_alignments is None:
            input_alignments = []

        if input_pointer_history is None:
            input_pointer_history = []

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
            return

        # Core Logic:
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

        #1  STOP CONDITION: If current cell score is 0 AND mode is local: save input alignments AS IS to universal bucket of alignments
        if global_alignment is False and fuzzy_equals(curr_cell_score, 0.0):
            self.universal_alignments_bucket.extend(input_alignments)
            return

        # Here is one of the bug fixes I mentioned in my quiz
        if row == 0 or col == 0:
            finished = input_alignments if input_alignments else []
            self.universal_alignments_bucket.extend(finished)
            return

        #2, #3 Based on current cell matrix letter, determine what residues to add to incoming alignments
        # Here is one of the bug fixes I mentioned in my quiz
        # Append residues based on curr cell first before passing on to pointer cells
        if curr_cell_matrix_letter == "M":
            residue_to_append_to_seq_a = seq_a[row - 1]
            residue_to_append_to_seq_b = seq_b[col - 1]
        elif curr_cell_matrix_letter == "Ix":
            residue_to_append_to_seq_a = seq_a[row - 1]
            residue_to_append_to_seq_b = "_"
        elif curr_cell_matrix_letter == "Iy":
            residue_to_append_to_seq_a = "_"
            residue_to_append_to_seq_b = seq_b[col - 1]
        else:
            return

        # 4 Update ALL incoming alignments with appropriate residue pair determined in step 1 above
        updated_input_alignments = list()
        # If empty list, initialize with current residues
        if len(input_alignments) == 0:
            updated_input_alignments = [[[residue_to_append_to_seq_a], [residue_to_append_to_seq_b]]]
        else:
            # Update all input alignments with latest residue based on pointer_to_next_cell
            for input_alignment in input_alignments:
                input_alignment_seq_a: list = input_alignment[0]
                input_alignment_seq_b: list = input_alignment[1]
                input_alignment_seq_a_updated = input_alignment_seq_a + [residue_to_append_to_seq_a]
                input_alignment_seq_b_updated = input_alignment_seq_b + [residue_to_append_to_seq_b]

                updated_input_alignments.append([input_alignment_seq_a_updated, input_alignment_seq_b_updated])

        # 5 STOP CONDITION: If there are NO pointers from current cell: save updated alignments to universal bucket of alignments
        if pointers_from_curr_cell is None or (len(pointers_from_curr_cell) == 0):
            final_alignments_to_add = updated_input_alignments if updated_input_alignments else input_alignments
            self.universal_alignments_bucket.extend(final_alignments_to_add)
            return

        # 8 If local alignment and any M-->0 pointer exists, keep ONLY the M pointer
        if self.align_params.global_alignment is False and any([pointer[0] == "M" for pointer in pointers_from_curr_cell]):
            m_pointer = [pointer for pointer in pointers_from_curr_cell if pointer[0] == "M"][0]
            m_pointer_score = self.m_matrix.get_score(m_pointer[1], m_pointer[2])
            if fuzzy_equals(m_pointer_score, 0.0):
                pointers_from_curr_cell = [m_pointer]

        # 10, 11, 12
        # for each pointer_to_next_cell:
        # update alignment based on direction of pointer_to_next_cell
        # M --> both curr residues added to all existing alignments in input alignments
        # Ix --> Gap in B. include residue from seq_a
        # Iy --> Gap in A. Include residue from seq_b
        # Once updated, call next cell with updated input alignment and next cell details from pointer_to_next_cell
        # Looping through {num_pointers_from_curr_cell} pointers
        for idx, pointer_to_next_cell in enumerate(pointers_from_curr_cell):
            input_pointer_history.append([curr_cell_matrix_letter, row, col])
            next_cell_letter = pointer_to_next_cell[0]
            next_cell_row = pointer_to_next_cell[1]
            next_cell_col = pointer_to_next_cell[2]

            self.traceback_cell(next_cell_letter, next_cell_row, next_cell_col, updated_input_alignments, input_pointer_history)

    def find_max_score_and_location_global(self):
        """
        Method to find the max score and location in the global alignment.

        Returns:
            (max_val, max_loc) where max_val is the best score
            max_loc is a set() containing tuples with the (i,j) location(s) to start the traceback
             (ex. [(1,2), (3,4)])
        """
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
        """
        Method to find the max score and location in the local alignment.

        Returns:
            (max_val, max_loc) where max_val is the best score
            max_loc is a set() containing tuples with the (i,j) location(s) to start the traceback
             (ex. [(1,2), (3,4)])
        """
        # Initialize max values
        max_val = None
        max_loc = list()

        for i in range(self.m_matrix.nrow):
            for j in range(self.m_matrix.ncol):
                curr_cell_score = self.m_matrix.get_score(i, j)
                # If max_val is None, set max_val to current cell score and add location to max_loc
                if max_val is None:
                    max_val = curr_cell_score
                    max_loc.append((i, j))
                    continue

                # If current cell score is equal to max_val, add location to max_loc
                if fuzzy_equals(max_val, curr_cell_score) is True:
                    max_loc.append((i, j))
                    continue

                # If current cell score is greater than max_val, continue
                if max_val > curr_cell_score:
                    continue

                # If current cell score is less than max_val, set max_val to current cell score and add location to max_loc
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
        if self.align_params.global_alignment is True:
            return self.find_max_score_and_location_global()

        if self.align_params.global_alignment is False:
            return self.find_max_score_and_location_local()

        return

    def traceback(self):
        """
        Performs a traceback to find optimal alignments.
        Hint: include a way to printing the traceback path. This will be helpful for debugging!
           ex. M(5,4)->Iy(4,3)->M(4,2)->Ix(3,1)->Ix(2,1)->M(1,1)->M(0,0)
        """
        best_alignment_score, traceback_start_locations = self.find_traceback_start()

        for traceback_start_location in traceback_start_locations:
            traceback_start_coord_x = traceback_start_location[0]
            traceback_start_coord_y = traceback_start_location[1]
            self.traceback_cell("M", traceback_start_coord_x, traceback_start_coord_y)

        final_alignments = list()
        for idx, alignment in enumerate(self.universal_alignments_bucket):
            final_seq_a, final_seq_b = trim_reverse_join_alignment(alignment[0], alignment[1])
            final_alignments.append((final_seq_a, final_seq_b))
        final_alignments = list(set(final_alignments))

        # Store results as instance variables for comparison
        self.final_score = best_alignment_score
        self.final_alignments = final_alignments

        self.write_output()

    def write_output(self):
        """
        Method to write the output to an output file.

        Input:
            output_file = file to write the output alignments to
        """
        ### TO-DO! FILL IN ###
        with open(self.output_file, "w") as f:
            f.write(f"{round(self.final_score, 1)}\n")

            for a, b in self.final_alignments:
                f.write("\n")
                f.write(a + "\n")
                f.write(b + "\n")


# Here is my other traceback feature
def trim_reverse_join_alignment(seq_a: list, seq_b: list):
    """
    Method to trim and reverse the sequences.
    Input:
        seq_a = the sequence A to trim and reverse
        seq_b = the sequence B to trim and reverse
    """
    def trim_sequences(seq_a: list, seq_b: list):
        """
        Method to trim the sequences.
        Input:
            seq_a = the sequence A to trim
            seq_b = the sequence B to trim
        """
        while len(seq_a) > 0 and len(seq_b) > 0:
            if seq_a[0] == "_" or seq_b[0] == "_":
                seq_a.pop(0)
                seq_b.pop(0)
            else:
                break

        return seq_a, seq_b

    # Trim sequences
    seq_a, seq_b = trim_sequences(seq_a, seq_b)
    seq_a = list(reversed(seq_a))
    seq_b = list(reversed(seq_b))
    # Trim in reverse (natural order)
    seq_a, seq_b = trim_sequences(seq_a, seq_b)

    seq_a = "".join(seq_a)
    seq_b = "".join(seq_b)

    return seq_a, seq_b


def read_input_file(filename):
    """
    Method to read the input file.
    Input:
        filename = the name of the input file
    """
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


def main():
    """
    Main function to run the alignment program.
    
    Expects command line arguments:
        sys.argv[1] = input file path
        sys.argv[2] = output file path
    """
    # check that the file is being properly used
    if (len(sys.argv) !=3):
        # ~print("Please specify an input file and an output file as args.")
        return

    # input variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # create an align object and run
    align = Align(input_file, output_file)
    align.align()


if __name__=="__main__":
    main()
