import pandas as pd


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
    
    # parse mode flag with validation
    mode = int(clean[2])
    if mode not in [0, 1]:
        raise ValueError(f"Invalid mode flag: {mode}. Must be 0 (global) or 1 (local)")
    data['global_alignment'] = (mode == 0)
    
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
    
    # verify we have exactly the expected number of entries
    expected_entries = data['len_alphabet_a'] * data['len_alphabet_b']
    if len(matrix_data) != expected_entries:
        raise ValueError(f"Expected {expected_entries} matrix entries but found {len(matrix_data)}")
    
    data['match_matrix'] = pd.DataFrame(matrix_data)
    
    return data


def print_data(data):
    print("seq_a:", data['seq_a'])
    print("seq_b:", data['seq_b'])
    print("global:", data['global_alignment'])
    print("gaps:", data['dx'], data['ex'], data['dy'], data['ey'])
    print("alphabets:", data['alphabet_a'], data['alphabet_b'])
    print("match matrix:")
    print(data['match_matrix'])

